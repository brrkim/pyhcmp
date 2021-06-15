import json
from provider_ktcloud import KTCloud,KTCZone,KTCServer
from provider_aws import AWS,AWSZone,AWSServer

def main():    
    with open('credentials_json/credentials_ktcloud.json',encoding='UTF-8') as credentials:
        credinfo_kt = json.load(credentials)
    ktcloud = KTCloud(credinfo_kt)

    with open('credentials_json/credentials_aws.json',encoding='UTF-8') as credentials:
        credinfo_aws = json.load(credentials)
    aws = AWS(credinfo_aws)

    try:
        d1_zone = KTCZone(ktcloud,'d1/','public')
        d1_server = KTCServer(d1_zone,'Servers','server/servers')
        
        g1_zone = KTCZone(ktcloud,'v1/','public')
        g1_server = KTCServer(g1_zone,'Servers','server/')

        g2_zone = KTCZone(ktcloud,'v2/','public')
        g2_server = KTCServer(g2_zone,'Servers','server/')

        seoul_zone = AWSZone(aws,credinfo_aws['region'],'public')
        seoul_server = AWSServer(seoul_zone,'Servers',None)
                
        # 2x2 | KOR-Central A | CentOS 7.6
        print(g1_server.create(
            name="pyhcmp-g1-test2",
            serviceofferingid="672cf914-069b-4abc-85cc-0db3155fe001",
            zoneid="eceb5d65-6571-4696-875f-5a17949f3317",
            templateid="2835a73c-f276-469c-b874-d75a7abca85b"))
        
        # 1x1.itl | DMZ | CentOS 7.6
        # print(d1_server.create(
        #     name="pyhcmp-dx1-test",
        #     key_name="js-test",
        #     flavorRef="f9764e6b-1b46-421d-8998-816c2d8d13ce",
        #     networks_uuid="acaa8f70-f1cd-41b3-a38a-852256ef6f1d",
        #     block_device_uuid="fa8fdef3-fb2c-43fd-ad38-de858c39a53a"))
        
        
        for server in [d1_server,g1_server,g2_server,seoul_server]:
            print("##### {0} {1} {2} ######".format(server.cloudname,server.zone,server.servicename))
            print(server.read())
            print()
        
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()