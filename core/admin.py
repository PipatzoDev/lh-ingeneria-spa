from django.contrib import admin
from .models import *
from django.apps import apps

# Register your models here.
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('rut',"nombre", "apellido",'fecha_nacimiento','departamento','cargo','correo_electronico','genero','telefono','direccion')
    search_fields = ('rut',"nombre", "apellido",'fecha_nacimiento','departamento','cargo','correo_electronico','genero','telefono','direccion')
    list_filter = ('departamento','genero')


admin.site.register(Empleado,EmpleadoAdmin)
admin.site.register(RegistroAsistencia)
admin.site.register(Feriado)
admin.site.register(Proveedor)
admin.site.register(Transaccion)

#app = apps.get_app_config('core')
#for model_name, model in app.models.items():
#     admin.site.register(model)
