from interface_actions import Provisioning
from auth_collections import getAuthToken,getQueryStr
from locations import Zone
from infraservices import Cloud
from resources import Services
import requests
import json
import os

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
    def __init__(self,ktcloud,zone,cloudtype):
        super().__init__(cloud=ktcloud,zone=zone,cloudtype='public')
        if zone in zones['D']:
            self.headers['X-Auth-Token'] = getAuthToken(self.cloud,self.zone,self.headers)

class KTCServer(Services,Provisioning):
    def __init__(self,ktcloudzone,servicename,endpoint):
        super().__init__(headers=ktcloudzone.headers,servicename=servicename,domain=ktcloudzone.cloud.domain,zone=ktcloudzone.zone,endpoint=endpoint,apikey=ktcloudzone.cloud.apikey,secret=ktcloudzone.cloud.secret)

    def create(self):
        return super().create()

    def read(self):
        # D1 Zone
        if self.zone in zones['D']:
            url = self.domain+self.zone+self.endpoint
            response = requests.get(url, headers=self.headers).json()

        # G1/G2 Zones
        elif self.zone in zones['G']:
            command = "listVirtualMachines"
            url = self.domain+self.endpoint+self.zone+"client/api?"+getQueryStr(command,self.apikey,self.secret)
            response = requests.get(url).json()
        return response

    def update(self):
        return super().update()

    def delete(self):
        return super().delete()