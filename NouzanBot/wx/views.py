from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .wx import check_signature, query_str2dict


@csrf_exempt
def handle(request):
    if request.method == 'GET':
        data = request.GET
        if len(data) == 0:
            return HttpResponse("Hello, this is NouzanBot's handle. ")
        signature = data.get('signature')
        timestamp = data.get('timestamp')
        nonce = data.get('nonce')
        echostr = data.get('echostr')
        if check_signature(signature, timestamp, nonce):
            return HttpResponse(echostr)
        else:
            return HttpResponse("")
    elif request.method == 'POST':
        msg_xml = request.body
        query_str = request.environ.get('QUERY_STRING')
        query_dict = query_str2dict(query_str)
        print(msg_xml)
        print(query_dict)
        signature = request.query_dict.get('signature')
        timestamp = request.query_dict.get('timestamp')
        nonce = request.query_dict.get('nonce')
        print(request.environ)
        if check_signature(signature, timestamp, nonce):
            return HttpResponse("success")
        else:
            return HttpResponse("")
