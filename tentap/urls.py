from django.urls import path

from . import views
from . import auth
urlpatterns = [
    path('', views.index, name='index'),
    path('api/login/', auth.login),
    path('api/signup/', auth.signup),
    path('api/users/<int:pk>', auth.user_details)
]
