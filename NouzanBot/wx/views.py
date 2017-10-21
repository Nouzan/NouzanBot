from django.shortcuts import render
from django.http import HttpResponse
import hashlib


def handle(request):
    data = request.GET
    if len(data) == 0:
        return HttpResponse("Hello, this is NouzanBot's handle. ")
    signature = data.get('signature')
    timestamp = data.get('timestamp')
    nonce = data.get('nonce')
    echostr = data.get('echostr')
    token = 'nouzan414'

    info = [token, timestamp, nonce]
    info.sort()
    s = bytes(info[0] + info[1] + info[2], encoding='utf8')
    hashcode = hashlib.sha1(s).hexdigest()
    print("handle/GET func: hashcode, signature: ", hashcode, signature)
    if hashcode == signature:
        return HttpResponse(echostr)
    else:
        return HttpResponse("")
