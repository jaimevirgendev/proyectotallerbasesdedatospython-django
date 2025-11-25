from django.urls import path
from .views import ListaPacientes

urlpatterns = [
    # La cadena vacía '' significa que será la página principal de esta app
    path('', ListaPacientes.as_view(), name='lista_pacientes'), 
]