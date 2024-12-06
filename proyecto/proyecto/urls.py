"""
URL configuration for proyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from ERP.views import *

router = DefaultRouter()
router.register(r'paises', PaisViewSet, basename='pais')
router.register(r'departamentos', DepartamentoViewSet, basename='departamento')
router.register(r'ciudades', CiudadViewSet, basename='ciudades')
router.register(r'colonias', ColoniaViewSet, basename='colonia')
router.register(r'direcciones', DireccionViewSet, basename='direccion')
router.register(r'marcas', MarcaViewSet, basename='marca')
router.register(r'tipo-seguro', TipoSeguroViewSet, basename='tiposeguro')
router.register(r'combustibles', CombustibleViewSet, basename='combustible')
router.register(r'modelos', ModeloViewSet, basename='modelo')
router.register(r'estados', EstadoViewSet, basename='estado')
router.register(r'tipo_transaccion', TipoTransaccionViewSet, basename='tipotransaccion')
router.register(r'sucursales', SucursalViewSet, basename='sucursal')
router.register(r'parqueos', ParqueoViewSet, basename='parqueo')
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'empleados', EmpleadoViewSet, basename='empleado')
router.register(r'vehiculos', VehiculoViewSet, basename='vehiculo')
router.register(r'colores', ColorViewSet, basename='color')
router.register(r'rangos', RangoViewSet, basename='rango')
router.register(r'sars', SarViewSet, basename='sar')
router.register(r'detallefactura', DetalleFacturaViewSet, basename='detallefactura')
router.register(r'metodospago', MetodoPagoViewSet, basename='metodopago')
router.register(r'facturas', FacturaViewSet, basename='factura')
router.register(r'pagos', PagoViewSet, basename='pago')
"""
router.register(r'paises', PaisViewSet)
router.register(r'departamento', DepartamentoViewSet)
router.register(r'ciudades', CiudadViewSet)
router.register(r'colonias', ColoniaViewSet)
router.register(r'direcciones', DireccionViewSet)
router.register(r'marcas', MarcaViewSet)
router.register(r'tipo-seguro', TipoSeguroViewSet)
router.register(r'combustible', CombustibleViewSet)
router.register(r'modelo', ModeloViewSet)
router.register(r'estado', EstadoViewSet)
router.register(r'tipo_transaccion', TipoTransaccionViewSet)
router.register(r'sucursal', SucursalViewSet)
router.register(r'parqueo', ParqueoViewSet)
router.register(r'usuario', UsuarioViewSet)
router.register(r'cliente', ClienteViewSet)
router.register(r'empleado', EmpleadoViewSet)
router.register(r'vehiculo', VehiculoViewSet)
router.register(r'color', ColorViewSet)
router.register(r'rango', RangoViewSet)
router.register(r'sar', SarViewSet)
router.register(r'detallefactura', DetalleFacturaViewSet)
router.register(r'metodopago', MetodoPagoViewSet)
router.register(r'factura', FacturaViewSet)
router.register(r'pago', PagoViewSet)
"""
urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += router.urls


