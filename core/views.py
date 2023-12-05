from django.shortcuts import render
from .models import Empleado,RegistroAsistencia,Proveedor,Transaccion
from django.views import generic
from django.utils import timezone
from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth.decorators import login_required
from datetime import datetime,timedelta
from django.db.models import Count,F,Sum
from django.db.models import F, ExpressionWrapper, CharField
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.core.cache import cache
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime, timedelta
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

from django.shortcuts import render
from google.oauth2 import service_account
from googleapiclient.discovery import build

from django.http import JsonResponse
import os,calendar 
from calendar import monthrange

# Obtén el directorio base de tu proyecto Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Construye la ruta al archivo client_scret.json usando BASE_DIR
json_file_path = os.path.join(BASE_DIR, 'core/static/client_scret.json')

# Ahora, puedes usar json_file_path en lugar de 'core/static/client_scret.json' en tu código

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

credentials = service_account.Credentials.from_service_account_file(
    json_file_path, scopes=SCOPES)

service = build('calendar', 'v3', credentials=credentials)



# Create your views here.


@login_required
def employe_list(request):
    empleado = Empleado.objects.all()
    asistencia  = RegistroAsistencia.objects.all()
    cant_regis = RegistroAsistencia.objects.values('empleado').annotate(cantidad_registros=Count('id'))
    listadias = list(range(1, 32))
    array_asistencia = []
    
    

     # Obtener el mes y el año actual
    mes_actual = datetime.now().month
    año_actual = datetime.now().year

    ##
        # Obtener el mes y año actuales
    now = datetime.now()
    month = now.month
    year = now.year

    # Obtener todas las semanas del mes actual
    cal = calendar.monthcalendar(year, month)

    # Obtener los nombres de los días de la semana
    days_of_week = calendar.day_name

    # Obtener el nombre del mes actual
    month_name = now.strftime("%B")

    # Combinar los nombres de los días de la semana, los nombres de los días del mes y el nombre del mes
    table_data = []
    for week in cal:
        week_data = []
        for day in week:
            if day == 0:
                week_data.append(("",""))
            else:
                week_data.append((calendar.day_name[calendar.weekday(year, month, day)], day))
        table_data.append(week_data)
    ##
    # Obtener los nombres de los días de la semana
    dias_de_la_semana = calendar.month_name

    # Obtener los números de los días del mes actual
    dias_del_mes = calendar.monthcalendar(año_actual, mes_actual)
    
    # Obtén el primer y último día del mes actual
    mes_actual = datetime.now().month
    anio_actual = datetime.now().year

    primer_dia_mes = datetime(año_actual, mes_actual, 1, 0, 0, 0).isoformat() + 'Z'

    if mes_actual == 12:
        siguiente_mes = 1
        siguiente_año = anio_actual + 1
    else:
        siguiente_mes = mes_actual + 1
        siguiente_año = anio_actual

    ultimo_dia_mes = (datetime(siguiente_año, siguiente_mes, 1, 0, 0, 0) - timedelta(seconds=1)).isoformat() + 'Z'
    
    # Obtener eventos del calendario
    events_result = service.events().list(calendarId='es.cl#holiday@group.v.calendar.google.com', timeMin=primer_dia_mes,timeMax=ultimo_dia_mes, maxResults=10, singleEvents=True,orderBy='startTime').execute()

    events = events_result.get('items', [])
    #mi_variable_booleana = request.session.get('mi_variable_booleana', True)
    # Procesar los eventos
    
    event_list = []
    if not events:
        event_list.append({'start': 'No hay eventos próximos.', 'summary': ''})
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        summary = event.get('summary', 'No hay resumen disponible.')
        event_list.append({'start': start, 'summary': summary})
    if request.method == "POST":
       
        form = EmpleadoForms(request.POST, request.FILES)
        form2 = AsistenciaForms(request.POST)
        # Obtén el valor actual de la variable booleana de la sesión, si no existe, devuelve True
        
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            messages.success(request, "Empleado Creado Correctamente")
            return redirect('inicio')
        elif form2.is_valid():
            post2 = form2.save(commit=False)
            post2.author = request.user
            post2.published_date = timezone.now()
            post2.save()
            messages.success(request, "Registro de Asistencia Existoso")
            return redirect('inicio')
        else:
            messages.error(request, 'Error: No se puede crear un empleado con el mismo RUT que otro existente o registrar asistencia 2 veces o más el mismo día.')

    else:
        form = EmpleadoForms()
        form2 = AsistenciaForms(request.POST)
    
    tabla_asistencia = generar_tabla_asistencia_mes_actual()


    return render(request,'index.html',{'empleado':empleado,'form':form,'asistencia':asistencia,'listadias':listadias,'cant_regis':cant_regis,'array_asistencia':array_asistencia,'events': event_list,'form2':form2,'table_data':table_data,'tabla_asistencia':tabla_asistencia,'anio_actual':anio_actual,'mes_actual':mes_actual,})


def generar_tabla_asistencia_mes_especifico(mes, anio):
    dias_en_mes = monthrange(anio, mes)[1]

    empleados = Empleado.objects.all()

    tabla_asistencia = []

    for empleado in empleados:
        fila_asistencia = {
            'nombre': empleado.nombre,
            'apellido': empleado.apellido,
            'rut': empleado.rut,
            'imagen': empleado.imageEmp,
            'asistencias': [],
        }
        dias_asistidos = 0

        for dia in range(1, dias_en_mes + 1):
            fecha = datetime(anio, mes, dia)
            asistencia = RegistroAsistencia.objects.filter(empleado=empleado, fecha=fecha).first()

            if asistencia:
                if asistencia.asistencia == 'Presente':
                    fila_asistencia['asistencias'].append('✔')
                elif asistencia.asistencia == 'Ausente':
                    fila_asistencia['asistencias'].append('✘')
                elif asistencia.asistencia == 'Justificado':
                    fila_asistencia['asistencias'].append('J')
            else:
                fila_asistencia['asistencias'].append('null')

            if asistencia and asistencia.asistencia != 'Ausente':
                dias_asistidos += 1

        fila_asistencia['dias_asistidos'] = dias_asistidos
        tabla_asistencia.append(fila_asistencia)

    return tabla_asistencia

def generar_tabla_asistencia_mes_actual():
    mes_actual = datetime.now().month
    anio_actual = datetime.now().year
    dias_en_mes = monthrange(anio_actual, mes_actual)[1]

    empleados = Empleado.objects.all()

    tabla_asistencia = []

    for empleado in empleados:
        fila_asistencia = {
            'nombre': empleado.nombre,
            'apellido': empleado.apellido,
            'rut': empleado.rut,
            'imagen': empleado.imageEmp, 
            'asistencias': [],
            
        }
        dias_asistidos = 0
        

        for dia in range(1, dias_en_mes + 1):
            fecha = datetime(anio_actual, mes_actual, dia)
            asistencia = RegistroAsistencia.objects.filter(empleado=empleado, fecha=fecha).first()

            if asistencia:
                if asistencia.asistencia == 'Presente':
                    fila_asistencia['asistencias'].append('✔')  # Presente se marca con un ticket (✔)
                elif asistencia.asistencia == 'Ausente':
                    fila_asistencia['asistencias'].append('✘')  # Ausente se marca con una X (✘)
                elif asistencia.asistencia == 'Justificado':
                    fila_asistencia['asistencias'].append('J')  # Justificado se marca con una J
            else:
                fila_asistencia['asistencias'].append('null')  # Si es NULL 

            if asistencia and asistencia.asistencia != 'Ausente':
                dias_asistidos += 1

        fila_asistencia['dias_asistidos'] = dias_asistidos
        tabla_asistencia.append(fila_asistencia)

    return tabla_asistencia

#Buscar Asistencia
@login_required
def buscarasistencia(request):
    mes = int(request.GET.get('mes', datetime.now().month))
    anio = int(request.GET.get('anio', datetime.now().year))
    tabla_asistencia = generar_tabla_asistencia_mes_especifico(mes, anio)
    table_data = []
    # Obtener el mes y año actuales
    now = datetime.now()
    year = now.year


    # Obtener todas las semanas del mes elegido
    cal = calendar.monthcalendar(year, mes)

    # Crear una lista para almacenar los datos de la tabla
    table_data = []

    # Iterar a través de las semanas del mes y llenar la tabla
    for week in cal:
        week_data = []
        for day in week:
            if day == 0:
                week_data.append(("",""))
            else:
                week_data.append((calendar.day_name[calendar.weekday(year, mes, day)], day))
        table_data.append(week_data)

    return render(request, 'Asistencia/buscarasistencia.html', {'tabla_asistencia': tabla_asistencia, 'anio_actual': anio,'table_data':table_data,'mes':mes,})



#PROVEEDOR
@login_required
def proveedor(request):
    if request.method == "POST":
        form = ProveedorForms(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            messages.success(request,"Proveedor agregado correctamente.")
            post.published_date = timezone.now()
            post.save()
            return redirect('proveedor')
        else:
            messages.error(request, 'Registrar Proveedor: Esa empresa ya se encuentra registrada.')
    else:
        form = ProveedorForms()
    proveedores = Proveedor.objects.all()
    return render(request,'Proveedores/proveedor.html',{'proveedores':proveedores,'form':form,})

#FINANZAS
@login_required
def finanza(request):
    trans = Transaccion.objects.all()
    if request.method == "POST":
        form = TransaccionForms(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            messages.success(request,"Transación agregada correctamente.")
            post.published_date = timezone.now()
            post.save()
            
            return redirect('finanza')

    else:
        form = TransaccionForms()
        
    monto_cargo = Transaccion.objects.filter(tipo_transaccion='(+) Ingreso (+)').aggregate(Sum('monto'))['monto__sum']
    monto_retiro = Transaccion.objects.filter(tipo_transaccion='(-) Retiro (-)').aggregate(Sum('monto'))['monto__sum']
    cant = Transaccion.objects.count()
    if monto_retiro and monto_cargo:
        monto_total = monto_cargo - monto_retiro
    else:
        monto_total = 0
    
    return render(request,'Finanzas/finanza.html',{'trans':trans,'form':form,'monto_total':monto_total,'monto_cargo':monto_cargo,'monto_retiro':monto_retiro,'cant':cant})



from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


#Empleado
class EmpleadoDetailView(generic.DetailView):
    model = Empleado
    template_name = 'Empleados/empleado_detail.html'
    context_object_name = 'empleado'
    

class EmpleadoListView(generic.ListView):
    model = Empleado


class EmpleadoCreate(CreateView):
    model = Empleado
    fields = '__all__'
    

class EmpleadoUpdate(UpdateView):
    model = Empleado
    template_name = 'Empleados/empleado_mod.html'
    context_object_name = 'empleado'
    form_class = EmpleadoForms
    success_url = reverse_lazy('inicio')
    
    def form_valid(self, form):
        messages.success(self.request, 'Empleado Editado Correctamente')
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super(EmpleadoUpdate, self).get_form_kwargs()
        kwargs['instance'] = self.object  # Pasa la instancia de Empleado al formulario
        return kwargs

class EmpleadoDelete(DeleteView):
    model = Empleado
    template_name = 'Empleados/empleado_confirm_delete.html'
    success_url = reverse_lazy('inicio')
    context_object_name = 'empleado'
    
    def form_valid(self, form):
        messages.success(self.request, 'Empleado Eliminado Correctamente')
        return super().form_valid(form)

#Login
class CustomLoginView(LoginView):
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Bienvenido {self.request.user}')
        return response
    def form_invalid(self, form):
        messages.error(self.request, 'Nombre de usuario o contraseña incorrectos.')
        return super().form_invalid(form)




#Proveedor
class ProveedorDetailView(generic.DetailView):
    model = Proveedor
    template_name = 'Proveedores/proveedor_detail.html'
    context_object_name = 'proveedor'

    
class ProveedorUpdate(UpdateView):
    model = Proveedor
    template_name = 'Proveedores/proveedor_mod.html'
    context_object_name = 'proveedor'
    form_class = ProveedorForms
    success_url = reverse_lazy('proveedor')
    
    def form_valid(self, form):
        messages.success(self.request, 'Proveedor Editado Correctamente')
        return super().form_valid(form)
    
class ProveedorDelete(DeleteView):
    model = Proveedor
    template_name = 'Proveedores/proveedor_confirm_delete.html'
    success_url = reverse_lazy('proveedor')
    context_object_name = 'proveedor'
    
    def form_valid(self, form):
        messages.success(self.request, 'Proveedor Eliminado Correctamente')
        return super().form_valid(form)
    
class TranssaccionDelete(DeleteView):
    model = Transaccion
    template_name = 'Finanzas/finanza_confirm_delete.html'
    success_url = reverse_lazy('finanza')
    context_object_name = 'finanza'
    
    def form_valid(self, form):
        messages.success(self.request, 'Finanza Eliminada Correctamente')
        return super().form_valid(form)