

class Services():
    def __init__(self,headers,servicename,domain,zone,endpoint,apikey,secret):
        self.headers = headers
        self.servicename = servicename
        self.domain = domain
        self.zone = zone
        self.endpoint = endpoint
        self.apikey = apikey
        self.secret = secret