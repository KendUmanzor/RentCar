from rest_framework import serializers
#from django.db import models
from .models import *


class PaisSerializer(serializers.Serializer):
    id_pais = serializers.IntegerField() 
    nombre = serializers.CharField(max_length=50, allow_blank=False, allow_null=False)

class DepartamentoSerializer(serializers.Serializer):
    id_departamento = serializers.IntegerField()
    nombre = serializers.CharField(max_length=50, allow_blank=False, allow_null=False)
    id_pais = serializers.IntegerField(allow_null=False)

class CiudadSerializer(serializers.Serializer):
    id_ciudad = serializers.IntegerField()
    nombre = serializers.CharField(max_length=50, allow_blank=False, allow_null=False)
    id_pais = serializers.IntegerField(allow_null=False)
    id_departamento = serializers.IntegerField(allow_null=False)

class ColoniaSerializer(serializers.Serializer):
    id_colonia = serializers.IntegerField()
    nombre = serializers.CharField(max_length=50, allow_blank=False, allow_null=False)
    id_pais = serializers.IntegerField(allow_null=False)
    id_departamento = serializers.IntegerField(allow_null=False)
    id_ciudad = serializers.IntegerField(allow_null=False)

class DireccionSerializer(serializers.Serializer):
    id_direccion = serializers.IntegerField()
    id_pais = serializers.IntegerField(allow_null=False)
    id_departamento = serializers.IntegerField(allow_null=False)
    id_ciudad = serializers.IntegerField(allow_null=False)
    id_colonia = serializers.IntegerField(allow_null=False)

class MarcaSerializer(serializers.Serializer):
    id_marca = serializers.IntegerField()
    nombre = serializers.CharField(max_length=50, allow_blank=False, allow_null=False)

class TipoSeguroSerializer(serializers.Serializer):
    id_tipo_seguro = serializers.IntegerField()
    nombre = serializers.CharField(max_length=50, allow_blank=False, allow_null=False)

class CombustibleSerializer(serializers.Serializer):
    id_combustible = serializers.IntegerField()
    nombre = serializers.CharField(max_length=50, allow_blank=False, allow_null=False)


class EstadoSerializer(serializers.Serializer):
    id_estado = serializers.IntegerField()
    nombre = serializers.CharField(max_length=50, allow_blank=False, allow_null=False)

class ModeloSerializer(serializers.Serializer):
    id_modelo = serializers.IntegerField()
    nombre = serializers.CharField(max_length=50, allow_blank=False, allow_null=False)
    id_marca = serializers.IntegerField()

class TipoTransaccionSerializer(serializers.Serializer):
    id_tipo_transaccion = serializers.IntegerField()
    nombre = serializers.CharField(max_length=50, allow_blank=False, allow_null=False)

class SucursalSerializer(serializers.Serializer):
    id_sucursal = serializers.IntegerField()
    nombre = serializers.CharField(max_length=50, allow_blank=False, allow_null=False)
    telefono = serializers.IntegerField(allow_null=False)
    id_direccion = serializers.IntegerField()

class ParqueoSerializer(serializers.Serializer):
    id_parqueo = serializers.IntegerField()
    lote = serializers.IntegerField(allow_null=False)
    referencia = serializers.CharField(max_length=100, allow_blank=False, allow_null=False)
    id_sucursal = serializers.IntegerField()

class VehiculoSerializer(serializers.Serializer):
    id_vehiculo = serializers.IntegerField()
    ano = serializers.IntegerField(allow_null=False)
    vin = serializers.IntegerField(allow_null=False)
    motor = serializers.IntegerField(allow_null=False)
    matricula = serializers.CharField(max_length=50, allow_blank=False, allow_null=False)
    disponibilidad = serializers.BooleanField(allow_null=False)
    precio = serializers.IntegerField(allow_null=False)
    id_marca = serializers.IntegerField()
    id_modelo = serializers.IntegerField()
    id_estado = serializers.IntegerField()
    id_tipo_transaccion = serializers.IntegerField()
    id_combustible = serializers.IntegerField()
    id_sucursal = serializers.IntegerField()
    id_parqueo = serializers.IntegerField()

class ColorSerializer(serializers.Serializer):
    id_color = serializers.IntegerField()
    nombre = serializers.CharField(max_length=50, allow_blank=False, allow_null=False)
    id_vehiculo = serializers.IntegerField(allow_null=False)


class RangoSerializer(serializers.Serializer):
    id_rango = serializers.IntegerField()
    inicio = serializers.IntegerField(allow_null=False)
    fin = serializers.IntegerField(allow_null=False)


class SarSerializer(serializers.Serializer):
    id_sar = serializers.IntegerField()
    fecha_limite = serializers.DateField(allow_null=False)
    num_trans = serializers.IntegerField(allow_null=False)
    id_tipo_transaccion = serializers.IntegerField(allow_null=False)
    id_rango = serializers.IntegerField(allow_null=False)
    id_sucursal = serializers.IntegerField(allow_null=False)

class DetalleFacturaSerializer(serializers.Serializer):
    id_detalle_factura = serializers.IntegerField()
    descuento = serializers.IntegerField(allow_null=False)
    id_vehiculo = serializers.IntegerField(allow_null=False)

class MetodoPagoSerializer(serializers.Serializer):
    id_metodo_pago = serializers.IntegerField()
    nombre = serializers.CharField(max_length=50, allow_blank=False, required=False)

class FacturaSerializer(serializers.Serializer):
    id_factura = serializers.IntegerField()
    fecha_emision = serializers.DateField(allow_null=False)
    total = serializers.IntegerField(allow_null=False)
    id_detalle_factura = serializers.IntegerField(allow_null=False)
    id_tipo_transaccion = serializers.IntegerField(allow_null=False)
    id_cliente = serializers.IntegerField(allow_null=False)
    id_empleado = serializers.IntegerField(allow_null=False)
    id_sar = serializers.IntegerField(allow_null=False)

class PagoSerializer(serializers.Serializer):
    id_pago = serializers.IntegerField()
    estado = serializers.BooleanField(allow_null=False)
    monto = serializers.IntegerField(allow_null=False)
    fecha_pago = serializers.DateField(allow_null=False)
    id_factura = serializers.IntegerField(allow_null=False)
    id_metodo_pago = serializers.IntegerField(allow_null=False)


"""
class PaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pais
        fields = '__all__'

class DepartamentoSerializer(serializers.ModelSerializer):
    id_pais = serializers.PrimaryKeyRelatedField(queryset=Pais.objects.all())  

    class Meta:
        model = Departamento
        fields = '__all__'


class CiudadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ciudad
        fields = '__all__'  

class ColoniaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colonia
        fields = '__all__'

class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields = '__all__'

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__'

class TipoSeguroSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoSeguro
        fields = '__all__'

class CombustibleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Combustible
        fields = '__all__'

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = '__all__'

class ModeloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modelo
        fields = '__all__'

class TipoTransaccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoTransaccion
        fields = '__all__'

class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = '__all__'

class ParqueoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parqueo
        fields = '__all__'
"""
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = '__all__'
"""
class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = '__all__'

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'

class RangoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rango
        fields = '__all__'

class SarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sar
        fields = '__all__'

class DetalleFacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleFactura
        fields = '__all__'

class MetodoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetodoPago
        fields = '__all__'

class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = '__all__'

class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'

"""