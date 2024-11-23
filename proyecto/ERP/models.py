
from django.db import models

class Pais(models.Model):
    id_pais = models.IntegerField(db_column='Id_pais', primary_key=True)  
    nombre = models.CharField(db_column='Nombre', unique=True, max_length=50, blank=True, null=True)  

    class Meta:
        db_table = 'Pais'

class Departamento(models.Model):
    id_departamento = models.IntegerField(db_column='Id_departamento', primary_key=True)  
    nombre = models.CharField(db_column='Nombre', max_length=50, blank=True, null=True)  
    id_pais = models.ForeignKey('Pais', db_column='Id_pais', blank=True, null=True)  

    class Meta:
        db_table = 'Departamento'
        unique_together = (('id_pais', 'nombre'),)


class Ciudad(models.Model):
    id_ciudad = models.IntegerField(db_column='Id_ciudad', primary_key=True)  
    nombre = models.CharField(db_column='Nombre', unique=True, max_length=50, blank=True, null=True)  
    id_pais = models.ForeignKey('Pais', db_column='Id_pais', blank=True, null=True)  
    id_departamento = models.ForeignKey('Departamento',  db_column='Id_departamento', blank=True, null=True)  

    class Meta:
        db_table = 'Ciudad'
        unique_together = (('id_departamento', 'nombre'),)


class Cliente(models.Model):
    id_cliente = models.IntegerField(db_column='Id_cliente', primary_key=True)  
    id_usuario = models.ForeignKey('Usuario', db_column='Id_usuario', blank=True, null=True)  

    class Meta:
        db_table = 'Cliente'


class Colonia(models.Model):
    id_colonia = models.IntegerField(db_column='Id_colonia', primary_key=True)  
    nombre = models.CharField(db_column='Nombre', unique=True, max_length=50, blank=True, null=True)  
    id_pais = models.ForeignKey('Pais', db_column='Id_pais', blank=True, null=True)  
    id_departamento = models.ForeignKey('Departamento', db_column='Id_departamento', blank=True, null=True)  
    id_ciudad = models.ForeignKey(Ciudad, db_column='Id_ciudad', blank=True, null=True)  

    class Meta:
        db_table = 'Colonia'
        unique_together = (('id_ciudad', 'nombre'),)


class Color(models.Model):
    id_color = models.IntegerField(db_column='Id_color', primary_key=True)  
    nombre = models.CharField(db_column='Nombre', unique=True, max_length=50, blank=True, null=True)  
    id_vehiculo = models.ForeignKey('Vehiculo', db_column='Id_vehiculo', blank=True, null=True)  

    class Meta:
        db_table = 'Color'
        unique_together = (('nombre', 'id_vehiculo'),)


class Combustible(models.Model):
    id_combustible = models.IntegerField(db_column='Id_combustible', primary_key=True)  
    nombre = models.CharField(db_column='Nombre', unique=True, max_length=50, blank=True, null=True)  

    class Meta:
        db_table = 'Combustible'


class Departamento(models.Model):
    id_departamento = models.IntegerField(db_column='Id_departamento', primary_key=True)  
    nombre = models.CharField(db_column='Nombre', max_length=50, blank=True, null=True)  
    id_pais = models.ForeignKey('Pais', db_column='Id_pais', blank=True, null=True)  

    class Meta:
        db_table = 'Departamento'
        unique_together = (('id_pais', 'nombre'),)


class DetalleFactura(models.Model):
    id_detalle_factura = models.IntegerField(db_column='Id_detalle_factura', primary_key=True)  
    descuento = models.IntegerField(blank=True, null=True)
    id_vehiculo = models.ForeignKey('Vehiculo', db_column='Id_vehiculo', blank=True, null=True)  

    class Meta:
        db_table = 'Detalle_factura'


class Direccion(models.Model):
    id_direccion = models.IntegerField(db_column='Id_direccion', primary_key=True)  
    d_pais = models.ForeignKey('Pais', db_column='d_pais', blank=True, null=True)
    id_departamento = models.ForeignKey(Departamento, db_column='Id_departamento', blank=True, null=True)  
    id_ciudad = models.ForeignKey(Ciudad, db_column='Id_ciudad', blank=True, null=True)  
    id_colonia = models.ForeignKey(Colonia, db_column='Id_colonia', blank=True, null=True)  

    class Meta:
        db_table = 'Direccion'


class Empleado(models.Model):
    id_empleado = models.IntegerField(db_column='Id_Empleado', primary_key=True)  
    id_usuario = models.ForeignKey('Usuario', db_column='Id_usuario', blank=True, null=True)  
    id_sucursal = models.ForeignKey('Sucursal', db_column='Id_sucursal', blank=True, null=True)  

    class Meta:
        db_table = 'Empleado'


class Estado(models.Model):
    id_estado = models.IntegerField(db_column='Id_estado', primary_key=True)  
    nombre = models.CharField(db_column='Nombre', unique=True, max_length=50, blank=True, null=True)  

    class Meta:
        db_table = 'Estado'


class Factura(models.Model):
    id_factura = models.IntegerField(db_column='Id_factura', primary_key=True)  
    fecha_emision = models.DateField(db_column='Fecha_emision', blank=True, null=True)  
    total = models.IntegerField(db_column='Total', blank=True, null=True)  
    id_detalle_factura = models.ForeignKey(DetalleFactura, db_column='Id_detalle_factura', blank=True, null=True)  
    id_tipo_transaccion = models.ForeignKey('TipoTransaccion', db_column='Id_tipo_transaccion', blank=True, null=True)  
    id_cliente = models.ForeignKey(Cliente, db_column='Id_cliente', blank=True, null=True)  
    id_empleado = models.ForeignKey(Empleado, db_column='Id_empleado', blank=True, null=True)  
    id_sar = models.ForeignKey('Sar', db_column='Id_sar', blank=True, null=True)  

    class Meta:
        db_table = 'Factura'


class Marca(models.Model):
    id_marca = models.IntegerField(db_column='Id_marca', primary_key=True)  
    nombre = models.CharField(db_column='Nombre', unique=True, max_length=50, blank=True, null=True)  

    class Meta:
        db_table = 'Marca'


class MetodoPago(models.Model):
    id_metodo_pago = models.IntegerField(db_column='Id_metodo_pago', primary_key=True)  
    nombre = models.CharField(db_column='Nombre', unique=True, max_length=50, blank=True, null=True)  

    class Meta:
        db_table = 'Metodo_pago'


class Modelo(models.Model):
    id_modelo = models.IntegerField(db_column='Id_modelo', primary_key=True)  
    nombre = models.CharField(db_column='Nombre', unique=True, max_length=50, blank=True, null=True)  
    id_marca = models.ForeignKey(Marca, db_column='Id_marca', blank=True, null=True)  

    class Meta:
        db_table = 'Modelo'


class Pago(models.Model):
    id_pago = models.IntegerField(db_column='Id_pago', primary_key=True)  
    estado = models.BooleanField(db_column='Estado', blank=True, null=True)  
    monto = models.IntegerField(db_column='Monto', blank=True, null=True)  
    fecha_pago = models.DateField(blank=True, null=True)
    id_factura = models.ForeignKey(Factura, db_column='Id_factura', blank=True, null=True)  
    id_metodo_pago = models.ForeignKey(MetodoPago, db_column='Id_metodo_pago', blank=True, null=True)  

    class Meta:
        db_table = 'Pago'


class Pais(models.Model):
    id_pais = models.IntegerField(db_column='Id_pais', primary_key=True)  
    nombre = models.CharField(db_column='Nombre', unique=True, max_length=50, blank=True, null=True)  

    class Meta:
        db_table = 'Pais'


class Parqueo(models.Model):
    id_parqueo = models.IntegerField(db_column='Id_parqueo', primary_key=True)  
    lote = models.IntegerField(db_column='Lote', unique=True, blank=True, null=True)  
    referencia = models.CharField(db_column='Referencia', max_length=100, blank=True, null=True)  
    id_sucursal = models.ForeignKey('Sucursal', db_column='Id_sucursal', blank=True, null=True)  

    class Meta:
        db_table = 'Parqueo'


class Rango(models.Model):
    id_rango = models.IntegerField(db_column='Id_rango', primary_key=True)  
    inicio = models.IntegerField(db_column='Inicio', unique=True, blank=True, null=True)  
    fin = models.IntegerField(db_column='Fin', unique=True, blank=True, null=True)  

    class Meta:
        db_table = 'Rango'
        unique_together = (('inicio', 'fin'),)


class Sar(models.Model):
    id_sar = models.IntegerField(db_column='Id_sar', primary_key=True)  
    fecha_limite = models.DateField(db_column='Fecha_limite', blank=True, null=True)  
    num_trans = models.IntegerField(db_column='Num_trans', blank=True, null=True)  
    id_tipo_transaccion = models.ForeignKey('TipoTransaccion', db_column='Id_tipo_transaccion', blank=True, null=True)  
    id_rango = models.ForeignKey(Rango, db_column='Id_rango', blank=True, null=True)  
    id_sucursal = models.ForeignKey('Sucursal', db_column='Id_sucursal', blank=True, null=True)  

    class Meta:
        db_table = 'SAR'


class Sucursal(models.Model):
    id_sucursal = models.IntegerField(db_column='Id_sucursal', primary_key=True)  
    nombre = models.CharField(db_column='Nombre', unique=True, max_length=50, blank=True, null=True)  
    telefono = models.IntegerField(blank=True, null=True)
    id_direccion = models.ForeignKey(Direccion, db_column='Id_direccion', blank=True, null=True)  

    class Meta:
        db_table = 'Sucursal'


class TipoSeguro(models.Model):
    id_tipo_seguro = models.IntegerField(db_column='Id_tipo_seguro', primary_key=True)  
    nombre = models.CharField(db_column='Nombre', unique=True, max_length=50, blank=True, null=True)  

    class Meta:
        db_table = 'Tipo_seguro'

class TipoTransaccion(models.Model):
    id_tipo_transaccion = models.IntegerField(db_column='Id_tipo_transaccion', primary_key=True)  
    nombre = models.CharField(db_column='Nombre', unique=True, max_length=50, blank=True, null=True)  

    class Meta:
        db_table = 'Tipo_transaccion'


class Usuario(models.Model):
    id_usuario = models.IntegerField(db_column='Id_usuario', primary_key=True)  
    nombre = models.CharField(db_column='Nombre', max_length=50, blank=True, null=True)  
    nombre_pila = models.CharField(db_column='Nombre_pila', max_length=50, blank=True, null=True)  
    apellido = models.CharField(db_column='Apellido', max_length=50, blank=True, null=True)  
    apellido_pila = models.CharField(db_column='Apellido_pila', max_length=50, blank=True, null=True)  
    correo = models.CharField(db_column='Correo', unique=True, max_length=50, blank=True, null=True)  
    telefono = models.IntegerField(db_column='Telefono', blank=True, null=True)  
    contrasena = models.CharField(db_column='Contrasena', max_length=50, blank=True, null=True)  
    fecha_ingreso = models.DateField(blank=True, null=True)
    fecha_salida = models.DateField(blank=True, null=True)
    id_direccion = models.ForeignKey(Direccion, db_column='Id_direccion', blank=True, null=True)  

    class Meta:
        db_table = 'Usuario'


class Vehiculo(models.Model):
    id_vehiculo = models.IntegerField(db_column='Id_Vehiculo', primary_key=True)  
    ano = models.IntegerField(db_column='Ano', blank=True, null=True)  
    vin = models.IntegerField(db_column='Vin', unique=True, blank=True, null=True)  
    motor = models.IntegerField(db_column='Motor', blank=True, null=True)  
    matricula = models.CharField(db_column='Matricula', unique=True, max_length=50, blank=True, null=True)  
    disponibilidad = models.BooleanField(db_column='Disponibilidad', blank=True, null=True)  
    precio = models.IntegerField(db_column='Precio', blank=True, null=True)  
    id_marca = models.ForeignKey(Marca, db_column='Id_marca', blank=True, null=True)  
    id_modelo = models.ForeignKey(Modelo, db_column='Id_modelo', blank=True, null=True)  
    id_estado = models.ForeignKey(Estado, db_column='Id_estado', blank=True, null=True)  
    id_tipo_transaccion = models.ForeignKey(TipoTransaccion, db_column='Id_tipo_transaccion', blank=True, null=True)  
    id_combustible = models.ForeignKey(Combustible, db_column='Id_combustible', blank=True, null=True)  
    id_sucursal = models.ForeignKey(Sucursal, db_column='Id_sucursal', blank=True, null=True)  
    id_parqueo = models.ForeignKey(Parqueo, db_column='Id_Parqueo', blank=True, null=True)  

    class Meta:
        db_table = 'Vehiculo'
