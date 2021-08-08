from flask import Flask, request, redirect, Response
import os
import uuid
from datetime import datetime
from authentication_services import getLoginUrl, getCognitoHost, exchangeCode4Token, getUserInfo, getRedirectURI, getBase64EncodedCredential
from authentication_utils import createResponse, isSessionActive, getSessionToken

app = Flask(__name__)

@app.route('/apis/authentication/login')
def login_url():
    return createResponse(getLoginUrl())


@app.route('/apis/authentication/status')
def login_status():
    if (isSessionActive()):
        return createResponse(json.dumps(session_info))
    print("Session ID: " + getSessionToken())
    return ""


@app.route('/apis/authentication/exchange')
def exchange_code():
    # exchange code for access token
    code = request.args.get("code")
    access_token = exchangeCode4Token(code)

    # retrieve user info, set up session info and redirect
    user_info = getUserInfo(access_token)
    user_info["id"] = str(uuid.uuid4())
    user_info["expirationTime"] = int(datetime.now().timestamp() * 1000 + 15 * 60 * 1000)  # Valid for 15 minutes
    global session_info
    session_info = user_info
    return redirect(login_redirect_url + "?session=" + session_info["id"])


@app.route('/apis/authentication/resource')
def protected_resource():
    print("Session ID: " + getSessionToken())
    if (isSessionActive()):
        return createResponse("Protected Resource Retrieved from DB.")
    return createResponse("", 401)


@app.route('/apis/authentication/logout')
def logout():
    global session_info
    session_info = None
    return createResponse("")


if __name__ == '__main__':
    app.run()
