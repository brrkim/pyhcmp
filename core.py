from provider_ktcloud import KTCloud,KTCZone,KTCServer
from provider_aws import AWS,AWSZone,AWSServer
import json
from pydantic import BaseModel

all_items = []

def sync():
    global all_items    
    with open('credentials_json/credentials_ktcloud.json',encoding='UTF-8') as credentials:
        credinfo_kt = json.load(credentials)
    ktcloud = KTCloud(credinfo_kt)

    with open('credentials_json/credentials_aws.json',encoding='UTF-8') as credentials:
        credinfo_aws = json.load(credentials)
    aws = AWS(credinfo_aws)
    
    try:
        d1_zone = KTCZone(ktcloud,'/d1','public')
        d1_server = KTCServer(d1_zone,'Servers','/server/servers')
        
        g1_zone = KTCZone(ktcloud,'/v1','public')
        g1_server = KTCServer(g1_zone,'Servers','/server')

        g2_zone = KTCZone(ktcloud,'/v2','public')
        g2_server = KTCServer(g2_zone,'Servers','/server')

        seoul_zone = AWSZone(aws,credinfo_aws['region'],'public')
        seoul_server = AWSServer(seoul_zone,'Servers',None)
                
        # # 2x2 | KOR-Central A | CentOS 7.6
        # print(g1_server.create(
        #     name="pyhcmp-g1-test2",
        #     serviceofferingid="672cf914-069b-4abc-85cc-0db3155fe001",
        #     zoneid="eceb5d65-6571-4696-875f-5a17949f3317",
        #     templateid="2835a73c-f276-469c-b874-d75a7abca85b"))
        
        # # 1x1.itl | DMZ | CentOS 7.6
        # print(d1_server.create(
        #     name="pyhcmp-dx1-test",
        #     key_name="js-test",
        #     flavorRef="f9764e6b-1b46-421d-8998-816c2d8d13ce",
        #     networks_uuid="acaa8f70-f1cd-41b3-a38a-852256ef6f1d",
        #     block_device_uuid="fa8fdef3-fb2c-43fd-ad38-de858c39a53a"))
        
        # t2.micro | Default VPC | Amazon Linux
        # print(seoul_server.create(
        #     TagsKey='Name',
        #     TagsValue='kgk-ec2',
        #     KeyName='testkey',
        #     InstanceType='t2.micro',
        #     ImageId='ami-0f2c95e9fe3f8f80e'))
        
        # for server in [d1_server,g1_server,g2_server,seoul_server]:
            # print("##### {0} {1} {2} ######".format(server.cloudname,server.zone,server.servicename))
            # print(json.dumps(server.read(),default=str))
            # print()
        
        # print(seoul_server.delete(InstanceIds='i-016fcd22041008893'))
        # print(g1_server.stop(id='dac1a443-62d3-4ac2-89a2-807d1946e81c'))
        # print(g1_server.delete(id='dac1a443-62d3-4ac2-89a2-807d1946e81c'))
    
        for server in [d1_server,g1_server,g2_server,seoul_server]:
            parse_data(server,server.read())
                
        
    except Exception as e:
        print(e)
        
    return all_items

class Item(BaseModel):
    tenant_id: str
    instance_name: str = None
    instance_id: str
    instance_addresses: str = None
    instance_az: str
    instance_flavor_id: str
    instance_os_image_id: str = None
    instance_key_name: str = None
    instance_status: str

def parse_data(server,response):
    global all_items
    clouds = {"KTC":["KT Cloud"],"AWS":["AMAZON AWS"]}
    zones = {"D":["/d1"],"G":["/v1","/v2"]}
    if server.cloudname in clouds["KTC"]:
        if server.zone in zones["D"]:
            for inst in response["servers"]:
                item = Item(
                    tenant_id=inst["tenant_id"],
                    instance_name=inst["name"],
                    instance_id=inst["hostId"],
                    instance_az=inst["OS-EXT-AZ:availability_zone"],
                    instance_flavor_id=inst["flavor"]["id"],
                    instance_key_name=inst["key_name"],
                    instance_status=inst["status"])
                all_items.append(item)
        elif server.zone in zones["G"]:
            for inst in response["listvirtualmachinesresponse"]["virtualmachine"]:
                item = Item(
                    tenant_id=inst["domainid"],
                    instance_name=inst["name"],
                    instance_id=inst["id"],
                    instance_az=inst["zonename"],
                    instance_flavor_id=inst["templatename"],
                    instance_status=inst["state"])
                all_items.append(item)
    elif server.cloudname in clouds["AWS"]:
        for reserv in response["Reservations"]:
            for inst in reserv["Instances"]:
                item = Item(
                    tenant_id=reserv["OwnerId"],
                    instance_id=inst["InstanceId"],
                    instance_az=inst["Placement"]["AvailabilityZone"],
                    instance_flavor_id=inst["InstanceType"],
                    instance_key_name=inst["KeyName"],
                    instance_status=inst["State"]["Name"])
                all_items.append(item)