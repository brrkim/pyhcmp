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
    endpoint = "identity/auth/tokens"
    cwd = os.getcwd()
    with open(cwd+'/requests_json/tokens.json',encoding='UTF-8') as json_file:
        body = json.load(json_file)
    body['auth']['identity']['password']['user']['name'] = cloud.userid
    body['auth']['identity']['password']['user']['password'] = cloud.userpw
    body['auth']['scope']['project']['name'] = cloud.userid
    response = requests.post(
        cloud.domain+zone+endpoint, headers=headers, data=json.dumps(body))
    if response.status_code != 201:
        raise Exception("Error: Authentication Fail")
    return response.headers['X-Subject-Token']

# %%
# dic = {"error":{"code":401,"message":"The request you have made requires authentication","title":"Unauthorized"}}

# %%

# G1/G2 Make Query Strings
def getQueryStr(command,apikey,secret):
    # request 문자열 생성
    params=dict()
    params['command']=command
    params['response']="json"
    params['apikey']=apikey
    secret=secret.encode('utf-8')
    requeststr = '&'.join(['='.join([k,urllib.parse.quote_plus(params[k])]) for k in params.keys()])
    # signature 생성
    message = '&'.join(['='.join([k.lower(),urllib.parse.quote_plus(params[k]).replace('+','%20').lower()]) for k in sorted(params.keys())])
    message = message.encode('utf-8')
    digest = hmac.new(secret, msg=message, digestmod=hashlib.sha1).digest()
    signature = base64.b64encode(digest)
    signature = urllib.parse.quote_plus(signature)
    requeststr += '&signature='+signature
    return requeststr
