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
        d1_server = KTCServer(d1_zone,'KTC D1 Servers','server/servers/')
        
        g1_zone = KTCZone(ktcloud,'v1/','public')
        g1_server = KTCServer(g1_zone,'KTC G1 Servers','server/')

        g2_zone = KTCZone(ktcloud,'v2/','public')
        g2_server = KTCServer(g2_zone,'KTC G2 Servers','server/')

        seoul_zone = AWSZone(aws,credinfo_aws['region'],'public')
        seoul_server = AWSServer(seoul_zone,'AWS SEOUL Instances',None)
                
        for server in [d1_server,g1_server,g2_server,seoul_server]:
            print("##### "+server.servicename+" #####")
            print(server.read())
            print()
        
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()