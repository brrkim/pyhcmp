import hashlib
import hmac
import base64
import urllib

def make_requeststr(command,credentials):
    # request 문자열 생성
    params=dict()
    params['command']=command
    params['response']="json"
    params['apikey']=credentials[0]
    secretkey=credentials[1].encode('utf-8')
    requeststr = '&'.join(['='.join([k,urllib.parse.quote_plus(params[k])]) for k in params.keys()])
    # signature 생성
    message = '&'.join(['='.join([k.lower(),urllib.parse.quote_plus(params[k]).replace('+','%20').lower()]) for k in sorted(params.keys())])
    message = message.encode('utf-8')
    digest = hmac.new(secretkey, msg=message, digestmod=hashlib.sha1).digest()
    signature = base64.b64encode(digest)
    signature = urllib.parse.quote_plus(signature)
    requeststr += '&signature='+signature

    return requeststr