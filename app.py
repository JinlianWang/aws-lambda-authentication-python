import json
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
session_info = None


@app.route('/apis/authentication/login')
def login_url():
    return createResponse(getCognitoHost() + "/oauth2/authorize?client_id=" \
                          + cognito_app_id + "&redirect_uri=" + urllib.parse.quote_plus(getRedirectURI()) \
                          + "&scope=openid&response_type=code")


@app.route('/apis/authentication/status')
def login_status():
    global session_info
    if (session_info is not None) and (getSessionToken() == session_info["id"]):
        return createResponse(json.dumps(session_info))
    print("Server: " + session_info["id"] if (session_info is not None) else "")
    print("Session: " + getSessionToken())
    return ""


@app.route('/apis/authentication/exchange')
def exchange_code():
    code = request.args.get("code")
    params = {"code": code, "grant_type": "authorization_code", "redirect_uri": getRedirectURI()}
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": getBase64EncodedCredential()}
    data = urlencode(params)
    response = requests.post(getCognitoHost() + "/oauth2/token", data=data, headers=headers)
    print("response: " + response.text)
    access_token = response.json()["access_token"]
    print("token: " + access_token)
    user_info = getUserInfo(access_token)
    user_info["id"] = str(uuid.uuid4())
    global session_info
    session_info = user_info
    print("user info: " + json.dumps(user_info))
    return redirect(login_redirect_url + "?session=" + session_info["id"])


@app.route('/apis/authentication/resource')
def protected_resource():
    global session_info
    if (session_info is not None) and (getSessionToken() == session_info["id"]):
        return createResponse("Protected Resource Retrieved from DB.")
    return createResponse("", 401)


@app.route('/apis/authentication/logout')
def logout():
    global session_info
    session_info = None
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


def createResponse(body: str, status_code: int = 200):
    global cors_allow_origin
    response = Response(body)
    response.headers['Access-Control-Allow-Origin'] = cors_allow_origin
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,POST,GET'
    response.status_code = status_code
    return response


def getSessionToken():
    auth_header = request.headers.get("Authorization")
    if auth_header is not None:
        print("Header: " + auth_header)
        auth_parts = auth_header.split(" ")
        if (len(auth_parts) == 2) and (auth_parts[0] == "Bearer"):
            return auth_parts[1]
    return ""


if __name__ == '__main__':
    app.run()
