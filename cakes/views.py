from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LogoutView
from django.contrib.auth.hashers import make_password
from django.views.decorators.http import require_POST
from cart.models import Cart

from users.models import *
from users.forms import *
from diary.models import *

from .models import *


def parse(request):
    from bs4 import BeautifulSoup
    import requests as r

    url = 'https://www.alenka.ru/catalog/'

    res = r.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    products = soup.find_all('div', 's-card')

    for product in products:
        text = product.find('a', 's-card-body-title').text.split(' ')
        category = text[0]
        name = ''
        if 'гр' in text[-1]:
            name = ' '.join(text[1:-2])
        else:
            name = ' '.join(text[1:])
        name = name.replace(',', '')

        price, amount = product.find('span', 's-card-body-price-title-old-current').text.split()
        amount = amount.split('/')[1]
        image = 'https://www.alenka.ru' + product.find('img').attrs['data-src']
        data = {
        'name': name,
        'category': category,
        'price': price,
        'amount': amount,
        'image': image,
        }
        Product.objects.update_or_create(**data)
    return None

def index(request):
    return render(request, 'index.html')

class Logout(LogoutView):
    template_name = 'index.html'

def signin(request):
    if request.user.is_authenticated:
        return redirect('cakes:index')
    if request.method == 'GET':
        form = UserSigninForm()
        context = {'form': form}
        return render(request, 'signin.html', context)
    elif request.method == 'POST':
        form = UserSigninForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user:
                login(request, user)
                return redirect('cakes:index')
            else:
                form = UserSigninForm()
                error = 'Неверные данные!'
                context = {'form': form, 'error': error}
                return render(request, 'signin.html', context)

def signup(request):
    if request.user.is_authenticated:
        return redirect('cakes:index')
    if request.method == 'GET':
        form = UserSignupForm()
        context = {'form': form}
        return render(request, 'signup.html', context)
    elif request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['password_confirm']
            if password == password_confirm:
                User.objects.create(
                    username=username,
                    password=make_password(password),
                    first_name=name,
                    last_name=surname,
                    email=email
                )
                return redirect('cakes:signin')
            
def catalog(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, 'catalog.html', context)

def profile(request):
    if request.method == 'GET' and request.user.is_authenticated:
        context = {
            'user': request.user,
        }
        return render(request, 'profile.html', context)
    else:
        return redirect('cakes:index')
    
def profile_update(request):
    if request.method == 'GET' and request.user.is_authenticated:
        user = request.user
        context = {
            'user': user,
            'form': UserUpdateForm(instance=user),
        }
        return render(request, 'profile_update.html', context)
    elif request.method == 'POST' and request.user.is_authenticated:
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('cakes:profile')
        else:
            print(form.errors)
    else:
        return redirect('cakes:index')

@require_POST
def cart_add(request):
    cart = Cart(request)
    product = Product.objects.get(id=request.GET['id'])
    cart.add(product=product,
        quantity=1,
        update_quantity=False
    )
    return redirect(request.META.get('HTTP_REFERER'))

def cart(request):
    cart = Cart(request)
    context = {
        'cart': cart
    }
    return render(request, 'cart.html', context)

@require_POST
def cart_remove(request):
    cart = Cart(request)
    product = Product.objects.get(id=request.GET['id'])
    cart.remove(product)
    return redirect(request.META.get('HTTP_REFERER'))

@require_POST
def cart_decrease(request):
    cart = Cart(request)
    product = Product.objects.get(id=request.GET['id'])
    cart.decrease(product, 1)
    return redirect(request.META.get('HTTP_REFERER'))

def reminders(request):
    if request.method == 'PUT':
        attr = request.body.decode().split('&')
        id = int(attr[0].split('=')[1])
        checked = int(attr[1].split('=')[1])
        reminder = get_object_or_404(Reminders, id=id)
        reminder.checked = True if checked == 1 else False
        reminder.save()
    if request.GET.get('id'):
        if request.method == 'DELETE':
            id = int(request.GET.get('id'))
            get_object_or_404(Reminders, id=id).delete()
            return redirect('cakes:reminders')
        id = int(request.GET.get('id'))
        return render(request, 'reminder.html', {'reminder': get_object_or_404(Reminders, id=id)})
    return render(request, 'reminders.html', {'reminders': Reminders.objects.filter(user=request.user).order_by('-id')})


def reminder(request, id):
    if request.method == 'DELETE':
        get_object_or_404(Reminders, id=id).delete()
        return redirect('reminders')
    if request.method == 'POST':
        r = get_object_or_404(Reminders, id=id)
        r.text = request.POST['text']
        r.date = request.POST.get('time') if request.POST.get('time') else r.date
        r.save()
        return redirect('cakes:reminders')
    return render(request, 'reminder.html', {'reminder': get_object_or_404(Reminders, id=id)})

def create_reminder(request):
    if request.method == 'POST':
        data = request.POST
        reminder = Reminders()
        reminder.text = data['Text']
        reminder.user = request.user
        reminder.date = data['date']
        reminder.save()
        return redirect('cakes:reminders')
    elif request.method == 'DELETE':
        pass
    return render(request, 'create_reminder.html')