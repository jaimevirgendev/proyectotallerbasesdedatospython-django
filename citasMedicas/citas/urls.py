from django.urls import path
from django.contrib.auth import views as auth_views
from .views import ListaPacientes, ListaMedicos, ListaConsultorios, ListaCitas

urlpatterns = [
    path('pacientes/', ListaPacientes.as_view(), name='lista_pacientes'), 
    path('doctores/', ListaMedicos.as_view(), name='lista_doctores'),
    path('consultorios/', ListaConsultorios.as_view(), name='lista_consultorios'),
    path('citas/', ListaCitas.as_view(), name='lista_citas'),
    # URL para el Login
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    
    # URL para el Logout (Cerrar sesión)
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]