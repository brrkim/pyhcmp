from Providers import Cloud
import requests
import json
import os

class KTCloudD(Cloud):
    def __init__(self,userid,userpw,domain,zone):
        super().__init__("KT Cloud AI/DX Platform","Public",[userid,userpw])
        self.domain = domain
        self.zone = zone
        self.headers = {
            "Content-Type": "application/json"
        }

    # AuthToken is available only for 1hr
    def getAuthToken(self):
        endpoint = "identity/auth/tokens"
        cwd = os.getcwd()
        with open(cwd+'\\requests_json\\tokens.json',encoding='UTF-8') as json_file:
            body = json.load(json_file)
        body['auth']['identity']['password']['user']['name'] = self.credentials[0]
        body['auth']['identity']['password']['user']['password'] = self.credentials[1]
        body['auth']['scope']['project']['name'] = self.credentials[0]
        response = requests.post(
            self.domain+self.zone+endpoint, headers=self.headers, data=json.dumps(body))
        if response.status_code != 201:
            raise Exception("ERROR: Authentication Fail")
        self.headers['X-Auth-Token'] = response.headers['X-Subject-Token']


class KTCloudG(Cloud):
    def __init__(self,userid,userpw,domain,zone):
        super().__init__("KT Cloud G1/G2 Platform","Public",[userid,userpw])
        self.domain = domain
        self.zone = zone