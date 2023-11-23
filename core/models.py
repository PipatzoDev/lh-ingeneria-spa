from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.


# Modelo de Recursos Humanos
class Empleado(models.Model):
    rut = models.CharField(max_length=15,primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    departamento = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    correo_electronico = models.EmailField()
    telefono = models.CharField(max_length=20)
    select_gender = (
        ('Mujer', 'Mujer'),
        ('Hombre', 'Hombre'),
        )
    genero = models.CharField(max_length=8, choices=select_gender)
    direccion = models.TextField()
    imageEmp = models.ImageField(upload_to='media/imagesEmpleados/', null=True, blank=True)
    
    def __str__(self):
        return f"({self.rut}) - {self.nombre} {self.apellido}"
    def get_absolute_url(self):
        return reverse("empleado-detail", kwargs={"pk":self.rut})
#        #return reverse("empleado-detail", kwargs={"pk": self.id})#



# Modelo de Registro de Asistencia
class RegistroAsistencia(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fecha = models.DateField()
    asistencia = models.CharField(max_length=20)
    hora_entrada = models.TimeField()
    hora_salida = models.TimeField()
    class Meta:
        unique_together = ('empleado', 'fecha')

# Modelo de Feriados
class Feriado(models.Model):
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    
    def __str__(self):
        return self.id

# Modelo de Proveedores
class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField(max_length=100)
    correo_electronico = models.EmailField()
    telefono = models.CharField(max_length=20)
    direccion = models.TextField()
    
    def __str__(self):
        return self.nombre_empresa
    def get_absolute_url(self):
        return reverse("proveedor-detail", kwargs={"pk":self.id_proveedor})
    def clean(self):
        # Verificar si ya existe un objeto con el mismo atributo_repetido
        if Proveedor.objects.filter(nombre_empresa=self.nombre_empresa).exclude(pk=self.pk).exists():
            raise ValidationError({'nombre_empresa': 'Empresa ya se encuentra registrada.'})

    
# Modelo de Finanzas
class Transaccion(models.Model):
    id_transaccion = models.AutoField(primary_key=True)
    tipo_transaccion = models.CharField(max_length=50)
    fecha_transaccion = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    empleado_relacionado = models.ForeignKey(Empleado, on_delete=models.SET_NULL, blank=True, null=True)
    proveedor_relacionado = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, blank=True, null=True)
    archivo = models.FileField(upload_to='archivos/')  # 'archivos/' es el directorio donde se guardarán los archivos
    
    def __int__(self):
        return self.id_transaccion

