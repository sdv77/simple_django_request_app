from docx import Document
import os
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Request, Device, Category, ClosedRequest, WrittenOffDevice
from .forms import RequestForm, ChangeStatusForm

# Главная страница
def home_view(request):
    return render(request, 'home.html')

# Страница создания заявки
def create_request(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    categories = Category.objects.all()

    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            request_instance = form.save(commit=False)
            request_instance.user = request.user
            request_instance.save()
            messages.success(request, 'Заявка успешно создана!')
            return redirect('request_list')
        else:
            messages.error(request, 'Ошибка при создании заявки.')
    else:
        form = RequestForm()
    
    return render(request, 'create_request.html', {'form': form, 'categories': categories})

def change_status(request, request_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    request_instance = get_object_or_404(Request, id=request_id)

    # Проверка, является ли пользователь техником
    if not request.user.groups.filter(name='Technician').exists():
        return HttpResponse('У вас нет прав для изменения статуса заявки.', status=403)

    if request.method == 'POST':
        form = ChangeStatusForm(request.POST)
        if form.is_valid():
            new_status = form.cleaned_data['status']
            technician = form.cleaned_data['technician']  # Получаем техника, который изменяет статус
            request_instance.set_status(new_status, technician)  # Сохраняем техника и статус
            messages.success(request, 'Статус заявки успешно изменён!')
            return redirect('request_list')
    else:
        form = ChangeStatusForm(initial={'status': request_instance.status})
    
    return render(request, 'change_status.html', {'form': form, 'request_instance': request_instance})



def request_list(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Проверяем, является ли пользователь техником
    technician = request.user.groups.filter(name='Technician').exists()

    if technician:
        # Для техников показываем все заявки, кроме закрытых
        requests = Request.objects.exclude(status='closed')
    else:
        # Для обычных пользователей показываем только их заявки
        requests = Request.objects.filter(user=request.user).exclude(status='closed')

    return render(request, 'request_list.html', {'requests': requests, 'technician': technician})


# Список закрытых заявок
def closed_requests(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    closed_requests = ClosedRequest.objects.filter(request__user=request.user).order_by('-closed_at')
    return render(request, 'closed_requests.html', {'closed_requests': closed_requests})

# Страница для выхода пользователя
def logout_view(request):
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы.')
    return redirect('login')

# Страница для логина
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Вы успешно вошли в систему!')
                return redirect('create_request')
        else:
            messages.error(request, 'Ошибка при входе в систему. Проверьте правильность введённых данных.')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

# Загрузка устройств по категории (для AJAX)
def load_devices(request):
    category_id = request.GET.get('category_id')  # Получаем ID категории из GET запроса
    devices = Device.objects.filter(category_id=category_id, is_deleted=False).order_by('name')
    
    device_data = list(devices.values('id', 'name'))  # Извлекаем id и имя устройства
    return JsonResponse(device_data, safe=False)  # Возвращаем список устройств в формате JSON

# Генерация акта списания устройства
# views.py
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
    device = get_object_or_404(Device, id=device_id)
    if not hasattr(device, 'written_off_device'):
        return HttpResponse('Устройство не было списано.', status=400)

    return generate_written_off_act(device)

def written_off_devices(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Получаем все списанные устройства
    written_off_devices = WrittenOffDevice.objects.all().order_by('-written_off_at')
    
    return render(request, 'written_off_devices.html', {'written_off_devices': written_off_devices})

