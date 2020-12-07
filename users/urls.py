from django.urls import path
from .views import SignInView, SignUpView, SocialSignUpView, SocialSignInView

urlpatterns = [
    path('',SignInView.as_view()),
    path('/sign_up', SignUpView.as_view()),
    path('/sign_in', SignInView.as_view()),
    path('/sign_up/kakao', SocialSignUpView.as_view()),
    path('/sign_in/kakao', SocialSignInView.as_view()),
]