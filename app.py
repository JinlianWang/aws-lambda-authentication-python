from flask import Flask, request, redirect, Response
import os
import uuid
import urllib.parse
from urllib.parse import urlencode
import base64
import requests

app = Flask(__name__)
cognito_app_id = "1vvp0tt53g1uhntoa5bmvnvk2a" if os.environ.get("COGNITO_APP_ID") is None else os.environ.get("COGNITO_APP_ID")
cognito_app_secret = "<secret>" if os.environ.get("COGNITO_APP_SECRET") is None else os.environ.get("COGNITO_APP_SECRET")
cognito_domain_prefix = "sunnyoauth" if os.environ.get("COGNITO_DOMAIN_PREFIX") is None else os.environ.get("COGNITO_DOMAIN_PREFIX")
api_gateway_url = "https://f4y2bwysuc.execute-api.us-east-1.amazonaws.com/dev" if os.environ.get("API_GATEWAY_URL") is None else os.environ.get("API_GATEWAY_URL")
login_redirect_url = "http://athenatestsunny2020.s3-website-us-east-1.amazonaws.com/" if os.environ.get("LOGIN_REDIRECT_URL") is None else os.environ.get("LOGIN_REDIRECT_URL")
cors_allow_origin = "http://athenatestsunny2020.s3-website-us-east-1.amazonaws.com/" if os.environ.get("CORS_ALLOW_ORIGIN") is None else os.environ.get("CORS_ALLOW_ORIGIN")
sessionInfo = None


@app.route('/apis/authentication/login')
def login_url():
    return createResponse(getCognitoHost() + "/oauth2/authorize?client_id=" \
                          + cognito_app_id + "&redirect_uri=" + urllib.parse.quote_plus(getRedirectURI()) \
                          + "&scope=openid&response_type=code")


@app.route('/apis/authentication/status')
def login_status():
    global sessionInfo
    if sessionInfo is None:
        return ""
    return createResponse(sessionInfo)


@app.route('/apis/authentication/exchange')
def exchange_code():
    code = request.args.get("code")
    params = {"code": code, "grant_type": "authorization_code", "redirect_uri": getRedirectURI()}
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": getBase64EncodedCredential()}
    data = urlencode(params)
    response = requests.post(getCognitoHost() + "/oauth2/token", data=data, headers=headers)
    access_token = response.json()["access_token"]
    user_info = getUserInfo(access_token)
    user_info["id"] = str(uuid.uuid4())
    global sessionInfo
    sessionInfo = user_info
    return redirect(login_redirect_url + "?session=" + sessionInfo["id"])


@app.route('/apis/authentication/logout')
def logout():
    global sessionInfo
    sessionInfo = None
    return createResponse("")


def getUserInfo(access_token: str):
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.get(getCognitoHost() + "/oauth2/userInfo", headers=headers)
    return response.json()


def getCognitoHost():
    return "https://" + cognito_domain_prefix + ".auth.us-east-1.amazoncognito.com"


def getRedirectURI():
    return api_gateway_url + "/apis/authentication/exchange"


def getBase64EncodedCredential():
    return "Basic " + base64.b64encode((cognito_app_id + ":" + cognito_app_secret).encode("ascii")).decode("ascii")


def createResponse(body: str):
    global cors_allow_origin
    response = Response(body)
    response.headers['Access-Control-Allow-Origin'] = cors_allow_origin
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,POST,GET'
    return response


if __name__ == '__main__':
    app.run()
