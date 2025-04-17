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
    path('catalog/', catalog, name='catalog'),

    path('profile/', profile, name='profile'),
    path('profile_update/', profile_update, name='profile_update'),

    path('cart_add/', cart_add, name='cart_add'),
    path('cart/', cart, name='cart'),
    path('cart_remove/', cart_remove, name='cart_remove'),
    path('cart_decrease/', cart_decrease, name='cart_decrease'),

    path("reminders/", reminders, name="reminders"),
    path("reminder/<int:id>", reminder, name="reminder"),
    path("create_reminder/", create_reminder, name="create_reminder"),
]