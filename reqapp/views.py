from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RequestForm
from .models import Request

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('create_request')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def create_request(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            request_instance = form.save(commit=False)
            request_instance.user = request.user
            request_instance.save()
            return redirect('request_list')
    else:
        form = RequestForm()
    return render(request, 'create_request.html', {'form': form})

def request_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    requests = Request.objects.filter(user=request.user)
    return render(request, 'request_list.html', {'requests': requests})

def logout_view(request):
    logout(request)
    return redirect('login')