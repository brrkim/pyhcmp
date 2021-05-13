### This is test script of getAuthToken from KT Cloud DX Zone ###
import requests
import json
import os

endpoint = "identity/auth/tokens"
userid = "test"
userpw = "pass"

cwd = os.getcwd()

with open(cwd+'\\requests_json\\tokens.json',encoding='UTF-8') as json_file:
    body = json.load(json_file)
body['auth']['identity']['password']['user']['name'] = userid
body['auth']['identity']['password']['user']['password'] = userpw
body['auth']['scope']['project']['name'] = userid

headers = {
    "Content-Type": "application/json"
}

response = requests.post(
    "https://api.ucloudbiz.olleh.com/"+"d1/"+endpoint, headers=headers, data=json.dumps(body))

print(response.headers)
print(response.status_code)