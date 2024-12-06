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
    nombre = serializers.CharField(max_length=50, allow_blank=True, allow_null=True)
    id_pais = serializers.IntegerField(allow_null=True)
    id_departamento = serializers.IntegerField(allow_null=True)

class ColoniaSerializer(serializers.Serializer):
    id_colonia = serializers.IntegerField()
    nombre = serializers.CharField(max_length=50, allow_blank=True, allow_null=True)
    id_pais = serializers.IntegerField(allow_null=True)
    id_departamento = serializers.IntegerField(allow_null=True)
    id_ciudad = serializers.IntegerField(allow_null=True)

class DireccionSerializer(serializers.Serializer):
    id_direccion = serializers.IntegerField()
    id_pais = serializers.IntegerField(allow_null=True)
    id_departamento = serializers.IntegerField(allow_null=True)
    id_ciudad = serializers.IntegerField(allow_null=True)
    id_colonia = serializers.IntegerField(allow_null=True)

class MarcaSerializer(serializers.Serializer):
    id_marca = serializers.IntegerField()
    nombre = serializers.CharField(max_length=50, allow_blank=True, allow_null=True)

class TipoSeguroSerializer(serializers.Serializer):
    id_tipo_seguro = serializers.IntegerField()
    nombre = serializers.CharField(max_length=50, allow_blank=True, allow_null=True)

class CombustibleSerializer(serializers.Serializer):
    id_combustible = serializers.IntegerField()
    nombre = serializers.CharField(max_length=50, allow_blank=True, allow_null=True)


class EstadoSerializer(serializers.Serializer):
    id_estado = serializers.IntegerField()
    nombre = serializers.CharField(max_length=50, allow_blank=True, allow_null=True)

class ModeloSerializer(serializers.Serializer):
    id_modelo = serializers.IntegerField()
    nombre = serializers.CharField(max_length=50, allow_blank=True, allow_null=True)
    id_marca = serializers.IntegerField()

class TipoTransaccionSerializer(serializers.Serializer):
    id_tipo_transaccion = serializers.IntegerField()
    nombre = serializers.CharField(max_length=50, allow_blank=True, allow_null=True)

class SucursalSerializer(serializers.Serializer):
    id_sucursal = serializers.IntegerField()
    nombre = serializers.CharField(max_length=50, allow_blank=True, allow_null=True)
    telefono = serializers.IntegerField(allow_null=True)
    id_direccion = serializers.IntegerField()


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
"""
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'
"""
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