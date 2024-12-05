from django.contrib import admin
from .models import Log

# Register your models here.


@admin.register(Log)
class AdminLog(admin.ModelAdmin):
    list_display = ['id', 'logs']
