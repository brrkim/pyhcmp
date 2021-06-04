from interface_actions import Provisioning
from auth_collections import getAuthToken,getQueryStr
from locations import Zone
from infraservices import Cloud
from resources import Services
import requests

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