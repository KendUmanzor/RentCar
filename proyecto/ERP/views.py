from django.shortcuts import render


from .models import *
from .serializer import *
from django.db import connection
from rest_framework.response import Response
from rest_framework import viewsets, status
#from .serializer import PaisSerializer
#
##
###
####
#####
######
#######
########
#########
##########
###########
############
#############
##############
class PaisViewSet(viewsets.ViewSet):
    def list(self, request):
        # Obtener todos los registros de la tabla Pais
        with connection.cursor() as cursor:
            cursor.execute("SELECT Id_pais, Nombre FROM Pais")
            rows = cursor.fetchall()

        # Convertir los resultados en una lista
        paises = [{"id_pais": row[0], "nombre": row[1]} for row in rows]
        return Response(paises)

    def retrieve(self, request, pk=None):
        # Obtener un país específico por su ID
        with connection.cursor() as cursor:
            cursor.execute("SELECT Id_pais, Nombre FROM Pais WHERE Id_pais = %s", [pk])
            row = cursor.fetchone()

        if row:
            pais = {"id_pais": row[0], "nombre": row[1]}
            return Response(pais)
        return Response({"error": "País no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = PaisSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            # Verificar si el ID del país ya existe
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM Pais WHERE Id_pais = %s", [data["id_pais"]])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El ID del país ya existe"}, status=status.HTTP_400_BAD_REQUEST)

            # Verificar si el nombre del país ya existe
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM Pais WHERE Nombre = %s", [data["nombre"]])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El nombre del país ya existe"}, status=status.HTTP_400_BAD_REQUEST)

            # Insertar el nuevo país
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Pais (Id_pais, Nombre) VALUES (%s, %s)",
                    [data["id_pais"], data["nombre"]],
                )
            return Response({"message": "País creado correctamente"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        serializer = PaisSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            # Verificar si el país existe antes de actualizar
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM Pais WHERE Id_pais = %s", [pk])
                if cursor.fetchone()[0] == 0:
                    return Response({"error": "País no encontrado"}, status=status.HTTP_404_NOT_FOUND)

            # Actualizar el país
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE Pais SET Nombre = %s WHERE Id_pais = %s",
                    [data["nombre"], pk],
                )
            return Response({"message": "País actualizado correctamente"})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        # Verificar si el país existe antes de eliminar
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM Pais WHERE Id_pais = %s", [pk])
            if cursor.fetchone()[0] == 0:
                return Response({"error": "País no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # Eliminar el país
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Pais WHERE Id_pais = %s", [pk])
        return Response({"message": "País eliminado correctamente"})
#
##
###
####
#####
######
#######
########
#########
##########
###########
############
#############
##############
class DepartamentoViewSet(viewsets.ViewSet):
    
    # Listar todos los departamentos
    def list(self, request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT Id_departamento, Nombre, Id_pais FROM Departamento")
            rows = cursor.fetchall()

        # Convertir los resultados en una lista de diccionarios
        departamentos = [{"id_departamento": row[0], "nombre": row[1], "id_pais": row[2]} for row in rows]
        return Response(departamentos)

    # Obtener un departamento específico por ID
    def retrieve(self, request, pk=None):
        with connection.cursor() as cursor:
            cursor.execute("SELECT Id_departamento, Nombre, Id_pais FROM Departamento WHERE Id_departamento = %s", [pk])
            row = cursor.fetchone()

        if row:
            departamento = {"id_departamento": row[0], "nombre": row[1], "id_pais": row[2]}
            return Response(departamento)
        else:
            return Response({"error": "Departamento no encontrado."}, status=status.HTTP_404_NOT_FOUND)

    # Crear un nuevo departamento
    def create(self, request):
        # Deserializar los datos recibidos
        serializer = DepartamentoSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            id_departamento = data['id_departamento']
            nombre = data['nombre']
            id_pais = data['id_pais']

            # Validar que el país exista
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM Pais WHERE Id_pais = %s", [id_pais])
                if cursor.fetchone()[0] == 0:
                    return Response({"error": "El país especificado no existe."}, status=status.HTTP_400_BAD_REQUEST)

                # Validar que no exista un departamento con el mismo nombre y país
                cursor.execute(
                    "SELECT COUNT(*) FROM Departamento WHERE Nombre = %s AND Id_pais = %s",
                    [nombre, id_pais]
                )
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "Ya existe un departamento con ese nombre en este país."}, status=status.HTTP_400_BAD_REQUEST)

            # Si pasa la validación, insertar el nuevo departamento
            with connection.cursor() as cursor:
                try:
                    cursor.execute(
                        "INSERT INTO Departamento (Id_departamento, Nombre, Id_pais) VALUES (%s, %s, %s)",
                        [id_departamento, nombre, id_pais]
                    )
                    connection.commit()
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"mensaje": "Departamento creado exitosamente."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Actualizar un departamento existente
    def update(self, request, pk=None):
        with connection.cursor() as cursor:
            cursor.execute("SELECT Id_departamento, Nombre, Id_pais FROM Departamento WHERE Id_departamento = %s", [pk])
            row = cursor.fetchone()

        if not row:
            return Response({"error": "Departamento no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Deserializar los datos recibidos para actualizar
        serializer = DepartamentoSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            id_departamento = data['id_departamento']
            nombre = data['nombre']
            id_pais = data['id_pais']

            # Validar que el país exista
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM Pais WHERE Id_pais = %s", [id_pais])
                if cursor.fetchone()[0] == 0:
                    return Response({"error": "El país especificado no existe."}, status=status.HTTP_400_BAD_REQUEST)

                # Validar que no exista un departamento con el mismo nombre y país
                cursor.execute(
                    "SELECT COUNT(*) FROM Departamento WHERE Nombre = %s AND Id_pais = %s AND Id_departamento != %s",
                    [nombre, id_pais, pk]
                )
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "Ya existe un departamento con ese nombre en este país."}, status=status.HTTP_400_BAD_REQUEST)

            # Si pasa la validación, actualizar el departamento
            with connection.cursor() as cursor:
                try:
                    cursor.execute(
                        "UPDATE Departamento SET Nombre = %s, Id_pais = %s WHERE Id_departamento = %s",
                        [nombre, id_pais, pk]
                    )
                    connection.commit()
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"mensaje": "Departamento actualizado exitosamente."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Eliminar un departamento
    def destroy(self, request, pk=None):
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM Departamento WHERE Id_departamento = %s", [pk])
            if cursor.fetchone()[0] == 0:
                return Response({"error": "Departamento no encontrado."}, status=status.HTTP_404_NOT_FOUND)

            try:
                cursor.execute("DELETE FROM Departamento WHERE Id_departamento = %s", [pk])
                connection.commit()
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"mensaje": "Departamento eliminado exitosamente."}, status=status.HTTP_204_NO_CONTENT)
""""
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
"""
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
"""
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
"""
class EmpleadoViewSet(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer
"""
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

    """