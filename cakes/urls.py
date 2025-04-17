from django.urls import path

from .views import *

app_name='cakes'

urlpatterns = [
    # Path to parse data from alenka.ru and save them into db
    path('parse/', parse, name='parse'),

    path('', index, name='index'),
    path('logout/', Logout.as_view(), name='logout'),
    path('signin/', signin, name='signin'),
    path('signup/', signup, name='signup'),
    path('catalog/', catalog, name='catalog')
]