from django.contrib import admin

# Register your models here.
# from django.contrib import admin
from .models import Airplane, Flight

admin.site.register(Airplane)
admin.site.register(Flight)
