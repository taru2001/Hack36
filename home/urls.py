from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from . import views



urlpatterns = [
    path('',views.home_view,name='home_view'),
    path('login/',views.login_user,name='login_page'),
    path('signup/',views.signup_user,name='signup_page'),
    path('logout/',views.logout_user,name='logout'),
    path('user/google/validate/',views.validate_user,name='validate_user'), #Use This to redirect any user to its right place
    path('user/student/confirm/',views.student_confirm,name='student_confirm'),#Setting new Students here
    path('user/teacher/confirm/',views.teacher_confirm,name='teacher_confirm'), #Setting new Teacher here
]
