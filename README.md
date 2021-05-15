# aws-lambda-authentication-python

This project is to demo how to create a Lambda function in Python which performs user authentication using oAuth Authorization Code grant type through AWS Cognito. The details, such as workflows and sequence diagrams can be found at [User authentication through authorization code grant type using AWS Cognito](https://dev.to/jinlianwang/user-authentication-through-authorization-code-grant-type-using-aws-cognito-1f93). 

The project can be developed locally and deployed to production in AWS. See "Development" and "Deploy" sections for procedures.


## Development

Use the following command to hot load any change in Python code. 

```
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Use IntelliJ "debug ..." to debug and stop at breakpoints. 

## Deploy

Follow [How to deploy a Flask app on AWS Lambda](https://blog.apcelent.com/deploy-flask-aws-lambda.html) to set up Zappa, the tool that we use in order to deploy code to AWS Lambda. Zappa also sets up API Gateway fronting Lambda function and enables CORS support for Lambda proxy integration. 

To deploy to AWS, use the following command to activate virtual environment and deploy changes to AWS. 

```
source .env/bin/activate
zappa deploy dev
```