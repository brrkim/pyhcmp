import os
import json
from KTCloud import KTCloudD, KTCloudG
from Driver import RestfulAPI
from InfraServices import ServerD, ServerG

cwd = os.getcwd()
with open(cwd+'\\requests_json\\credentials.json',encoding='UTF-8') as credentials:
    credinfo = json.load(credentials)

ktc_d1 = KTCloudD(userid=credinfo['userid'],userpw=credinfo['userpw'],domain=credinfo['domain'],zone="d1/")
ktc_g1 = KTCloudG(userid=credinfo['apikey'],userpw=credinfo['secret'],domain=credinfo['domain'],zone="v1/")
ktc_g2 = KTCloudG(userid=credinfo['apikey'],userpw=credinfo['secret'],domain=credinfo['domain'],zone="v2/")

try:
    ktc_d1.getAuthToken()
    ktc_d1_server = ServerD(servicename="Server",endpoint="server/servers/",cloud=ktc_d1)
    print(ktc_d1_server.read())
    ktc_g1_server = ServerG(servicename="Server",endpoint="server/",cloud=ktc_g1)
    print(ktc_g1_server.read())
    ktc_g2_server = ServerG(servicename="Server",endpoint="server/",cloud=ktc_g2)
    print(ktc_g2_server.read())
except Exception as e:
    print(e)