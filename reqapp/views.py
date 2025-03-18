from docx import Document
import os
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Request, Device, Category, ClosedRequest, WrittenOffDevice
from .forms import RequestForm, ChangeStatusForm

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
    
    categories = Category.objects.all()  # Получаем все категории

    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            request_instance = form.save(commit=False)
            request_instance.user = request.user
            request_instance.save()
            return redirect('request_list')
    else:
        form = RequestForm()
    
    return render(request, 'create_request.html', {'form': form, 'categories': categories})

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
    devices = Device.objects.filter(category_id=category_id, is_deleted=False).order_by('name')
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
    
    closed_requests = ClosedRequest.objects.filter(request__user=request.user).order_by('-closed_at')
    return render(request, 'closed_requests.html', {'closed_requests': closed_requests})

def generate_written_off_act(device):
    template_path = os.path.join(settings.BASE_DIR, 'reqapp', 'templates', 'act_template.docx')
    
    try:
        document = Document(template_path)
    except Exception as e:
        return HttpResponse(f"Ошибка при открытии шаблона: {str(e)}", status=500)

    replacements = {
        '{device_name}': device.name,
        '{device_code}': device.code or 'Нет кода',
        '{equipment_number}': device.equipment_number or 'Нет номера',
        '{purchase_date}': device.purchase_date.strftime('%d.%m.%Y') if device.purchase_date else 'Нет даты',
        '{initial_cost}': str(device.initial_cost) if device.initial_cost else 'Нет данных',
        '{location}': device.location or 'Нет данных',
        '{residual_value}': str(device.residual_value) if device.residual_value else 'Нет данных',
        '{written_off_date}': device.written_off_device.written_off_at.strftime('%d.%m.%Y'),
    }

    for paragraph in document.paragraphs:
        for key, value in replacements.items():
            if key in paragraph.text:
                paragraph.text = paragraph.text.replace(key, value)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = f'attachment; filename=act_written_off_{device.id}.docx'
    document.save(response)
    return response

def download_written_off_act(request, device_id):
    if not request.user.is_authenticated:
        return redirect('login')

    device = get_object_or_404(Device, id=device_id)
    if not hasattr(device, 'written_off_device'):
        return HttpResponse('Устройство не было списано.', status=400)

    return generate_written_off_act(device)

def written_off_devices(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    written_off_devices = WrittenOffDevice.objects.all().order_by('-written_off_at')
    return render(request, 'written_off_devices.html', {'written_off_devices': written_off_devices})