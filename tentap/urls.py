from django.urls import path

from . import views
from . import auth

urlpatterns = [
    path('', views.index, name='index'),
    path('api/login', auth.login.as_view()),
    path('api/logout', auth.logout.as_view()),
    path('api/signup', auth.signup.as_view()),
    path('api/verifection/<str:email>/<str:hash_>', auth.emailVerification.as_view()),
    path('api/set_superuser', auth.setSuperUser.as_view()),
    path('api/set_admin', auth.setAdmin.as_view()),
    path('api/remove_admin', auth.removeAdmin.as_view()),
    path('api/request_password_reset_link', auth.requestPasswordResetLink.as_view()),
    path('api/reset_password_link/<str:email>/<str:hash_>', auth.resetPasswordViaLink.as_view()),
    path('api/reset_password', auth.resetPassword.as_view()),
    path('api/user', auth.userView.as_view()),
    path('api/users/<int:pk>', auth.user_details)
]
