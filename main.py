import os
import json
from provider_ktcloud import KTCloud,CloudZone,Server

def main():
    cwd = os.getcwd()
    with open(cwd+'/requests_json/credentials.json',encoding='UTF-8') as credentials:
        credinfo = json.load(credentials)

    ktcloud = KTCloud(credinfo)

    try:
        d1_zone = CloudZone(ktcloud,'d1/','public')
        d1_server = Server(d1_zone,'Server','server/servers/')
        print(d1_server.read())

        g1_zone = CloudZone(ktcloud,'v1/','public')
        g1_server = Server(g1_zone,'Server','server/')
        print(g1_server.read())
        
        g2_zone = CloudZone(ktcloud,'v2/','public')
        g2_server = Server(g2_zone,'Server','server/')
        print(g2_server.read())

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
