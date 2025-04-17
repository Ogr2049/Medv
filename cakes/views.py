from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LogoutView
from django.contrib.auth.hashers import make_password

from users.models import *
from users.forms import *

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