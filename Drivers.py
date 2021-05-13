from abc import *
import requests
import json

class OpenAPI():
    def __init__(self,url,credentials):
        self.url = url
        self.credentials = credentials

class RestfulAPI():
    def __init__(self,url,credentials):
        self.url = url
        self.credentials = credentials

class gRPC():
    pass

class JsonRPC():
    pass

class SDK():
    def __init__(self):
        pass

class CDK():
    def __init__(self):
        pass