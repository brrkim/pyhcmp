from interface_actions import Provisioning
from auth_collections import getAuthToken,getQueryStr
from locations import Zone
from infraservices import Cloud
from resources import Services
import boto3


class AWS(Cloud):
    def __init__(self,credinfo,cloudname='AMAZON AWS'):
        super().__init__(
            apikey=credinfo['apikey'],
            secret=credinfo['secret'],
            region=credinfo['region'],
            cloudname=cloudname
        )

class AWSZone(Zone):
    def __init__(self,cloud,zone,cloudtype):
        super().__init__(cloud=cloud,zone=zone,cloudtype='public')

class AWSServer(Services,Provisioning):
    def __init__(self,cloudzone,servicename,endpoint):
        super().__init__(cloudname=cloudzone.cloud.cloudname,headers=cloudzone.headers,servicename=servicename,domain=cloudzone.cloud.domain,zone=cloudzone.zone,endpoint=endpoint,apikey=cloudzone.cloud.apikey,secret=cloudzone.cloud.secret)
        self.client = boto3.client('ec2',aws_access_key_id=self.apikey,aws_secret_access_key=self.secret,region_name=self.zone)
        # self.ec2 = boto3.resource('ec2',aws_access_key_id=self.apikey,aws_secret_access_key=self.secret,region_name=self.zone)
        
    # def create(self):
    #     response = self.ec2.create_instances(
    #         ImageId='ami-0f2c95e9fe3f8f80e',
    #         InstanceType='t2.micro',
    #         MinCount=1,
    #         MaxCount=1,
    #         KeyName='bamboo'
    #     )
    #     return response

    def create(self,**kwargs):
        response = self.client.run_instances(
            ImageId='ami-0f2c95e9fe3f8f80e',
            InstanceType='t2.micro',
            MinCount=1,
            MaxCount=1,
            KeyName='testkey',
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'kgh-ec2'
                        },
                    ]
                },
            ]
        )
        return response

    
    def read(self):
        response = self.client.describe_instances()
        return response
    
    def update(self):
        return super().update()

    def delete(self):
        return super().delete()
        