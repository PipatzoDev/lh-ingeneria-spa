from django.urls import path,include
from django.contrib import *
from .views import *
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.employe_list , name='inicio'),
    path('BuscarAsistencia', views.buscarasistencia , name='buscarasistencia'),
    path('login', views.CustomLoginView.as_view(template_name='registration/login.html') , name='login'),
    path('modificarEmpleado/<pk>/', views.EmpleadoUpdate.as_view() , name='empleado-update'),
    path('empleados/<pk>/', EmpleadoDetailView.as_view(), name='empleado-detail'),
    path('empleados/<pk>/eliminar/', EmpleadoDelete.as_view(), name='empleado-delete'),
    path('finanzas', views.finanza, name='finanza'),
    path('finanzas/<pk>/eliminar/', TranssaccionDelete.as_view(), name='trans-delete'),
    path('proveedores', views.proveedor, name='proveedor'),
    path('proveedores/<pk>/', ProveedorDetailView.as_view(), name='proveedor-detail'),
    path('modificarProveedor/<pk>/', views.ProveedorUpdate.as_view() , name='proveedor-update'),
    path('proveedores/<pk>/eliminar/', ProveedorDelete.as_view(), name='proveedor-delete'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html',email_template_name='registration/password_reset_email.html'), name='password_reset'),
    path('reset_password/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset_password/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_password/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    

]
