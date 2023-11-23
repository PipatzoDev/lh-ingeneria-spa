from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import Empleado,RegistroAsistencia,Proveedor,Transaccion

class EmpleadoForms(forms.ModelForm):
    rut = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese Rut del Empleado'}))
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre del Empleado'}))
    apellido = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Apellido del Empleado'}))
    departamento = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Departamento..'}))
    correo_electronico = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Correo del Empleado'}))
    telefono = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese Telefono'}))
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control datetimepicker',}))       
    cargo = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese Cargo'}))
    direccion = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese Dirección del Empleado'}))
    select_gender = (('Mujer', 'Mujer'),('Hombre', 'Hombre'))
    genero = forms.ChoiceField(choices=select_gender,widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = Empleado
        fields = "__all__"
    

        
        

class AsistenciaForms(forms.ModelForm):
    fecha = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control','type':'Date'}))
    select_gender = (('Presente', 'Presente'),('Ausente', 'Ausente'),('Justificado', 'Justificado'))
    asistencia = forms.ChoiceField(choices=select_gender,widget=forms.Select(attrs={'class':'form-control'}))
    hora_entrada = forms.TimeField(widget=forms.DateInput(attrs={'class':'form-control','type':'time'}))
    hora_salida = forms.TimeField(widget=forms.DateInput(attrs={'class':'form-control','type':'time'}))
    
    #empleados = Empleado.objects.all()
    # Crea una lista de tuplas para el ChoiceField
    #choices_list = [(x) for x in empleados]
    #empleado = forms.ChoiceField(choices=[('', 'Selecciona un Empleado')] + choices_list,widget=forms.Select(attrs={'class': 'form-control'}))
    
    queryset = Empleado.objects.all()
    empleado = forms.ModelChoiceField(queryset=queryset,empty_label="Seleccione un Empleado",widget=forms.Select(attrs={'class':'form-control'}))#,input_formats=['%Y-%m-%d'],)
    class Meta:
        model = RegistroAsistencia
        fields = "__all__"
        
      
        
        
class ProveedorForms(forms.ModelForm):
  
    nombre_empresa = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre Empresa'}))
    correo_electronico = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Correo Empresa'}))
    telefono = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese Telefono'}))
    direccion = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese Dirección del Empleado'}))

    
    class Meta:
        model = Proveedor
        fields = "__all__"
        

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result
    
class TransaccionForms(forms.ModelForm):
    select_gender = (('(-) Retiro (-)', '(-) Retiro (-)'),('(+) Cargo (+)', '(+) Cargo (+)'))
    tipo_transaccion = forms.ChoiceField(choices=select_gender,widget=forms.Select(attrs={'class':'form-control'}))
    fecha_transaccion = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control','type':'Date'}))  
    monto = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'number'}))
    descripcion = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese una Descripción'}))
    queryset = Empleado.objects.all()
    queryset2 = Proveedor.objects.all()
    empleado_relacionado = forms.ModelChoiceField(queryset=queryset,empty_label="Seleccione un Empleado",widget=forms.Select(attrs={'class':'form-control'}),required=False)
    proveedor_relacionado = forms.ModelChoiceField(queryset=queryset2,empty_label="Seleccione un Proveedor",widget=forms.Select(attrs={'class':'form-control'}),required=False)
    #archivo = MultipleFileField()
    archivo = forms.FileField(required=False)
    
    """def clean(self):
        cleaned_data = super().clean()
        campo_obligatorio = cleaned_data.get('empleado_relacionado')
        campo_opcional = cleaned_data.get('proveedor_relacionado')

        if not campo_obligatorio and not campo_opcional:
            raise forms.ValidationError("Al menos uno de los campos debe ser llenado.")

        return cleaned_data """
    
    class Meta:
        model = Transaccion
        fields = "__all__"