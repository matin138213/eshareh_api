from rest_framework.urls import path
from . import views

urlpatterns = [
    path('user-number/', views.UserPhoneNumbers.as_view()),
    path('login/', views.Login.as_view()),
]
