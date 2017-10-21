from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .wx import check_signature


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
        data = request.body
        print(data)
        signature = request.POST.get('signature')
        timestamp = request.POST.get('timestamp')
        nonce = request.POST.get('nonce')
        if check_signature(signature, timestamp, nonce):
            return HttpResponse("success")
        else:
            return HttpResponse("")
