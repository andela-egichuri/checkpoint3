from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .forms import LoginForm, RegistrationForm


@login_required
def dashboard(request):
    """App dashboard"""
    return render(request, 'dashboard.html', {})


@login_required
def bucketlists(request, bucketid):
    """Bucketlist Manipulation"""
    data = {}
    data['bucketid'] = bucketid
    return render(request, 'bucketlists.html', data)


@api_view(('GET',))
def api_root(request, format=None):
    """Browsable API root"""
    return Response({
        'bucketlists': reverse(
            'bucketlist-list', request=request, format=format
        ),
        'items': reverse('item-list', request=request, format=format),
        'users': reverse('user-list', request=request, format=format),
    })


def index(request):
    """Handle login and registration"""
    if request.user.is_authenticated() and request.user.is_active:
        return HttpResponseRedirect('/dashboard')

    content = {}
    content['login_form'] = LoginForm()
    content['reg_form'] = RegistrationForm()

    if request.method == 'POST' and request.POST['src'] == 'login':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username'].upper()
            password = request.POST['password']

            user = authenticate(username=username, password=password)
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect('/dashboard/')
        content['messages'] = {'Error': 'Error logging in'}

    if request.method == 'POST' and request.POST['src'] == 'reg':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            content['messages'] = {'Success': 'Registration complete. You may now log in'}
        else:
            content['messages'] = form.errors
    return render(request, 'index.html', content)


@login_required
def user_logout(request):
    """Logout user and redirect to homepage"""
    logout(request)
    return HttpResponseRedirect('/')