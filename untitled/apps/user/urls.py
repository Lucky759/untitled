
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginAPIView.as_view()),
    path('sms/', views.SMSAPIView.as_view()),
    path('login/mobile/', views.LoginMobileAPIView.as_view()),
    path('mobile/', views.MobileAPIView.as_view()),
    path('register/', views.RegisterAPIView.as_view()),

]
