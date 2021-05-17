from interface_actions import Provisioning
from auth_collections import getAuthToken,getQueryStr
from locations import Zone
from infraservices import Cloud
from resources import Services
import requests
import json
import os
import boto3


class AWS(Cloud):
    def __init__(self,credinfo,cloudname='AMAZON AWS'):
        super().__init__(
            apikey=credinfo['apikey'],
            secret=credinfo['secret'],
            cloudname=cloudname
        )

class AWSZone(Zone):
    def __init__(self,cloud,zone,cloudtype):
        super().__init__(cloud=cloud,zone=zone,cloudtype='public')

class AWSServer(Services,Provisioning):
    def __init__(self,cloudzone,servicename,endpoint):
        super().__init__(headers=cloudzone.headers,servicename=servicename,domain=cloudzone.cloud.domain,zone=cloudzone.zone,endpoint=endpoint,apikey=cloudzone.cloud.apikey,secret=cloudzone.cloud.secret)
        self.client = boto3.client(
            'ec2',
            aws_access_key_id=self.apikey,
            aws_secret_access_key=self.secret
        )
        
    def create(self):
        return super().create()

    def read(self):
        response = self.client.describe_instances()
        return response
    
    def update(self):
        return super().update()

    def delete(self):
        return super().delete()
        