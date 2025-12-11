from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from .models import Paciente, Doctor, Consultorio, Cita
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
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


class ListaMedicos(LoginRequiredMixin, ListView):
    model = Doctor
    
    template_name = 'lista_doctores.html'


class ListaConsultorios(LoginRequiredMixin, ListView):
    model = Consultorio
    template_name = 'lista_consultorios.html'


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
            return queryset.filter(doctor=user.doctor_profile)
        
        # Si el usuario tiene un perfil de paciente, muestra sus citas.
        if hasattr(user, 'paciente_profile'):
            return queryset.filter(paciente=user.paciente_profile)

        # Si es un superusuario o no tiene perfil (ej. recepcionista), puede ver todo.
        return queryset
