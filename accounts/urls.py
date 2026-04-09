from django.urls import path
from .views import RegisterUser
from .views import LoginUser
from .views import ProfileView

urlpatterns = [
    path('register/', RegisterUser.as_view()),
    path('login/', LoginUser.as_view()),
    path('profile/', ProfileView.as_view()),
]