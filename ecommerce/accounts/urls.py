from django.urls import path, include
from django.contrib import admin #
from . import views
#

urlpatterns = [
    path('user_login', views.user_login, name="user_login"),
    path('user_register', views.user_register, name="user_register"),
    path('user_logout', views.user_logout, name="user_logout"),
    path('not_registered', views.not_registered, name="not_registered"),
    path('already_member', views.already_member, name = "already_member"),
    
    path('forget_password', views.forgetpassword, name = "forget_password"),
    path('change_password<token>', views.changepassword, name = "change_password"), 
     
    
]