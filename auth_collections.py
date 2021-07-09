import hashlib
import hmac
import base64
import urllib
import os
import requests
import json

# D1 Get Auth Token
# AuthToken is available only for 1hr
def getAuthToken(cloud,zone,headers):
    endpoint = "/identity/auth/tokens"
    with open('jsons/requests/tokens.json',encoding='UTF-8') as json_file:
        body = json.load(json_file)
    body['auth']['identity']['password']['user']['name'] = cloud.userid
    body['auth']['identity']['password']['user']['password'] = cloud.userpw
    body['auth']['scope']['project']['name'] = cloud.userid
    response = requests.post(
        cloud.domain+zone+endpoint, headers=headers, data=json.dumps(body))
    if response.status_code != 201:
        raise Exception("Error: Authentication Fail")
    
    return response.headers['X-Subject-Token']

# G1/G2 Make Query Strings
def getQueryStr(secret,params):
    # Query Strings 생성
    secret = secret.encode('utf-8')
    querystr = '&'.join(['='.join([k,urllib.parse.quote_plus(params[k]).replace('+','%20')]) for k in sorted(params.keys(), key=str.lower)])
    
    # Signature 생성
    digest = hmac.new(secret, msg=querystr.encode('utf-8').lower(), digestmod=hashlib.sha1).digest()
    signature = urllib.parse.quote_plus(base64.b64encode(digest))
    
    # Final
    querystr += '&signature='+signature
    
    return querystr