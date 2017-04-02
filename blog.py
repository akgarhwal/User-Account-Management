
#
# Copyright (c) 2008 - 2013 10gen, Inc. <http://10gen.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#

import pymongo
import sessionDAO
import userDAO
import bottle
import cgi
import re

from bs4 import BeautifulSoup
from IPython.display import Image
import urllib



__author__ = 'aje'


# General Discussion on structure. This program implements a blog. This file is the best place to start to get
# to know the code. In this file, which is the controller, we define a bunch of HTTP routes that are handled
# by functions. The basic way that this magic occurs is through the decorator design pattern. Decorators
# allow you to modify a function, adding code to be executed before and after the function. As a side effect
# the bottle.py decorators also put each callback into a route table.

# These are the routes that the blog must handle. They are decorated using bottle.py


@bottle.route('/images/<filename:re:.*\.jpg>')
def send_image(filename):
    return bottle.static_file(filename, root='./images/')

@bottle.route('/static/<filename:path>')
def send_static(filename):
    return bottle.static_file(filename, root='./static/')





#Code-Forces data scrapping
def codeforces_data_scrap(handle):
    submission_url = 'http://codeforces.com/submissions/'  


    r = urllib.urlopen(submission_url+handle).read()
    soup = BeautifulSoup(r,"lxml")
    #print type(soup)

    #Finding total no of submission page
    pageno = soup.find_all("div",class_="pagination")


    ind=1
    numPage=1
    if len(pageno) != 1:
        ind = 0;
        pageno = pageno[1].find("ul")
        pageno = pageno.find_all("li")
        numPage =  int(pageno[-2].get_text())
    page_url = '/page/'



    for i in range(1,numPage+1):
        url = submission_url+handle+page_url+str(i)
        print url

        r = urllib.urlopen(url).read()
        soup = BeautifulSoup(r,"lxml")

        datatable = soup.find_all("table", class_="status-frame-datatable")
        #print len(datatable)

        TR =  datatable[0].find_all("tr")
        TR = TR[1:]
        #print TR[1]
        print "TOtal Submission : "+str(len(TR))
        codeforces_data =  "\"Code-Forces\" : [\n\t"
        for tr in TR :
            submission_link = tr.find("td",class_="id-cell");
            submission_link = submission_link.a["href"]
            
            problem_name_link = tr.find_all("td",class_="status-small")
            problem_name_link = problem_name_link[1]
            problem_link = (problem_name_link.a["href"]).strip()
            problem_name = (problem_name_link.find("a").get_text()).strip()
            
            submission_id_verdict = tr.find("td",class_="status-cell status-small status-verdict-cell")
            submission_id_verdict = submission_id_verdict.find_all("span")
            submission_id = submission_id_verdict[0]["submissionid"]
            submission_verdict = submission_id_verdict[0]["submissionverdict"]
            codeforces_data+= "\t{ \"submission_link\" : \"" +submission_link +"\",\n\t  \"submission_id\" : \"" + submission_id + "\",\n\t  \"submission_verdict\" : \"" + submission_verdict + "\",\n\t  \"problem_name\" : \"" + problem_name+ "\",\n\t  \"problem_link\" : \"" + problem_link+"\"\n\t}"
            codeforces_data += "\n"


    codeforces_data += "]"
    return codeforces_data







# This route is the main page of the blog
@bottle.route('/')
def blog_index():

    cookie = bottle.request.get_cookie("session")

    username = sessions.get_username(cookie)

    # todo: this is not yet implemented at this point in the course

    return bottle.template('blog_template', dict(username=username))



# displays the initial blog signup form
@bottle.get('/signup')
def present_signup():

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)  # see if user is logged in
    print username,"##############################################"

    if not(username is None or username == ""):
        # print "welcome: can't identify user...redirecting to signup"
        bottle.redirect("/index")
        return 

    return bottle.template("signup",
                           dict(username="", password="",
                                password_error="",
                                email="", username_error="", email_error="",
                                verify_error =""))

# display profile page of user
@bottle.get('/profile')
def profile_page():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    print username
    res = database.users.find_one({'username':username})
    print res['_id']
    return bottle.template('blog_template', dict(username=username))





# displays the initial blog login form
@bottle.get('/login')
def present_login():

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)  # see if user is logged in
    if not(username is None or username == ""):
        # print "welcome: can't identify user...redirecting to signup"
        bottle.redirect("/index")
        return 

    return bottle.template("login",
                          dict(username="", password="",
                                login_error=""))

# handles a login request
@bottle.post('/login')
def process_login():

    username = bottle.request.forms.get("username")
    password = bottle.request.forms.get("password")

    print "user submitted ", username, "pass ", password

    user_record = users.validate_login(username, password)
    if user_record:
        # username is stored in the user collection in the _id key
        session_id = sessions.start_session(user_record['_id'])

        if session_id is None:
            bottle.redirect("/internal_error")

        cookie = session_id

        # Warning, if you are running into a problem whereby the cookie being set here is
        # not getting set on the redirect, you are probably using the experimental version of bottle (.12).
        # revert to .11 to solve the problem.
        bottle.response.set_cookie("session", cookie)

        bottle.redirect("/index")

    else:
        return bottle.template("login",
                               dict(username=cgi.escape(username), password="",
                                    login_error="Invalid Login"))


@bottle.get('/internal_error')
@bottle.view('error_template')
def present_internal_error():
    return {'error':"System has encountered a DB error"}


@bottle.get('/logout')
def process_logout():

    cookie = bottle.request.get_cookie("session")

    sessions.end_session(cookie)

    bottle.response.set_cookie("session", "")


    bottle.redirect("/signup")


@bottle.post('/signup')
def process_signup():

    email = bottle.request.forms.get("email")
    username = bottle.request.forms.get("username")
    password = bottle.request.forms.get("password")
    verify = bottle.request.forms.get("verify")
    handle = bottle.request.forms.get("Codeforces-handle")

    #codeforces_data = codeforces_data_scrap(handle)

    # set these up in case we have an error case
    errors = {'username': cgi.escape(username), 'email': cgi.escape(email)}
    if validate_signup(username, password, verify, email, errors):

        if not users.add_user(username, password, email,handle):
            # this was a duplicate
            errors['username_error'] = "Username already in use. Please choose another"
            return bottle.template("signup", errors)

        session_id = sessions.start_session(username)
        print session_id
        # print codeforces_data
        bottle.response.set_cookie("session", session_id)
        bottle.redirect("/index")
    else:
        print "user did not validate"
        return bottle.template("signup", errors)



@bottle.get("/index")
def present_welcome():
    # check for a cookie, if present, then extract value

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)  # see if user is logged in
    if username is None:
        print "welcome: can't identify user...redirecting to signup"
        bottle.redirect("/signup")

    return bottle.template("index", {'username': username})


# Helper Functions

# validates that the user information is valid for new signup, return True of False
# and fills in the error string if there is an issue
def validate_signup(username, password, verify, email, errors):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    PASS_RE = re.compile(r"^.{3,20}$")
    EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

    errors['username_error'] = ""
    errors['password_error'] = ""
    errors['verify_error'] = ""
    errors['email_error'] = ""

    if email != "":
        if not EMAIL_RE.match(email):
            errors['email_error'] = "invalid email address"
            return False
    if not USER_RE.match(username):
        errors['username_error'] = "invalid username. try just letters and numbers"
        return False

    if not PASS_RE.match(password):
        errors['password_error'] = "invalid password."
        return False
    if password != verify:
        errors['verify_error'] = "password must match"
        return False
    
    return True

connection_string = "mongodb://localhost"
connection = pymongo.MongoClient(connection_string)
database = connection.blog

users = userDAO.UserDAO(database)
sessions = sessionDAO.SessionDAO(database)


bottle.debug(True)
bottle.run(host='localhost', port=8082,reloader='True')         # Start the webserver running and wait for requests

