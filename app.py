from flask import Flask, jsonify, redirect
import json
import urllib.parse
from datetime import datetime, timezone, timedelta

app = Flask(__name__)
cognito_app_id = "1vvp0tt53g1uhntoa5bmvnvk2a"
cognito_domain_prefix: str = "sunnyoauth"
api_gateway_url = "https://fp6god49v7.execute-api.us-east-1.amazonaws.com/prod"
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
    return json.dumps({"message": "Exchange for session token!"})


@app.route('/apis/authentication/logout')
def logout():
    global sessionInfo
    sessionInfo = None
    return ""


def getCognitoHost():
    return "https://" + cognito_domain_prefix + ".auth.us-east-1.amazoncognito.com"


def getRedirectURI():
    return api_gateway_url + "/apis/authentication/exchange"


if __name__ == '__main__':
    app.run()
