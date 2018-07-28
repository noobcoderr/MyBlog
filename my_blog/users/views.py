from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib import auth
from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm


def login(request):

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('learning_logs:index')))    # 此处没获取到from ,不知道为什么

    else:
        login_form = LoginForm()

    context = {
        'login_form': login_form
    }
    return render(request, 'users/login.html', context)


def logout_view(request):
    """注销用户"""
    logout(request)
    return redirect(request.GET.get('from', reverse('learning_logs:index')))
    # referer = request.META.get('HTTP_REFERER', 'learning_logs/index.html')
    # return HttpResponseRedirect(referer)


def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():

            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']
            email = register_form.cleaned_data['email']

            user = User.objects.create_user(username, email, password)
            user.save()

            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)

            return redirect(request.GET.get('from', reverse('learning_logs:index')))
    else:
        register_form = RegisterForm()

    context = {
        'register_form': register_form
    }
    return render(request, 'users/register.html', context)


def user_info(request):
    context = {}
    return render(request, 'users/user_info.html', context)


