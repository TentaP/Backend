from django.urls import path

from . import views
from . import auth

urlpatterns = [
    path('', views.index, name='index'),
    path('api/login/', auth.login.as_view()),
    path('api/logout/', auth.logout.as_view()),
    path('api/signup/', auth.signup.as_view()),
    path('api/verifection/<str:email>/<str:hash_>', auth.emailVerification.as_view()),
    path('api/setsuperuser/', auth.setSuperUser.as_view()),
    path('api/setadmin/', auth.setAdmin.as_view()),
    path('api/removeadmin/', auth.removeAdmin.as_view()),
    path('api/user/', auth.userView.as_view()),
    path('api/users/<int:pk>', auth.user_details)
]
