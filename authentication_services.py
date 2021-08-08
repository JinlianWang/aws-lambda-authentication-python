import os
from urllib.parse import quote_plus

api_gateway_url = "https://f4y2bwysuc.execute-api.us-east-1.amazonaws.com/dev" if os.environ.get("API_GATEWAY_URL") is None else os.environ.get("API_GATEWAY_URL")
login_redirect_url = "http://athenatestsunny2020.s3-website-us-east-1.amazonaws.com/" if os.environ.get("LOGIN_REDIRECT_URL") is None else os.environ.get("LOGIN_REDIRECT_URL")
cognito_domain_prefix = "sunnyoauth" if os.environ.get("COGNITO_DOMAIN_PREFIX") is None else os.environ.get("COGNITO_DOMAIN_PREFIX")
cognito_app_id = "1vvp0tt53g1uhntoa5bmvnvk2a" if os.environ.get("COGNITO_APP_ID") is None else os.environ.get("COGNITO_APP_ID")
cognito_app_secret = "<secret>" if os.environ.get("COGNITO_APP_SECRET") is None else os.environ.get("COGNITO_APP_SECRET")

def getLoginUrl():
    return getCognitoHost() + "/oauth2/authorize?client_id=" \
                                 + cognito_app_id + "&redirect_uri=" + quote_plus(getRedirectURI()) \
                                 + "&scope=openid&response_type=code"

def exchangeCode4Token(code: str):
    params = {"code": code, "grant_type": "authorization_code", "redirect_uri": getRedirectURI()}
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": getBase64EncodedCredential()}
    data = urlencode(params)
    response = requests.post(getCognitoHost() + "/oauth2/token", data=data, headers=headers)
    return response.json()["access_token"]

def getUserInfo(access_token: str):
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.get(getCognitoHost() + "/oauth2/userInfo", headers=headers)
    return response.json()


def getRedirectURI():
    return api_gateway_url + "/apis/authentication/exchange"


def getBase64EncodedCredential():
    return "Basic " + base64.b64encode((cognito_app_id + ":" + cognito_app_secret).encode("ascii")).decode("ascii")

def getCognitoHost():
    return "https://" + cognito_domain_prefix + ".auth.us-east-1.amazoncognito.com"


