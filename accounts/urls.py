from django.urls import path
from .views import RegisterUser
from .views import LoginUser
from .views import ProfileView
from .views import AllUsersView

urlpatterns = [
    path('register/', RegisterUser.as_view()),
    path('login/', LoginUser.as_view()),
    path('profile/', ProfileView.as_view()),
    path('all-users/', AllUsersView.as_view()),
]