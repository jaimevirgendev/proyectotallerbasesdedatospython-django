from django.shortcuts import render
from django.views.generic import ListView
from .models import Paciente
# Create your views here.

class ListaPacientes(ListView):
    model = Paciente
    template_name = 'lista_pacientes.html'
