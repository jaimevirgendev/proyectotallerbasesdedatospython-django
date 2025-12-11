from django.contrib import admin
from .models import Paciente, Doctor, Consultorio, Cita

@admin.register(Consultorio)
class ConsultorioAdmin(admin.ModelAdmin):
    list_display = ('nombre_consultorio', 'direccion')
    search_fields = ('nombre_consultorio',)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'consultorio')
    list_filter = ('consultorio',) # Filtro lateral
    search_fields = ('nombre', 'email')

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'telefono', 'fecha_nacimiento')
    search_fields = ('nombre', 'apellido') # Buscador por nombre
    list_filter = ('fecha_nacimiento',)

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    # Columnas que verás en la tabla
    list_display = ('fecha_cita', 'hora_cita', 'paciente', 'doctor', 'motivo')
    
    # Filtros laterales (Vital para secretarias/doctores)
    list_filter = ('fecha_cita', 'doctor', 'consultorio')
    
    # Barra de búsqueda (Busca por nombre de paciente O doctor)
    search_fields = ('paciente__nombre', 'doctor__nombre', 'motivo')
    
    # Navegación rápida por fechas
    date_hierarchy = 'fecha_cita'