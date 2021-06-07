from interface_actions import Provisioning
from auth_collections import getAuthToken,getQueryStr
from locations import Zone
from infraservices import Cloud
from resources import Services
import requests
import os
import json

zones = {'D':['d1/'],'G':['v1/','v2/']}

class KTCloud(Cloud):
    def __init__(self,credinfo,cloudname='KT Cloud'):
        super().__init__(
            apikey = credinfo['apikey'],
            secret = credinfo['secret'],
            userid = credinfo['userid'],
            userpw = credinfo['userpw'],
            domain = credinfo['domain'],
            cloudname = cloudname
        )

class KTCZone(Zone):
    def __init__(self,cloud,zone,cloudtype):
        super().__init__(cloud=cloud,zone=zone,cloudtype='public')
        if zone in zones['D']:
            self.headers['X-Auth-Token'] = getAuthToken(self.cloud,self.zone,self.headers)

class KTCServer(Services,Provisioning):
    def __init__(self,cloudzone,servicename,endpoint):
        super().__init__(cloudname=cloudzone.cloud.cloudname,headers=cloudzone.headers,servicename=servicename,domain=cloudzone.cloud.domain,zone=cloudzone.zone,endpoint=endpoint,apikey=cloudzone.cloud.apikey,secret=cloudzone.cloud.secret)

    def create(self,**kwargs):
        # D1 Zone
        if self.zone in zones['D']:            
            kwargs['name'] = "pyhcmp-dx1-test"
            kwargs['key_name'] = "js-test"
            kwargs['flavorRef'] = "2192ea6d-235a-4b06-b620-3d7a1fe92693"
            kwargs['availability_zone'] = "DX-M1"
            kwargs['networks.uuid'] = "acaa8f70-f1cd-41b3-a38a-852256ef6f1d"
            kwargs['block_device_mapping_v2.destination_type'] = "volume"
            kwargs['block_device_mapping_v2.boot_index'] = "0"
            kwargs['block_device_mapping_v2.source_type'] = "image"
            kwargs['block_device_mapping_v2.volume_size'] = 50
            kwargs['block_device_mapping_v2.uuid'] = "fa8fdef3-fb2c-43fd-ad38-de858c39a53a"
            cwd = os.getcwd()
            with open(cwd+'/requests_json/servers.json',encoding='UTF-8') as json_file:
                body = json.load(json_file)
            body['server']['name'] = kwargs['name']
            body['server']['key_name'] = kwargs['key_name']
            url = self.domain+self.zone+self.endpoint
            response = requests.post(url, headers=self.headers, data=json.dumps(body))
            
        # G1/G2 Zone
        elif self.zone in zones['G']:
            kwargs['command'] = "deployVirtualMachine"
            kwargs['response'] = "json"
            kwargs['zoneid'] = "eceb5d65-6571-4696-875f-5a17949f3317"            # KOR-Central A
            kwargs['serviceofferingid'] = "672cf914-069b-4abc-85cc-0db3155fe001" # 2 vCore X 2GB
            kwargs['templateid'] = "2835a73c-f276-469c-b874-d75a7abca85b"        # CentOS 7.6
            kwargs['name'] = "pyhcmp-g1-test"
            kwargs['displayname'] = "pyhcmp-g1-test"
            kwargs['apikey'] = self.apikey
            url = self.domain+self.endpoint+self.zone+"client/api?"+getQueryStr(self.secret,kargs)
            response = requests.get(url).json()
        return response

    def read(self,**kwargs):
        # D1 Zone
        if self.zone in zones['D']:
            url = self.domain+self.zone+self.endpoint
            response = requests.get(url, headers=self.headers).json()

        # G1/G2 Zones
        elif self.zone in zones['G']:
            kwargs['command'] = "listVirtualMachines"
            kwargs['response'] = "json"
            kwargs['apikey'] = self.apikey
            url = self.domain+self.endpoint+self.zone+"client/api?"+getQueryStr(self.secret,kwargs)
            response = requests.get(url).json()
        return response

    def update(self):
        return super().update()

    def delete(self):
        return super().delete()