from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, UserProfileSerializer
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import number
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.http.response import JsonResponse
import urllib, hashlib # gravatar library
import json
import time
from .models import User
import hashlib
import hmac
import base64
import requests
import time, json
import random


@api_view(['POST'])
def signup(request):
	#1-1. Client에서 온 데이터를 받아서
    password = request.data.get('password')
    password_confirmation = request.data.get('passwordConfirmation')
	#1-2. 패스워드 일치 여부 체크
    if password != password_confirmation:
        return Response({'error': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
		
	#2. UserSerializer를 통해 데이터 직렬화
    serializer = UserSerializer(data=request.data)
    
	#3. validation 작업 진행 -> password도 같이 직렬화 진행
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        #4. 비밀번호 해싱 후 
        user.set_password(request.data.get('password'))
        user.save()
        # print(user.password)
    # password는 직렬화 과정에는 포함 되지만 → 표현(response)할 때는 나타나지 않는다.
    return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['get'])
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes([IsAuthenticated])
def profile(request, username):    
    person = get_object_or_404(get_user_model(), username=username)
    print('휴대폰', person.phone)
    context ={
        'username': person.username,
        'email': person.email,
        'money': person.money,
        'phone': person.phone,
    }
    return JsonResponse(context)
 

@api_view(['POST'])
def confirm(request):
    phone = request.data.get('phone')
    timestamp = int(time.time() *1000)
    timestamp = str(timestamp)

    url = "https://sens.apigw.ntruss.com"
    requestUrl = "/sms/v2/services/"
    requestUrl2 = "/messages"
    serviceId = 'ncp:sms:kr:275688994599:mvti'
    access_key = 'F5PkIYQwl6xBnFYFvQ7t'

    uri = requestUrl + serviceId + requestUrl2
    apiUrl = url + uri

    def make_signature(uri, access_key):
        secret_key = 'NUFYJ36MJOnLtAUboiaJGg5FCrAdQTPSuPwr3L8s'
        secret_key = bytes(secret_key, 'UTF-8')
        method = 'POST'
        message = method + " " + uri + '\n' + timestamp + '\n' + access_key
        message = bytes(message, 'UTF-8')
        signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
        return signingKey

    auth_number = random.randint(1000, 10000)
    
    number(
        num = auth_number,
    ).save()
    messages = { "to" : f"{phone}"}
    body = {
        "type" : 'SMS',
        'contentType' : 'COMM',
        'from': '01027781007',
        'subject' : 'subject',
        'content' : '인증번호 [{}]를 입력해주세요.'.format(auth_number),
        "messages" : [messages]
    }

    body2 = json.dumps(body)
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': access_key,
        'x-ncp-apigw-signature-v2': make_signature(uri, access_key)
    }

    res = requests.post(apiUrl, headers=headers, data=body2)

    res.request
    res.status_code
    res.raise_for_status()

    print(res.json())

@api_view(['POST'])
def confirm_num(request):
    num = number.objects.all().order_by('-pk')[:1][0].num
    numbers = request.data.get('numbers')
    print(num, numbers)
    if int(numbers) == int(num):
        return Response({'인증되었습니다.'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'인증번호가 잘못 입력되었습니다.'}, status=status.HTTP_201_CREATED)
