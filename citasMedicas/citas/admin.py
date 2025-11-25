from django.contrib import admin
from .models import Paciente, Doctor, Consultorio, Cita
# Register your models here.

admin.site.register(Paciente)
admin.site.register(Doctor)
admin.site.register(Consultorio)
admin.site.register(Cita)
