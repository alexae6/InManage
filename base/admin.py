from sqlite3 import dbapi2
from django.contrib import admin
from .models import Patient

# Register your models here.
admin.site.register(Patient)
