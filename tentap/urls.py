from django.urls import path

from . import views
from .api import auth, course, file, university

urlpatterns = [
    path('', views.index, name='index'),
    path('api/login/', auth.login.as_view()),
    path('api/logout/', auth.logout.as_view()),
    path('api/signup/', auth.signup.as_view()),
    path('api/user/', auth.userView.as_view()),
    path('api/users/<int:pk>', auth.user_details),
    path('api/course/', course.courses),
    path('api/course/<int:pk>', course.course),
    path('api/file/', file.fileupload),
    path('api/file/<int:pk>', file.file),
    path('api/uni/', university.university),
    path('api/uni/<int:pk>', university.universitypk.as_view())
]
