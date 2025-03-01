from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RequestForm, ChangeStatusForm
from .models import Request, Device, Category, ClosedRequest
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def home_view(request):
    return render(request, 'home.html')

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
    
    requests = Request.objects.filter(user=request.user).exclude(status='closed')
    return render(request, 'request_list.html', {'requests': requests})

def logout_view(request):
    logout(request)
    return redirect('login')

def load_devices(request):
    category_id = request.GET.get('category_id')
    devices = Device.objects.filter(category_id=category_id).order_by('name')
    return JsonResponse(list(devices.values('id', 'name')), safe=False)

def change_status(request, request_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    request_instance = get_object_or_404(Request, id=request_id, user=request.user)
    
    if request.method == 'POST':
        form = ChangeStatusForm(request.POST)
        if form.is_valid():
            new_status = form.cleaned_data['status']
            request_instance.set_status(new_status)
            return redirect('request_list')
    else:
        form = ChangeStatusForm(initial={'status': request_instance.status})
    
    return render(request, 'change_status.html', {'form': form, 'request_instance': request_instance})

def closed_requests(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    closed_requests = ClosedRequest.objects.filter(request__user=request.user)
    return render(request, 'closed_requests.html', {'closed_requests': closed_requests})