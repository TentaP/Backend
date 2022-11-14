from django.urls import path

from . import views
from .api import auth

urlpatterns = [
    path('', views.index, name='index'),
    path('api/login/', auth.login.as_view()),
    path('api/logout/', auth.logout.as_view()),
    path('api/signup/', auth.signup.as_view()),
    path('api/user/', auth.userView.as_view()),
    path('api/users/<int:pk>', auth.user_details)
]
