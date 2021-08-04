from app.internal.provider.ktcloud.provider_ktcloud import KTCloud,KTCZone,KTCServer
from app.internal.provider.aws.provider_aws import AWS,AWSZone,AWSServer
from app.models import Provider,Server
import json

def build_provider_resource(provider):
    
    ret = []
    
    if provider['vendor'] == 'ktcloud':
        ktcloud = KTCloud(provider)
        d1_zone = KTCZone(ktcloud,'d1/','public')
        d1_server = KTCServer(d1_zone,'Servers','server/servers')
        g1_zone = KTCZone(ktcloud,'v1/','public')
        g1_server = KTCServer(g1_zone,'Servers','server/')
        g2_zone = KTCZone(ktcloud,'v2/','public')
        g2_server = KTCServer(g2_zone,'Servers','server/')
        ret = [d1_server,g1_server,g2_server]

    elif provider['vendor'] == 'aws':
        aws = AWS(provider)
        seoul_zone = AWSZone(aws,provider['region'],'public')
        seoul_server = AWSServer(seoul_zone,'Servers',None)
        ret = [seoul_server]

    return ret

def discover_brownfields(provider_server):
    all_items = []
    try:
        for server in provider_server:
            all_items += parse_data(server,server.read())
    except Exception as e:
        print(e)
    return all_items

def parse_data(server,response):
    items = []
    clouds = {"KTC":["KT Cloud"],"AWS":["AMAZON AWS"]}
    zones = {"D":["d1/"],"G":["v1/","v2/"]}
    if server.cloudname in clouds["KTC"]:
        if server.zone in zones["D"]:
            for inst in response["servers"]:
                item = Server(
                    tenant_id=inst["tenant_id"],
                    instance_name=inst["name"],
                    instance_id=inst["hostId"],
                    instance_az=inst["OS-EXT-AZ:availability_zone"],
                    instance_flavor_id=inst["flavor"]["id"],
                    instance_key_name=inst["key_name"],
                    instance_status=inst["status"])
                items.append(item)
        elif server.zone in zones["G"]:
            for inst in response["listvirtualmachinesresponse"]["virtualmachine"]:
                item = Server(
                    tenant_id=inst["domainid"],
                    instance_name=inst["name"],
                    instance_id=inst["id"],
                    instance_az=inst["zonename"],
                    instance_flavor_id=inst["templatename"],
                    instance_status=inst["state"])
                items.append(item)
    elif server.cloudname in clouds["AWS"]:
        for reserv in response["Reservations"]:
            for inst in reserv["Instances"]:
                item = Server(
                    tenant_id=reserv["OwnerId"],
                    instance_id=inst["InstanceId"],
                    instance_az=inst["Placement"]["AvailabilityZone"],
                    instance_flavor_id=inst["InstanceType"],
                    instance_key_name=inst["KeyName"],
                    instance_status=inst["State"]["Name"])
                items.append(item)
    return items