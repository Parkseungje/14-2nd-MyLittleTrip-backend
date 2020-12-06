from django.urls import path
from .views import SignInView, SignUpView, SocialSignUpView, SocialSignInView

urlpatterns = [
    path('/sign_up', SignInView.as_view()),
    path('/sign_in', SignUpView.as_view()),
    path('/sign_up/kakao', SocialSignUpView.as_view()),
    path('/sign_in/kakao', SocialSignInView.as_view()),
]