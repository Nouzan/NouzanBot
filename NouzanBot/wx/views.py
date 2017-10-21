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
    token = "nouzan414"

    info = [token, timestamp, nonce]
    info.sort()
    sha1 = hashlib.sha1()
    map(sha1.update, info)
    hashcode = sha1.hexdigest()
    print("handle/GET func: hashcode, signature: ", hashcode, signature)
    if hashcode == signature:
        return HttpResponse(chostr)
    else:
        return HttpResponse("")
