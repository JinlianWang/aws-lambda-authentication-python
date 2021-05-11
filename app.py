from flask import Flask, request, redirect
import uuid
import urllib.parse
from urllib.parse import urlencode
from datetime import datetime, timezone, timedelta
import base64
import requests

app = Flask(__name__)
cognito_app_id = "1vvp0tt53g1uhntoa5bmvnvk2a"
cognito_app_secret = "<secret>"
cognito_domain_prefix = "sunnyoauth"
api_gateway_url = "https://f4y2bwysuc.execute-api.us-east-1.amazonaws.com/dev"
sessionInfo = {"id": "123", "sub": "sunny", "expirationTime": datetime.now(timezone.utc) + timedelta(minutes=15)}


@app.route('/apis/authentication/login')
def login_url():
    return redirect(getCognitoHost() + "/oauth2/authorize?client_id=" \
                    + cognito_app_id + "&redirect_uri=" + urllib.parse.quote_plus(getRedirectURI()) \
                    + "&scope=openid&response_type=code")


@app.route('/apis/authentication/status')
def login_status():
    if sessionInfo is None:
        return ""
    return sessionInfo


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
    return user_info


@app.route('/apis/authentication/logout')
def logout():
    global sessionInfo
    sessionInfo = None
    return ""


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


if __name__ == '__main__':
    app.run()
