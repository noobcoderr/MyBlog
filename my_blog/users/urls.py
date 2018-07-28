"""为应用程序users定义url模式"""

from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [

    # 注册
    path('register/', views.register, name='register'),

    # 登录
    path('login/', views.login, name='login'),

    # 注销界面
    path('logout/', views.logout_view, name='logout'),

    path('user_info/', views.user_info, name='user_info'),

]