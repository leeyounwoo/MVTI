import hashlib
import hmac
import base64
import requests
import time, json
import random
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
messages = { "to" : "01027781007"}
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