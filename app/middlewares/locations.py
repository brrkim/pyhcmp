

class Zone():
    def __init__(self,cloud,zone,cloudtype):
        self.cloud = cloud
        self.zone = zone
        self.cloudtype = cloudtype
        self.headers = {
            "Content-Type": "application/json"
        }