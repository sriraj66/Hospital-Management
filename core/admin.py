from django.contrib import admin
from .models import *

admin.site.register(Profile)
admin.site.register(Blog)
admin.site.register(Appointment)
admin.site.register(Doctor)