from django.urls import path
from .views import ProductListView, ProductView

urlpatterns=[
    path('',ProductListView.as_view()),
    path('/<int:pk>', ProductView.as_view()),
]

