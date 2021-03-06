from app.internal.provider.common.interface_actions import Provisioning,Management
from app.internal.provider.common.locations import Zone
from app.internal.provider.common.infraservices import Cloud
from app.internal.provider.common.resources import Services
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

class AWSServer(Services,Provisioning,Management):
    def __init__(self,cloudzone,servicename,endpoint):
        super().__init__(cloudname=cloudzone.cloud.cloudname,headers=cloudzone.headers,servicename=servicename,domain=cloudzone.cloud.domain,zone=cloudzone.zone,endpoint=endpoint,apikey=cloudzone.cloud.apikey,secret=cloudzone.cloud.secret)
        self.client = boto3.client('ec2',aws_access_key_id=self.apikey,aws_secret_access_key=self.secret,region_name=self.zone)

    def create(self,**kwargs):
        response = self.client.run_instances(
            ImageId=kwargs['ImageId'],
            InstanceType=kwargs['InstanceType'],   
            MinCount=1,
            MaxCount=1,
            KeyName=kwargs['KeyName'],
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': kwargs['TagsKey'],
                            'Value': kwargs['TagsValue']
                        },
                    ]
                },
            ]
        )
        return response
    
    def read(self,**kwargs):
        response = self.client.describe_instances()
        return response
    
    def update(self,**kwargs):
        return super().update(**kwargs)

    def delete(self,**kwargs):
        response = self.client.terminate_instances(
            InstanceIds=[
                kwargs['InstanceIds'],
            ],
            DryRun=True
        )
        return response
    
    def start(self, **kwargs):
        return super().start(**kwargs)
    
    def stop(self, **kwargs):
        return super().stop(**kwargs)
    
    def restart(self, **kwargs):
        return super().restart(**kwargs)
        