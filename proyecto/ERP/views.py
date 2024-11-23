from django.shortcuts import render

from rest_framework import viewsets
from .models import *
from .serializer import *
"""""
class PaisViewSet(viewsets.ViewSet):
    
    def list(self, request):
        paises_data = [pais.__dict__ for pais in self.paises]  
        return Response(paises_data)

    def create(self, request):
        data = request.data
        nuevo_pais = Pais(data['id_pais'], data['nombre'])
        self.paises.append(nuevo_pais) 
        return Response(data, status=201)

    def update(self, request, pk=None):
        data = request.data
        pais = next((pais for pais in self.paises if pais.id_pais == int(pk)), None)
        if pais:
            pais.nombre = data['nombre']
            return Response(data)
        return Response({"detail": "."}, status=404)

    def destroy(self, request, pk=None):
        pais = next((pais for pais in self.paises if pais.id_pais == int(pk)), None)
        if pais:
            self.paises.remove(pais)
            return Response(status=204)
        return Response({"detail": "."}, status=404)
"""

class PaisViewSet(viewsets.ModelViewSet):
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer

class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer

class CiudadViewSet(viewsets.ModelViewSet):
    queryset = Ciudad.objects.all()
    serializer_class = CiudadSerializer

class ColoniaViewSet(viewsets.ModelViewSet):
    queryset = Colonia.objects.all()
    serializer_class = ColoniaSerializer

class DireccionViewSet(viewsets.ModelViewSet):
    queryset = Direccion.objects.all()
    serializer_class = DireccionSerializer

class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer

class TipoSeguroViewSet(viewsets.ModelViewSet):
    queryset = TipoSeguro.objects.all()
    serializer_class = TipoSeguroSerializer

class CombustibleViewSet(viewsets.ModelViewSet):
    queryset = Combustible.objects.all()
    serializer_class = CombustibleSerializer

class EstadoViewSet(viewsets.ModelViewSet):
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer

class ModeloViewSet(viewsets.ModelViewSet):
    queryset = Modelo.objects.all()
    serializer_class = ModeloSerializer

class TipoTransaccionViewSet(viewsets.ModelViewSet):
    queryset = TipoTransaccion.objects.all()
    serializer_class = TipoTransaccionSerializer

class SucursalViewSet(viewsets.ModelViewSet):
    queryset = Sucursal.objects.all()
    serializer_class = SucursalSerializer

class ParqueoViewSet(viewsets.ModelViewSet):
    queryset = Parqueo.objects.all()
    serializer_class = ParqueoSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class EmpleadoViewSet(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer

class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer

class RangoViewSet(viewsets.ModelViewSet):
    queryset = Rango.objects.all()
    serializer_class = RangoSerializer

class SarViewSet(viewsets.ModelViewSet):
    queryset = Sar.objects.all()
    serializer_class = SarSerializer

class DetalleFacturaViewSet(viewsets.ModelViewSet):
    queryset = DetalleFactura.objects.all()
    serializer_class = DetalleFacturaSerializer

class MetodoPagoViewSet(viewsets.ModelViewSet):
    queryset = MetodoPago.objects.all()
    serializer_class = MetodoPagoSerializer

class FacturaViewSet(viewsets.ModelViewSet):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer

class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer