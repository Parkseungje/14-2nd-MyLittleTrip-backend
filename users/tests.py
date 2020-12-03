from datetime import datetime
import bcrypt
import jwt

from django.test   import TestCase, Client
from unittest.mock import patch, MagicMock

from .models       import User
from .utils        import Login_decorator
from my_settings   import JWT_ALGORITHM, SECRET_KEY


class SignUpTestCase(TestCase):
    def setUp(self):
        self.URL = '/users/sign_up'
        self.client = Client()
        hashed_password = bcrypt.hashpw('12345678'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        User.objects.create(name = 'Dummy', email = 'dummy@naver.com', password = hashed_password, phone_number = '01012341234')
    
    def tearDown(self):
        User.objects.all().delete()

    def test_sign_up_post_success(self):
        request = {
            'name' : '승찬',
            'email' : 'seungchan@naver.com',
            'password' : '12345678',
            'phone_number' : '010-7266-5438'
        }
        response = self.client.post(self.URL, request,content_type='application/json')
        self.assertEqual(response.json()['message'],'SUCCESS')
        self.assertEqual(response.status_code, 200) 

    def test_sign_up_post_key_error(self):
        requests=[]
        # 전화번호 없을 때
        requests.append({
            'name' : '승찬',
            'email' : 'seungchan@naver.com',
            'password' : '12345678',
        })
        # 이메일 없을 때
        requests.append({
            'name' : '승찬',
            'password' : '12345678',
            'phone_number' : '010-7266-5438'
        })
        # 이름 없을 때
        requests.append({
            'email' : 'seungchan@naver.com',
            'password' : '12345678',
            'phone_number' : '010-7266-5438'
        })

        for request in requests:
            response = self.client.post(self.URL, request, content_type='application/json')
            self.assertEqual(response.json()['message'],'KEY_ERROR')
            self.assertEqual(response.status_code,400)

    def test_sign_up_post_overlap(self):
        requests =[]
        # 이메일 중복
        requests.append({
            'name' : 'Dummy',
            'email' : 'dummy@naver.com',
            'password' : '12345678',
            'phone_number' : '01012345678'
        })
        # 전화번호 중복
        requests.append({
            'name' : 'Dummy',
            'email' : 'dummy2@naver.com',
            'password' : '12345678',
            'phone_number' : '01012341234'
        })

        for request in requests:
            response = self.client.post(self.URL, request, content_type='application/json')
            self.assertEqual(response.json()['message'],'OVER_LAP_ERROR')
            self.assertEqual(response.status_code,400)
 
    def test_sign_up_post_password_error(self):
        request={
            'name' : 'Dummy',
            'email' : 'dummy3@naver.com',
            'password' : '12345',
            'phone_number' : '01012345678'
        }
        response = self.client.post(self.URL, request,content_type='application/json')
        self.assertEqual(response.json()['message'],'INVALID_ERROR')
        self.assertEqual(response.status_code, 400) 
    
    def test_sign_up_post_email_error(self):
        requests =[]
        # @(골뱅이) 가 없는 경우
        requests.append({
            'name' : 'Dummy',
            'email' : 'dummynaver.com',
            'password' : '12345678',
            'phone_number' : '01012344657'
        })
        # .(콤마) 가 없는 경우
        requests.append({
            'name' : 'Dummy',
            'email' : 'dummy2@navercom',
            'password' : '12345678',
            'phone_number' : '01012341231'
        })

        for request in requests:
            response = self.client.post(self.URL, request, content_type='application/json')
            self.assertEqual(response.json()['message'],'INVALID_ERROR')
            self.assertEqual(response.status_code,400)

    def test_sign_up_post_password_verification(self):
        hashed_password = User.objects.get(email = 'dummy@naver.com').password.encode('utf-8')
        new_password = '12345678'.encode('utf-8')
        self.assertEqual(bcrypt.checkpw(new_password,hashed_password), True)

class SignInTestCase(TestCase):
    def setUp(self):
        self.URL = '/users/sign_in'
        self.client = Client()
        hashed_password = bcrypt.hashpw('12345678'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        User.objects.create(name = 'Dummy', email = 'dummy@naver.com', password = hashed_password, phone_number = '01012341234')
    
    def tearDown(self):
        User.objects.all().delete()

    def test_sign_in_post_success(self):
        request = {
            'email' : 'dummy@naver.com',
            'password' : '12345678'
        }
        User.objects.get(email=request['email'])
        response = self.client.post(self.URL,request,content_type='application/json')
        self.assertEqual('token'in response.json().keys(),True)
        self.assertEqual(response.status_code, 200) 

    def test_sign_in_post_does_not_exist_user(self):
        request = {
            'email' : 'dummy1@naver.com',
            'password' : '12345678'
        }
        response = self.client.post(self.URL,request,content_type='application/json')
        self.assertEqual(response.json()['message'],'INVALID_ERROR')
        self.assertEqual(response.status_code, 400) 

    def test_sign_in_post_key_error(self):
        requests = []
        requests.append({
            'email' : 'dummy@naver.com'
        })
        requests.append({
            'password' : '12345678'
        })
        for request in requests:
            response = self.client.post(self.URL,request,content_type='application/json')
            self.assertEqual(response.json()['message'],'KEY_ERROR')
            self.assertEqual(response.status_code, 400) 

    def test_sign_in_post_wrong_password(self):
        request = {
            'email' : 'dummy@naver.com',
            'password' : 'abcdefgh'
        }

        response = self.client.post(self.URL,request,content_type='application/json')
        self.assertEqual(response.json()['message'],'INVALID_ERROR')
        self.assertEqual(response.status_code, 400) 

class SocialSignUpTestCase(TestCase):
    def setUp(self):
        hashed_password = bcrypt.hashpw('12345678'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        User.objects.create(
            name = 'kakao',
            email='kakao@gmail.com',
            password = hashed_password
        )
        self.request = Client()
        self.URL = '/users/sign_up/kakao'
    def tearDown(self):
        User.objects.all().delete()

    @patch('users.views.requests')
    def test_social_sign_up_post_success(self, mocked_request):
        class KakaoResponse:
            def json(self):
                return {'id': 1,
                'connected_at': str(datetime.now()),
                'properties': {'nickname': 'dummy'},
                'kakao_account': {
                    'profile_needs_agreement': False,
                    'profile': {'nickname': 'dummy'},
                    'has_email': True,
                    'email_needs_agreement': False, 
                    'is_email_valid': True, 'is_email_verified': True, 
                    'email': 'dummy@naver.com'
                    }
                }

        mocked_request.get = MagicMock(return_value = KakaoResponse())
        header = {'HTTP_Authorization': 'access_token'}
        response =self.client.post(self.URL, content_type='application/json', **header)
        self.assertEqual(response.status_code, 200)

class SocialSignInTestCase(TestCase):
    def setUp(self):
        hashed_password = bcrypt.hashpw('12345678'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        User.objects.create(
            name = 'dummy',
            email='dummy@naver.com',
            password = hashed_password
        )
        self.request = Client()
        self.URL = '/users/sign_in/kakao'
    def tearDown(self):
        User.objects.all().delete()

    @patch('users.views.requests')
    def test_social_sign_in_post_success(self, mocked_request):
        class KakaoResponse:
            def json(self):
                return {'id': 1,
                'connected_at': str(datetime.now()),
                'properties': {'nickname': 'dummy'},
                'kakao_account': {
                    'profile_needs_agreement': False,
                    'profile': {'nickname': 'dummy'},
                    'has_email': True,
                    'email_needs_agreement': False, 
                    'is_email_valid': True, 'is_email_verified': True, 
                    'email': 'dummy@naver.com'
                    }
                }

        mocked_request.get = MagicMock(return_value = KakaoResponse())
        header = {'HTTP_Authorization': 'access_token'}
        response =self.client.post(self.URL, content_type='application/json', **header)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,'access_token')
        
    @patch('users.views.requests')
    def test_social_sign_in_post_key_error(self, mocked_request):
        class KakaoResponse:
            def json(self):
                return {'id': 1,
                'connected_at': str(datetime.now()),
                'properties': {'nickname': 'dummy'},
                'kakao_account': {
                    'profile_needs_agreement': False,
                    'profile': {'nickname': 'dummy'},
                    'has_email': True,
                    'email_needs_agreement': False, 
                    'is_email_valid': True, 'is_email_verified': True, 
                    'email': 'dummy@gmail.com'
                    }
                }

        mocked_request.get = MagicMock(return_value = KakaoResponse())
        header = {'HTTP_Authorization': 'access_token'}
        response =self.client.post(self.URL, content_type='application/json', **header)
        self.assertEqual(response.status_code, 400)