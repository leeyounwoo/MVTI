from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, UserProfileSerializer

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.http.response import JsonResponse
import urllib, hashlib # gravatar library
import json
import time
from .models import User

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
 

# class SMSVerificationView(View):
#   def send_verification(self, phone_number, verification_number):
#     AUTH_SECRET_KEY = 'NUFYJ36MJOnLtAUboiaJGg5FCrAdQTPSuPwr3L8s'
#     AUTH_ACCESS_KEY = 'F5PkIYQwl6xBnFYFvQ7t'
#     # 네이버 클라우드 플랫폼에 가입하면 발급해주는 serviceId를 입력해서 sms를 보내는 주소를 완성해준다.
#     SMS_URL    = 'https://sens.apigw.ntruss.com/sms/v2/services/{serviceId}/messages'
#     # time.time()*1000은 1970년 1월 1일 00:00:00 협정 세계시(UTC)부터의 경과 시간을
#     # 밀리초(Millisecond)단위로 나타낸 것
#     # API Gateway 서버와 시간 차가 5분 이상 나는 경우 유효하지 않은 요청으로 처리하기 위해 필요하다
#     timestamp  = str(int(time.time()*1000))
#     # serviceId와 마찬가지로 클라우드 플랫폼 가입자마다 다른 고유 secret key
#     secret_key = bytes(AUTH_SECRET_KEY, 'utf-8')
    
#     method = 'POST'
#     uri    = '/sms/v2/services/{serviceId}/messages'
#     message    = method + ' ' + uri + '\n' + timestamp + '\n' + AUTH_ACCESS_KEY
    
#     # message 형태를 풀어쓰면 아래와 같다.
#     '''
#     GET /photos/puppy.jpg?query1=&query2
#     {timeStamp}
#     {accessKey}
#     '''
#     # 암호화하기 위해 bytes type으로 인코딩한다.
#     message    = bytes(message, 'utf-8')

#     # 위에서 생성한 StringToSign(message)를 HmacSHA256 알고리즘으로 암호화한 후
#     # base64로 인코딩해서 signingKey를 만든다.
#     signingKey = base64.b64encode(
#       hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    
#     # 요청 헤더
#     headers    = {
#       'Content-Type'             : 'application/json; charset=utf-8',
#       'x-ncp-apigw-timestamp'    : timestamp,
#       'x-ncp-iam-access-key'     : AUTH_ACCESS_KEY,
#       'x-ncp-apigw-signature-v2' : signingKey,
#     }

#     # 요청 바디
#     body       = {
#       # 장문 문자라면 'LMS'
#       'type'        : 'SMS',
#       'contentType' : 'COMM',
#       'countryCode' : '82',
#       # 카페 24와 마찬가지로 주요 정보는 my_settings.py에 저장했고
#       # settings.py와 연결해 그곳에서 끌어온다.
#       'from'        : f'{SMS_SEND_PHONE_NUMBER}',
#       'content'     : f'인증번호 [{verification_number}]를 입력해주세요.',
#       'messages'    : [
#         {
#           'to' : phone_number
#         }
#       ]
#     }

#     # 만든 바디를 json 형태로 변환한 뒤
#     encoded_data = json.dumps(body)
#     # 헤더와 함께 post 메소드로 SMS 전송 url에 요청을 보낸다.
#     res = requests.post(SMS_URL, headers=headers, data=encoded_data)
#     return HttpResponse(res.status_code)

# def post(self, request):
#     try:
#         data                = json.loads(request.body)
#         member_phone        = data['phoneNumber']
#         # 6자리 인증번호 랜덤 생성
#         verification_number = str(randint(100000, 999999))
#         # 같은 휴대전화 번호로 여러 번 인증할 수 있는데,
#         # 이때마다 새로운 row를 생성해서 저장하면 안 되므로
#         # 휴대전화 번호가 존재하는지 여부를 확인해서 존재한다면 update로 처리해 인증번호만 갈아끼워 저장한다.
#         Verification.objects.update_or_create(
#         member_phone = member_phone,
#         defaults     = {
#             'member_phone'        : member_phone,
#             'verification_number' : verification_number
#         }
#         )
#         # 휴대전화번호와 인증번호를 담아 같은 클래스 내 send_verification 메소드를 호출한다.
#         # member_phone과 verification_number가 send_verification 메소드의 인자가 된다.
#         self.send_verification(
#             rphone              = member_phone,
#             verification_number = verification_number
#         )
#         return HttpResponse(status=200)
#     except KeyError:
#         return JsonResponse({'message' : 'Invalide key'}, status=400)

# def make_sig(self, string):
#     secret_key = bytes(SMS_SECRET_KEY, 'UTF-8')
#     return base64.b64encode(hmac.new(secret_key, string, digestmod=hashlib.sha256).digest())

# def send_sms(self):
#     timestamp = str(int(time.time()*1000))

#     message = 'POST' + URI + '\n' + timestamp + '\n' + ACCESS_KEY
#     message = bytes(message, 'UTF-8')

#     SIGNATURE = self.make_sig(message)

#     headers = {
#         "Content-Type": "application/json; charset=utf-8",
#         "x-ncp-apigw-timestamp": timestamp,
#         "x-ncp-iam-access-key": ACCESS_KEY,
#         "x-ncp-apigw-signature-v2": SIGNATURE
#     }

#     body = {
        
#     "type":"SMS",
#     "contentType":"COMM",
#     "from":"01012341234",
#     "content":"인증번호 [{}]를 입력하세요.".format(self.auth_number),
#     "messages":[
#         {
#             "to":self.phone
#         }
#     ],
#     }
#     requests.post(API_URL, data = json.dumps(body), headers = headers)