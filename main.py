import os
import json
from provider_ktcloud import KTCloud,KTCZone,KTCServer
from provider_aws import AWS,AWSZone,AWSServer

def main():
    cwd = os.getcwd()
    
    with open(cwd+'/requests_json/credentials_ktcloud.json',encoding='UTF-8') as credentials:
        credinfo_kt = json.load(credentials)
    ktcloud = KTCloud(credinfo_kt)

    with open(cwd+'/requests_json/credentials_aws.json',encoding='UTF-8') as credentials:
        credinfo_aws = json.load(credentials)
    aws = AWS(credinfo_aws)

    try:
        d1_zone = KTCZone(ktcloud,'d1/','public')
        d1_server = KTCServer(d1_zone,'Servers','server/servers/detail')
        
        g1_zone = KTCZone(ktcloud,'v1/','public')
        g1_server = KTCServer(g1_zone,'Servers','server/')

        g2_zone = KTCZone(ktcloud,'v2/','public')
        g2_server = KTCServer(g2_zone,'Servers','server/')

        seoul_zone = AWSZone(aws,credinfo_aws['region'],'public')
        seoul_server = AWSServer(seoul_zone,'Servers',None)
                
        # for server in [d1_server,g1_server,g2_server,seoul_server]:
        #     print("##### {0} {1} {2} ######".format(server.cloudname,server.zone,server.servicename))
        #     print(server.read())
        #     print()
        
        # g1_server.create()
        print(d1_server.create())
        
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()