<!DOCTYPE html>

<html>
  <head>
    <title>Sign Up</title>
    <style type="text/css">
      .label {text-align: right}
      .error {color: red}
    </style>
<!-- Latest compiled and minified CSS -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

<!-- Optional theme -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">

<!-- Latest compiled and minified JavaScript -->
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
  </head>

  <body>
  <div class="container">    
        <div style="margin-top:100px;" class="mainbox col-md-9 col-md-offset-2 col-sm-8 col-sm-offset-2">                    
            <div class="panel panel-info" >
                    <div class="panel-heading">
                        <div class="panel-title">Sign up</div>
                        <div style="float:right; font-size: 80%; position: relative; top:-10px"><a href="/login">Log in</a></div>
                    </div>     

                    <div style="padding-top:30px" class="panel-body" >

                        <div style="display:none" id="login-alert" class="alert alert-danger col-sm-12"></div>
                            
                        <form id="signupform" class="form-horizontal" role="form" method="post" href="/signup">
                            
                            <div class="form-group">
                                     <label for="email" class="col-md-3 control-label">Email</label>
                                      <div class="col-md-8">
                                          <input type="text" class="form-control" name="email" placeholder="Email Address" required>
                                     </div>
                                     %if (email_error != ""):
                                          <label class="error">{{email_error}}</label>
                                          %end
                                  </div>   



                            <div class="form-group">
                                    <label class="col-md-3 control-label">User Name</label>
                                    <div class="col-md-8">
                                        <input type="text" class="form-control" name="username" placeholder="Username" required>
                                    </div>

                                          %if (username_error != ""):
                                          <label class="error">{{username_error}}</label>
                                          %end
                                </div>


                 
                                <div class="form-group">
                                    <label for="password" class="col-md-3 control-label">Password</label>
                                    <div class="col-md-8">
                                        <input type="password" class="form-control" name="password" placeholder="Password" required>
                                    </div>
                                    %if (password_error != ""):
                                          <label class="error">{{password_error}}</label>
                                          %end
                                </div>
                                <div class="form-group">
                                    <label class="col-md-3 control-label">Confirm Password</label>
                                    <div class="col-md-8">
                                        <input type="password" class="form-control" name="verify" placeholder="Confirm Password" required>
                                    </div>
                                    %if (verify_error != ""):
                                          <label class="error">{{verify_error}}</label>
                                          %end
                                </div>


                                <div class="form-group">
                                    <label class="col-md-3 control-label">Codeforces Handle</label>
                                    <div class="col-md-8">
                                        <input type="text" class="form-control" name="Codeforces-handle" placeholder="Codeforces Handle" required>
                                    </div>

                                         
                                </div>
                               <!--  <div class="form-group">
                                    <label for="icode" class="col-md-3 control-label">Invitation Code</label>
                                    <div class="col-md-9">
                                        <input type="text" class="form-control" name="icode" placeholder="">
                                    </div>
                                </div> -->



                                <div style="margin-top:10px" class="form-group">
                                    <!-- Button -->

                                    <div style = "margin-left:200px" class="col-sm-12 controls">
                                     <input type="submit" class="btn btn-success" value="Sign up">  </input>
                                      

                                    </div>
                                </div>


                                <div class="form-group">
                                    <div class="col-md-12 control">
                                        <div style="border-top: 1px solid#888; padding-top:15px; font-size:85%" >
                                            Already has account 
                                        <a href="/login" >
                                            Log in Here
                                        </a>
                                        </div>
                                    </div>
                                </div>    
                            </form>     



                        </div>                     
                    </div>  
        </div>
        
    </div>












  </body>

</html>
