import os
from flask import request, Response

cors_allow_origin = "http://athenatestsunny2020.s3-website-us-east-1.amazonaws.com/" if os.environ.get("CORS_ALLOW_ORIGIN") is None else os.environ.get("CORS_ALLOW_ORIGIN")
session_info = None

def createResponse(body: str, status_code: int = 200):
    global cors_allow_origin
    response = Response(body)
    response.headers['Access-Control-Allow-Origin'] = cors_allow_origin
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,POST,GET'
    response.status_code = status_code
    return response

def isSessionActive():
    global session_info
    return (session_info is not None) and \
           (getSessionToken() == session_info["id"]) and \
           (session_info["expirationTime"] > int(datetime.now().timestamp() * 1000))

def getSessionToken():
    auth_header = request.headers.get("Authorization")
    if auth_header is not None:
        auth_parts = auth_header.split(" ")
        if (len(auth_parts) == 2) and (auth_parts[0] == "Bearer"):
            return auth_parts[1]
    return ""