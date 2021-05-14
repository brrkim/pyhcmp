from Actions import Provisioning
from Supports import make_requeststr
import requests
import json

class Services():
    def __init__(self,servicename,endpoint):
        self.servicename = servicename
        self.endpoint = endpoint

class ServerD(Services,Provisioning):
    def __init__(self,servicename,endpoint,cloud):
        super().__init__(servicename,endpoint)
        self.cloud = cloud

    def create(self):
        return super().create()

    def read(self):
        url = self.cloud.domain+self.cloud.zone+self.endpoint
        response = requests.get(url, headers=self.cloud.headers).json()
        return response
    
    def update(self):
        return super().update()

    def delete(self):
        return super().delete()

class ServerG(Services,Provisioning):
    def __init__(self,servicename,endpoint,cloud,state=None):
        super().__init__(servicename,endpoint)
        self.cloud = cloud
        self.command = None

    def create(self):
        return super().create()

    def read(self):
        self.command = "listVirtualMachines"
        url = self.cloud.domain+self.endpoint+self.cloud.zone+"client/api?"+make_requeststr(self.command,self.cloud.credentials)
        response = requests.get(url).json()
        # if response['response'] and response['response']['errorcode'] == '432':
        #     raise Exception("ERROR: The given command is not supported")
        return response
    
    def update(self):
        return super().update()

    def delete(self):
        return super().delete()
