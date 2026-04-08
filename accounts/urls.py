from django.urls import path
from .views import RegisterUser
from .views import LoginUser

urlpatterns = [
    path('register/', RegisterUser.as_view()),
    path('login/', LoginUser.as_view()),
]