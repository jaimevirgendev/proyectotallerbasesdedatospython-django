from django.shortcuts import render
from django.views.generic import ListView, TemplateView, View, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Paciente, Doctor, Consultorio, Cita
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
import subprocess
import os
# Create your views here.


class ListaPacientes(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Paciente
    template_name = 'lista_pacientes.html'

    def test_func(self):
        """
        Solo permite el acceso a Doctores (usuarios con perfil de doctor) o superusuarios.
        """
        user = self.request.user
        return user.is_superuser or hasattr(user, 'doctor_profile')

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(Q(nombre__icontains=q) | Q(apellido__icontains=q) | Q(email__icontains=q))
        return queryset


class ListaMedicos(LoginRequiredMixin, ListView):
    model = Doctor
    template_name = 'lista_doctores.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(Q(nombre__icontains=q) | Q(email__icontains=q))
        return queryset


class ListaConsultorios(LoginRequiredMixin, ListView):
    model = Consultorio
    template_name = 'lista_consultorios.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(nombre_consultorio__icontains=q)
        return queryset


class ListaCitas(LoginRequiredMixin, ListView):
    model = Cita
    template_name = 'lista_citas.html'

    def get_queryset(self):
        """
        Sobrescribimos este método para filtrar las citas dependiendo del perfil del usuario.
        """
        user = self.request.user
        queryset = super().get_queryset()

        # Si el usuario tiene un perfil de doctor, muestra sus citas.
        if hasattr(user, 'doctor_profile'):
            queryset = queryset.filter(doctor=user.doctor_profile)
        
        # Si el usuario tiene un perfil de paciente, muestra sus citas.
        elif hasattr(user, 'paciente_profile'):
            queryset = queryset.filter(paciente=user.paciente_profile)

        # Lógica de búsqueda
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(paciente__nombre__icontains=q) | 
                Q(paciente__apellido__icontains=q) | 
                Q(doctor__nombre__icontains=q) |
                Q(motivo__icontains=q)
            )

        return queryset


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Contadores totales
        context['total_pacientes'] = Paciente.objects.count()
        context['total_doctores'] = Doctor.objects.count()
        context['total_consultorios'] = Consultorio.objects.count()
        context['total_citas'] = Cita.objects.count()

        # Agrupar citas por mes
        citas_mes = Cita.objects.annotate(
            mes=TruncMonth('fecha_cita')
        ).values('mes').annotate(
            cantidad=Count('id')
        ).order_by('mes')

        context['citas_por_mes'] = citas_mes
        return context


class RealizarBackup(LoginRequiredMixin, View):
    """
    Genera un backup completo de la base de datos MySQL usando mysqldump.
    """
    def get(self, request, *args, **kwargs):
        # Obtenemos credenciales desde settings.py
        db_conf = settings.DATABASES['default']
        db_name = db_conf['NAME']
        db_user = db_conf['USER']
        db_password = db_conf['PASSWORD']
        db_host = db_conf['HOST'] or 'localhost'
        db_port = db_conf['PORT'] or '3306'

        # Configurar entorno para pasar la contraseña de forma segura
        env = os.environ.copy()
        if db_password:
            env['MYSQL_PWD'] = db_password

        # Comando mysqldump (debe estar en el PATH del sistema)
        cmd = ['mysqldump', '-h', db_host, '-P', str(db_port), '-u', db_user, db_name]

        try:
            process = subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()

            if process.returncode != 0:
                return HttpResponse(f"Error al generar backup: {error.decode('utf-8', errors='replace')}", status=500)

            response = HttpResponse(output, content_type='application/sql')
            response['Content-Disposition'] = f'attachment; filename="backup_{db_name}_{timezone.now().strftime("%Y-%m-%d_%H-%M")}.sql"'
            return response
            
        except FileNotFoundError:
            return HttpResponse("Error: No se encontró el comando 'mysqldump'. Asegúrate de que la carpeta 'bin' de MySQL esté en el PATH de Windows.", status=500)


class VistaBackup(LoginRequiredMixin, TemplateView):
    template_name = 'backup.html'


# --- VISTAS CRUD GENÉRICAS ---

# Constantes para templates compartidos
TEMPLATE_FORM = 'form_generico.html'
TEMPLATE_DELETE = 'confirmar_eliminar.html'

# CRUD PACIENTES
class CrearPaciente(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Paciente
    fields = '__all__'
    template_name = TEMPLATE_FORM
    success_url = reverse_lazy('lista_pacientes')
    success_message = "Paciente creado correctamente."

class EditarPaciente(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Paciente
    fields = '__all__'
    template_name = TEMPLATE_FORM
    success_url = reverse_lazy('lista_pacientes')
    success_message = "Paciente actualizado correctamente."

class EliminarPaciente(LoginRequiredMixin, DeleteView):
    model = Paciente
    template_name = TEMPLATE_DELETE
    success_url = reverse_lazy('lista_pacientes')
    
    def form_valid(self, form):
        messages.success(self.request, "Paciente eliminado correctamente.")
        return super().form_valid(form)

# CRUD DOCTORES
class CrearDoctor(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Doctor
    fields = '__all__'
    template_name = TEMPLATE_FORM
    success_url = reverse_lazy('lista_doctores')
    success_message = "Doctor registrado correctamente."

class EditarDoctor(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Doctor
    fields = '__all__'
    template_name = TEMPLATE_FORM
    success_url = reverse_lazy('lista_doctores')
    success_message = "Información del doctor actualizada."

class EliminarDoctor(LoginRequiredMixin, DeleteView):
    model = Doctor
    template_name = TEMPLATE_DELETE
    success_url = reverse_lazy('lista_doctores')
    def form_valid(self, form):
        messages.success(self.request, "Doctor eliminado correctamente.")
        return super().form_valid(form)

# CRUD CONSULTORIOS
class CrearConsultorio(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Consultorio
    fields = '__all__'
    template_name = TEMPLATE_FORM
    success_url = reverse_lazy('lista_consultorios')
    success_message = "Consultorio creado correctamente."

class EditarConsultorio(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Consultorio
    fields = '__all__'
    template_name = TEMPLATE_FORM
    success_url = reverse_lazy('lista_consultorios')
    success_message = "Consultorio actualizado."

class EliminarConsultorio(LoginRequiredMixin, DeleteView):
    model = Consultorio
    template_name = TEMPLATE_DELETE
    success_url = reverse_lazy('lista_consultorios')
    def form_valid(self, form):
        messages.success(self.request, "Consultorio eliminado correctamente.")
        return super().form_valid(form)

# CRUD CITAS
class CrearCita(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Cita
    fields = '__all__'
    template_name = TEMPLATE_FORM
    success_url = reverse_lazy('lista_citas')
    success_message = "Cita agendada correctamente."

class EditarCita(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Cita
    fields = '__all__'
    template_name = TEMPLATE_FORM
    success_url = reverse_lazy('lista_citas')
    success_message = "Cita actualizada."

class EliminarCita(LoginRequiredMixin, DeleteView):
    model = Cita
    template_name = TEMPLATE_DELETE
    success_url = reverse_lazy('lista_citas')
    def form_valid(self, form):
        messages.success(self.request, "Cita eliminada correctamente.")
        return super().form_valid(form)
