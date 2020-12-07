import json
import re
import bcrypt
import jwt
import requests

from django.http              import JsonResponse
from django.views             import View

from .models                  import User
from mylittletrip.my_settings import SECRET_KEY, JWT_ALGORITHM
from users.utils              import Login_decorator

class SignUpView(View):
    def post(self, request):
        data  = json.loads(request.body)
        try:
            if len(data['password']) < 8:
                return JsonResponse({'message' : 'INVALID_ERROR'}, status = 400)
            
            invalid_email = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            
            if not invalid_email.match(data['email']):
                return JsonResponse({'message' : 'INVALID_ERROR'}, status = 400)

            if User.objects.filter(phone_number = data['phone_number']).exists():
                return JsonResponse({'message': 'OVER_LAP_ERROR'},status=400)

            if User.objects.filter(email = data['email']).exists():
                return JsonResponse({'message': 'OVER_LAP_ERROR'},status=400)

            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(name = data['name'], email = data['email'],\
                 password = hashed_password, phone_number= data['phone_number'])
            return JsonResponse({'message': 'SUCCESS'},status=200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
    

class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = User.objects.get(email = data['email'])

            if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                token = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm=JWT_ALGORITHM).decode('utf-8')
                
                return JsonResponse({'token' : token}, status=200)

            return JsonResponse({'message' : 'INVALID_ERROR'}, status=400)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_ERROR'}, status=400)
    @Login_decorator
    def get(self, request):
        request.user
        user_info={
            'name' : request.user.name,
            'email' : request.user.email,
            'phone_number' : request.user.phone_number,
            'card_number' : request.user.card_number
        }
        return JsonResponse({'user_info':user_info}, status = 200)

    

class SocialSignUpView(View):
    def post(self, request):
        try :
            access_token = request.headers.get('Authorization', None)
            response = requests.get('https://kapi.kakao.com/v2/user/me',headers = {'Authorization' : 'Bearer '+ access_token}).json()
            print(response)
            if not User.objects.filter(email=response['kakao_account']['email']).exists():
                User.objects.create(email=response['kakao_account']['email'], name=response['kakao_account']['profile']['nickname'])
                return JsonResponse({"message" : "SUCCESS"}, status=200)
            return JsonResponse({'message' : 'INVALID_ERROR'})

        except KeyError :
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        
class SocialSignInView(View):
    def post(self, request):
        try:
            access_token = request.headers.get('Authorization', None)
            response = requests.get('https://kapi.kakao.com/v2/user/me',headers = {'Authorization': 'Bearer '+ access_token}).json()
            user = User.objects.get(email=response['kakao_account']['email'])
            token = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm=JWT_ALGORITHM).decode('utf-8')
            return JsonResponse({'Authorization' : token}, status=200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_ERROR'}, status=400)
