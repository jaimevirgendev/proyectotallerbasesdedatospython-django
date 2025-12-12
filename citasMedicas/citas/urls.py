from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    # Listados
    path('pacientes/', ListaPacientes.as_view(), name='lista_pacientes'), 
    path('doctores/', ListaMedicos.as_view(), name='lista_doctores'),
    path('consultorios/', ListaConsultorios.as_view(), name='lista_consultorios'),
    path('citas/', ListaCitas.as_view(), name='lista_citas'),

    # CRUD Pacientes
    path('pacientes/nuevo/', CrearPaciente.as_view(), name='crear_paciente'),
    path('pacientes/editar/<int:pk>/', EditarPaciente.as_view(), name='editar_paciente'),
    path('pacientes/eliminar/<int:pk>/', EliminarPaciente.as_view(), name='eliminar_paciente'),

    # CRUD Doctores
    path('doctores/nuevo/', CrearDoctor.as_view(), name='crear_doctor'),
    path('doctores/editar/<int:pk>/', EditarDoctor.as_view(), name='editar_doctor'),
    path('doctores/eliminar/<int:pk>/', EliminarDoctor.as_view(), name='eliminar_doctor'),

    # CRUD Consultorios
    path('consultorios/nuevo/', CrearConsultorio.as_view(), name='crear_consultorio'),
    path('consultorios/editar/<int:pk>/', EditarConsultorio.as_view(), name='editar_consultorio'),
    path('consultorios/eliminar/<int:pk>/', EliminarConsultorio.as_view(), name='eliminar_consultorio'),

    # CRUD Citas
    path('citas/nueva/', CrearCita.as_view(), name='crear_cita'),
    path('citas/editar/<int:pk>/', EditarCita.as_view(), name='editar_cita'),
    path('citas/eliminar/<int:pk>/', EliminarCita.as_view(), name='eliminar_cita'),

    # Extras
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('panel-backup/', VistaBackup.as_view(), name='vista_backup'),
    path('backup/', RealizarBackup.as_view(), name='realizar_backup'),
    # URL para el Login
    path('', auth_views.LoginView.as_view(template_name='login.html', next_page='dashboard', redirect_authenticated_user=True), name='login'),
    
    # URL para el Logout (Cerrar sesión)
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]