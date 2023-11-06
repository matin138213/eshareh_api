from rest_framework.urls import path
from . import views

urlpatterns = [
    path('usernumber/', views.UserPhoneNumbers.as_view()),
    path('login/', views.Login.as_view()),
]
