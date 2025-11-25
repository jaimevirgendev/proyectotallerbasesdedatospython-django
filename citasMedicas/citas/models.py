from django.db import models

# Create your models here.

#Consultorio
class Consultorio(models.Model):
    nombre_consultorio = models.CharField(max_length=100)
    direccion = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.nombre_consultorio

#Doctor
class Doctor(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    consultorio = models.ForeignKey(Consultorio, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

#Paciente
class Paciente(models.Model):
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45, blank=True, null=True)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre}{self.apellido}"
    
class Cita(models.Model):
    # Relación con Paciente
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    # Relación con Doctor
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    # Relación con Consultorio (Aquí estaba el error)
    consultorio = models.ForeignKey(Consultorio, on_delete=models.CASCADE)
    
    fecha_cita = models.DateField()
    hora_cita = models.TimeField()
    motivo = models.CharField(max_length=255, blank=True, null=True)
    notas = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Cita: {self.paciente} con {self.doctor}"

