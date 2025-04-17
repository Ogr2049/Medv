from django.contrib import admin

from .models import *

admin.site.register(Step)
admin.site.register(Recipe)
admin.site.register(Meal)
admin.site.register(Day)