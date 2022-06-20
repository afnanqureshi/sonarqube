This python script bulk updates the visibility of selected projects in SonarQube.
The steps to run the script are as follows:
1. Set the environment in the 'SQ_env' variable in which the projects' visibility needs
    to be changed.
2. Set the admin token in the 'SQ_token' variable.
3. Set the 'visibility' variable to 'private' or 'public'
4. Set the 'key_expression' variable to match the key pattern of those projects whose
    visibility needs to be changed.
5. Run the script as a python file
NOTE: The 'key_expression' variable here is a regular expression and not a string.
    For example: If the key_expression is set to '^example.com', it will change the
    visibility of all the projects that have a key pattern that starts with
     'example.com'.
    For projects that you want to just match the key pattern, end the key_expression with a
    '$' symbol. For example '^example.com.test$' will only update project that has a key
    pattern of 'example.com.test'