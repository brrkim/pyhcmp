class Cloud():
    def __init__(self,credinfo,cloudname):
        self.apikey = credinfo['apikey']
        self.secret = credinfo['secret']
        self.userid = credinfo['userid']
        self.userpw = credinfo['userpw']
        self.domain = credinfo['domain']
        self.cloudname = cloudname

class Network():
    pass

class IDC():
    pass