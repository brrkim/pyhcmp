from interface_actions import Provisioning
from auth_collections import getAuthToken,getQueryStr
from locations import Zone
from infraservices import Cloud
from resources import Services
import requests
import json
import os



class DummyCloud(Cloud):
    def __init__(self,credinfo,cloudname='DummyCloud'):
        super().__init__(
            userid = credinfo['userid'],
            userpw = credinfo['userpw'],
            domain = credinfo['domain'],
            cloudname = cloudname
        )

class CloudZone(Zone):
    def __init__(self,cloud,zone,cloudtype):
        super().__init__(cloud=cloud,zone=zone,cloudtype='public')
        self.headers['X-Auth-Token'] = getAuthToken(self.cloud,self.zone,self.headers)

class Server(Services,Provisioning):
    def __init__(self,cloudzone,servicename,endpoint):
        super().__init__(headers=cloudzone.headers,servicename=servicename,domain=cloudzone.cloud.domain,zone=cloudzone.zone,endpoint=endpoint,apikey=cloudzone.cloud.apikey,secret=cloudzone.cloud.secret)

    def create(self):
        return super().create()

    def read(self):
        url = self.domain+self.zone+self.endpoint
        response = requests.get(url, headers=self.headers).json()
        return response
    
    def update(self):
        return super().update()

    def delete(self):
        return super().delete()
        