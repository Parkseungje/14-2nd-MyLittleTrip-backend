import jwt
from django.http import request,JsonResponse
from my_settings import SECRET, ALGORITHMS
from .models import User

def login_decorator(func):
    def wrapper_func(self, request,**kwargs):
        access_token = request.headers.get('authorization')
        if access_token is None:
            return JsonResponse({'message': 'TOKEN PLEASE'},status=400)
        try:
            user_id = jwt.decode(access_token, SECRET, algorithms=ALGORITHMS)
            user = User.objects.get(id=user_id['id'])
            request.user = user.id
            return func(self,request,**kwargs)
        except KeyError:
            return JsonResponse({'message': "KEY_ERROR"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message':'UNKNOWN_USER'},status=401)
        except jwt.DecodeError:
            return JsonResponse({'message':'INVALID_TOKEN'},status=401)
    return wrapper_func
