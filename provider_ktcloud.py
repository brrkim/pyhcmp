from interface_actions import Provisioning,Management
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
    def __init__(self,cloud,zone,cloudtype='public'):
        super().__init__(cloud=cloud,zone=zone,cloudtype=cloudtype)
        if zone in zones['D']:
            self.headers['X-Auth-Token'] = getAuthToken(self.cloud,self.zone,self.headers)

class KTCServer(Services,Provisioning,Management):
    def __init__(self,cloudzone,servicename,endpoint):
        super().__init__(cloudname=cloudzone.cloud.cloudname,headers=cloudzone.headers,servicename=servicename,domain=cloudzone.cloud.domain,zone=cloudzone.zone,endpoint=endpoint,apikey=cloudzone.cloud.apikey,secret=cloudzone.cloud.secret)

    def create(self,**kwargs):
        # D1 Zone
        if self.zone in zones['D']:            
            cwd = os.getcwd()
            with open(cwd+'/requests_json/servers.json',encoding='UTF-8') as json_file:
                body = json.load(json_file)
            body['server']['name'] = kwargs['name']
            body['server']['key_name'] = kwargs['key_name']
            body['server']['flavorRef'] = kwargs['flavorRef']
            body['server']['networks'][0]['uuid'] = kwargs['networks_uuid']
            body['server']['block_device_mapping_v2'][0]['uuid'] = kwargs['block_device_uuid']
            url = self.domain+self.zone+self.endpoint
            response = requests.post(url, headers=self.headers, data=json.dumps(body)).json()
            
        # G1/G2 Zone
        elif self.zone in zones['G']:
            kwargs['command'] = "deployVirtualMachine"
            kwargs['response'] = "json"
            kwargs['displayname'] = kwargs['name']
            kwargs['apikey'] = self.apikey
            url = self.domain+self.endpoint+self.zone+"client/api?"+getQueryStr(self.secret,kwargs)
            response = requests.get(url).json()
        return response

    def read(self,**kwargs):
        # D1 Zone
        if self.zone in zones['D']:
            url = self.domain+self.zone+self.endpoint+"/detail"
            response = requests.get(url, headers=self.headers).json()

        # G1/G2 Zones
        elif self.zone in zones['G']:
            kwargs['command'] = "listVirtualMachines"
            kwargs['response'] = "json"
            kwargs['apikey'] = self.apikey
            url = self.domain+self.endpoint+self.zone+"client/api?"+getQueryStr(self.secret,kwargs)
            response = requests.get(url).json()
        return response

    def update(self,**kwargs):
        return super().update()

    def delete(self,**kwargs):
        # D1 Zone
        if self.zone in zones['D']:
            # url = self.domain+self.zone+self.endpoint+"/detail"
            # response = requests.get(url, headers=self.headers).json()
            pass

        # G1/G2 Zones
        elif self.zone in zones['G']:
            kwargs['command'] = "destroyVirtualMachine"
            kwargs['response'] = "json"
            kwargs['apikey'] = self.apikey
            url = self.domain+self.endpoint+self.zone+"client/api?"+getQueryStr(self.secret,kwargs)
            response = requests.get(url).json()
        return response
    
    def start(self, **kwargs):
        return super().start(**kwargs)
    
    def stop(self, **kwargs):
        # D1 Zone
        if self.zone in zones['D']:
            # url = self.domain+self.zone+self.endpoint+"/detail"
            # response = requests.get(url, headers=self.headers).json()
            pass

        # G1/G2 Zones
        elif self.zone in zones['G']:
            kwargs['command'] = "stopVirtualMachine"
            kwargs['response'] = "json"
            kwargs['apikey'] = self.apikey
            url = self.domain+self.endpoint+self.zone+"client/api?"+getQueryStr(self.secret,kwargs)
            response = requests.get(url).json()
        return response
    
    def restart(self, **kwargs):
        return super().restart(**kwargs)