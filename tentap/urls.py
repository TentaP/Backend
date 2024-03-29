from django.urls import path

from . import views
from .api import auth, course, file, university, review, comment, users, avatar

urlpatterns = [
    path('', views.index, name='index'),
    path('api/login', auth.login.as_view()),
    path('api/signup', auth.signup.as_view()),
    path('api/verifection/<str:email>/<str:hash_>', auth.emailVerification.as_view()),
    path('api/set_superuser', auth.setSuperUser.as_view()),
    path('api/set_admin', auth.setAdmin.as_view()),
    path('api/remove_admin', auth.removeAdmin.as_view()),
    path('api/request_password_reset_token', auth.requestPasswordResetToken.as_view()),
    path('api/reset_password_via_token', auth.resetPasswordViaToken.as_view()),
    path('api/reset_password', auth.resetPassword.as_view()),
    #User
    path('api/user', users.userView.as_view()),
    path('api/user/uni/<int:pk>', users.userUni.as_view()),
    path('api/user/avatar', avatar.avatar_upload.as_view()),
    path('api/user/avatar/<int:pk>', avatar.avatar_pk.as_view()),
    path('api/user/<int:pk>', users.userDetails.as_view()),
    path('api/user/files', file.userFiles.as_view()),
    path('api/user/courses', course.userCourses.as_view()),
    path('api/users', users.usersList.as_view()),

    #UserSearch
    path('api/user/<int:pk>/files', file.filesByUser.as_view()),

    #Course/s
    path('api/courses', course.courses.as_view()),
    path('api/courses/uni/<str:uni>', course.coursesByUni.as_view()),
    path('api/course/<int:pk>', course.coursePk.as_view()),
    path('api/course/<str:course_name>/files', file.filesByCourse.as_view()),
    path('api/course/<int:pk>/reviews', review.ReviewListByCourse.as_view()),
    #File
    path('api/file', file.fileUpload.as_view()),
    path('api/files', file.files.as_view()),
    path('api/file/<int:pk>', file.filePk.as_view()),
    path('api/file/<int:pk>/reviews', review.ReviewListByFile.as_view()),
    path('api/file/<int:pk>/comments', comment.CommentListByFile.as_view()),
    #University
    path('api/uni', university.university.as_view()),
    path('api/uni/<int:pk>', university.universitypk.as_view()),
    #Review/s
    path('api/review/course/<int:course_pk>', review.ReviewItem.as_view()),
    path('api/review/file/<int:file_pk>', review.ReviewItem.as_view()),
    path('api/review/<int:pk>', review.ReviewPk.as_view()),
    #Comment
    path('api/comment/<int:pk>', comment.Comment.as_view()),
]
