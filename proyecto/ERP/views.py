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
class CiudadViewSet(viewsets.ViewSet):
    def list(self, request):
        # Obtener todas las ciudades
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Id_ciudad, Nombre, Id_pais, Id_departamento 
                FROM Ciudad
            """)
            rows = cursor.fetchall()

        ciudades = [
            {
                "id_ciudad": row[0],
                "nombre": row[1],
                "id_pais": row[2],
                "id_departamento": row[3],
            }
            for row in rows
        ]
        return Response(ciudades)

    def retrieve(self, request, pk=None):
        # Obtener una ciudad específica
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Id_ciudad, Nombre, Id_pais, Id_departamento 
                FROM Ciudad
                WHERE Id_ciudad = %s
            """, [pk])
            row = cursor.fetchone()

        if not row:
            return Response({"error": "Ciudad no encontrada"}, status=404)

        ciudad = {
            "id_ciudad": row[0],
            "nombre": row[1],
            "id_pais": row[2],
            "id_departamento": row[3],
        }
        return Response(ciudad)

    def create(self, request):
        data = request.data
        serializer = CiudadSerializer(data=data)
        if serializer.is_valid():
            # Validar existencia única
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM Ciudad 
                    WHERE Id_departamento = %s AND Nombre = %s
                """, [data["id_departamento"], data["nombre"]])
                exists = cursor.fetchone()[0]

                if exists > 0:
                    return Response(
                        {"error": "Ya existe una ciudad con ese nombre en el departamento"},
                        status=400
                    )

                # Insertar la nueva ciudad
                cursor.execute("""
                    INSERT INTO Ciudad (Id_ciudad, Nombre, Id_pais, Id_departamento)
                    VALUES (%s, %s, %s, %s)
                """, [
                    data["id_ciudad"],
                    data["nombre"],
                    data["id_pais"],
                    data["id_departamento"],
                ])
            return Response({"message": "Ciudad creada exitosamente"}, status=201)

        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        data = request.data
        serializer = CiudadSerializer(data=data)
        if serializer.is_valid():
            with connection.cursor() as cursor:
                # Validar existencia única si el nombre o departamento cambian
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM Ciudad 
                    WHERE Id_departamento = %s AND Nombre = %s AND Id_ciudad != %s
                """, [data["id_departamento"], data["nombre"], pk])
                exists = cursor.fetchone()[0]

                if exists > 0:
                    return Response(
                        {"error": "Ya existe una ciudad con ese nombre en el departamento"},
                        status=400
                    )

                # Actualizar los datos
                cursor.execute("""
                    UPDATE Ciudad
                    SET Nombre = %s, Id_pais = %s, Id_departamento = %s
                    WHERE Id_ciudad = %s
                """, [
                    data["nombre"],
                    data["id_pais"],
                    data["id_departamento"],
                    pk,
                ])
            return Response({"message": "Ciudad actualizada exitosamente"}, status=200)

        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        # Eliminar una ciudad
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Ciudad WHERE Id_ciudad = %s", [pk])
        return Response({"message": "Ciudad eliminada exitosamente"}, status=204)
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
class ColoniaViewSet(viewsets.ViewSet):
    def list(self, request):
        # Obtener todas las colonias
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Id_colonia, Nombre, Id_pais, Id_departamento, Id_ciudad
                FROM Colonia
            """)
            rows = cursor.fetchall()

        colonias = [
            {
                "id_colonia": row[0],
                "nombre": row[1],
                "id_pais": row[2],
                "id_departamento": row[3],
                "id_ciudad": row[4],
            }
            for row in rows
        ]
        return Response(colonias)

    def retrieve(self, request, pk=None):
        # Obtener una colonia específica
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Id_colonia, Nombre, Id_pais, Id_departamento, Id_ciudad
                FROM Colonia
                WHERE Id_colonia = %s
            """, [pk])
            row = cursor.fetchone()

        if not row:
            return Response({"error": "Colonia no encontrada"}, status=404)

        colonia = {
            "id_colonia": row[0],
            "nombre": row[1],
            "id_pais": row[2],
            "id_departamento": row[3],
            "id_ciudad": row[4],
        }
        return Response(colonia)

    def create(self, request):
        data = request.data
        serializer = ColoniaSerializer(data=data)
        if serializer.is_valid():
            # Validar unicidad
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM Colonia
                    WHERE Id_ciudad = %s AND Nombre = %s
                """, [data["id_ciudad"], data["nombre"]])
                exists = cursor.fetchone()[0]

                if exists > 0:
                    return Response(
                        {"error": "Ya existe una colonia con ese nombre en la ciudad especificada"},
                        status=400
                    )

                # Insertar nueva colonia
                cursor.execute("""
                    INSERT INTO Colonia (Id_colonia, Nombre, Id_pais, Id_departamento, Id_ciudad)
                    VALUES (%s, %s, %s, %s, %s)
                """, [
                    data["id_colonia"],
                    data["nombre"],
                    data["id_pais"],
                    data["id_departamento"],
                    data["id_ciudad"],
                ])
            return Response({"message": "Colonia creada exitosamente"}, status=201)

        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        data = request.data
        serializer = ColoniaSerializer(data=data)
        if serializer.is_valid():
            with connection.cursor() as cursor:
                # Validar unicidad
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM Colonia
                    WHERE Id_ciudad = %s AND Nombre = %s AND Id_colonia != %s
                """, [data["id_ciudad"], data["nombre"], pk])
                exists = cursor.fetchone()[0]

                if exists > 0:
                    return Response(
                        {"error": "Ya existe una colonia con ese nombre en la ciudad especificada"},
                        status=400
                    )

                # Actualizar datos
                cursor.execute("""
                    UPDATE Colonia
                    SET Nombre = %s, Id_pais = %s, Id_departamento = %s, Id_ciudad = %s
                    WHERE Id_colonia = %s
                """, [
                    data["nombre"],
                    data["id_pais"],
                    data["id_departamento"],
                    data["id_ciudad"],
                    pk,
                ])
            return Response({"message": "Colonia actualizada exitosamente"}, status=200)

        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        # Eliminar una colonia
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Colonia WHERE Id_colonia = %s", [pk])
        return Response({"message": "Colonia eliminada exitosamente"}, status=204)


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
class DireccionViewSet(viewsets.ViewSet):
    def list(self, request):
        # Obtener todas las direcciones
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Id_direccion, d_pais, Id_departamento, Id_ciudad, Id_colonia
                FROM Direccion
            """)
            rows = cursor.fetchall()

        direcciones = [
            {
                "id_direccion": row[0],
                "id_pais": row[1],
                "id_departamento": row[2],
                "id_ciudad": row[3],
                "id_colonia": row[4],
            }
            for row in rows
        ]
        return Response(direcciones)

    def retrieve(self, request, pk=None):
        # Obtener una dirección específica
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Id_direccion, d_pais, Id_departamento, Id_ciudad, Id_colonia
                FROM Direccion
                WHERE Id_direccion = %s
            """, [pk])
            row = cursor.fetchone()

        if not row:
            return Response({"error": "Dirección no encontrada"}, status=404)

        direccion = {
            "id_direccion": row[0],
            "id_pais": row[1],
            "id_departamento": row[2],
            "id_ciudad": row[3],
            "id_colonia": row[4],
        }
        return Response(direccion)

    def create(self, request):
        data = request.data
        serializer = DireccionSerializer(data=data)
        if serializer.is_valid():
            with connection.cursor() as cursor:
                # Insertar nueva dirección
                cursor.execute("""
                    INSERT INTO Direccion (Id_direccion, d_pais, Id_departamento, Id_ciudad, Id_colonia)
                    VALUES (%s, %s, %s, %s, %s)
                """, [
                    data["id_direccion"],
                    data["id_pais"],
                    data["id_departamento"],
                    data["id_ciudad"],
                    data["id_colonia"],
                ])
            return Response({"message": "Dirección creada exitosamente"}, status=201)

        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        data = request.data
        serializer = DireccionSerializer(data=data)
        if serializer.is_valid():
            with connection.cursor() as cursor:
                # Actualizar dirección
                cursor.execute("""
                    UPDATE Direccion
                    SET d_pais = %s, Id_departamento = %s, Id_ciudad = %s, Id_colonia = %s
                    WHERE Id_direccion = %s
                """, [
                    data["id_pais"],
                    data["id_departamento"],
                    data["id_ciudad"],
                    data["id_colonia"],
                    pk,
                ])
            return Response({"message": "Dirección actualizada exitosamente"}, status=200)

        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        # Eliminar una dirección
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Direccion WHERE Id_direccion = %s", [pk])
        return Response({"message": "Dirección eliminada exitosamente"}, status=204)

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
class MarcaViewSet(viewsets.ViewSet):
    def list(self, request):
        # Obtener todas las marcas
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Id_marca, Nombre
                FROM Marca
            """)
            rows = cursor.fetchall()

        marcas = [
            {"id_marca": row[0], "nombre": row[1]}
            for row in rows
        ]
        return Response(marcas)

    def retrieve(self, request, pk=None):
        # Obtener una marca específica
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Id_marca, Nombre
                FROM Marca
                WHERE Id_marca = %s
            """, [pk])
            row = cursor.fetchone()

        if not row:
            return Response({"error": "Marca no encontrada"}, status=404)

        marca = {"id_marca": row[0], "nombre": row[1]}
        return Response(marca)

    def create(self, request):
        data = request.data
        serializer = MarcaSerializer(data=data)
        if serializer.is_valid():
            with connection.cursor() as cursor:
                # Verificar si el nombre ya existe
                cursor.execute("SELECT COUNT(*) FROM Marca WHERE Nombre = %s", [data["nombre"]])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El nombre de la marca ya existe"}, status=400)

                # Insertar nueva marca
                cursor.execute("""
                    INSERT INTO Marca (Id_marca, Nombre)
                    VALUES (%s, %s)
                """, [data["id_marca"], data["nombre"]])
            return Response({"message": "Marca creada exitosamente"}, status=201)

        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        data = request.data
        serializer = MarcaSerializer(data=data)
        if serializer.is_valid():
            with connection.cursor() as cursor:
                # Verificar si el nombre ya existe para otro ID
                cursor.execute("""
                    SELECT COUNT(*) FROM Marca
                    WHERE Nombre = %s AND Id_marca != %s
                """, [data["nombre"], pk])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El nombre de la marca ya existe para otro registro"}, status=400)

                # Actualizar marca
                cursor.execute("""
                    UPDATE Marca
                    SET Nombre = %s
                    WHERE Id_marca = %s
                """, [data["nombre"], pk])
            return Response({"message": "Marca actualizada exitosamente"}, status=200)

        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        # Eliminar una marca
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Marca WHERE Id_marca = %s", [pk])
        return Response({"message": "Marca eliminada exitosamente"}, status=204)

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
class TipoSeguroViewSet(viewsets.ViewSet):
    def list(self, request):
        # Obtener todos los tipos de seguro
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Id_tipo_seguro, Nombre
                FROM Tipo_seguro
            """)
            rows = cursor.fetchall()

        tipo_seguros = [
            {"id_tipo_seguro": row[0], "nombre": row[1]}
            for row in rows
        ]
        return Response(tipo_seguros)

    def retrieve(self, request, pk=None):
        # Obtener un tipo de seguro específico
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Id_tipo_seguro, Nombre
                FROM Tipo_seguro
                WHERE Id_tipo_seguro = %s
            """, [pk])
            row = cursor.fetchone()

        if not row:
            return Response({"error": "Tipo de seguro no encontrado"}, status=404)

        tipo_seguro = {"id_tipo_seguro": row[0], "nombre": row[1]}
        return Response(tipo_seguro)

    def create(self, request):
        data = request.data
        serializer = TipoSeguroSerializer(data=data)
        if serializer.is_valid():
            with connection.cursor() as cursor:
                # Verificar si el nombre ya existe
                cursor.execute("SELECT COUNT(*) FROM Tipo_seguro WHERE Nombre = %s", [data["nombre"]])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El nombre del tipo de seguro ya existe"}, status=400)

                # Insertar nuevo tipo de seguro
                cursor.execute("""
                    INSERT INTO Tipo_seguro (Id_tipo_seguro, Nombre)
                    VALUES (%s, %s)
                """, [data["id_tipo_seguro"], data["nombre"]])
            return Response({"message": "Tipo de seguro creado exitosamente"}, status=201)

        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        data = request.data
        serializer = TipoSeguroSerializer(data=data)
        if serializer.is_valid():
            with connection.cursor() as cursor:
                # Verificar si el nombre ya existe para otro ID
                cursor.execute("""
                    SELECT COUNT(*) FROM Tipo_seguro
                    WHERE Nombre = %s AND Id_tipo_seguro != %s
                """, [data["nombre"], pk])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El nombre del tipo de seguro ya existe para otro registro"}, status=400)

                # Actualizar tipo de seguro
                cursor.execute("""
                    UPDATE Tipo_seguro
                    SET Nombre = %s
                    WHERE Id_tipo_seguro = %s
                """, [data["nombre"], pk])
            return Response({"message": "Tipo de seguro actualizado exitosamente"}, status=200)

        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        # Eliminar un tipo de seguro
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Tipo_seguro WHERE Id_tipo_seguro = %s", [pk])
        return Response({"message": "Tipo de seguro eliminado exitosamente"}, status=204)

class CombustibleViewSet(viewsets.ViewSet):
    def list(self, request):
        # Obtener todos los combustibles
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Id_combustible, Nombre
                FROM Combustible
            """)
            rows = cursor.fetchall()

        combustibles = [
            {"id_combustible": row[0], "nombre": row[1]}
            for row in rows
        ]
        return Response(combustibles)

    def retrieve(self, request, pk=None):
        # Obtener un combustible específico
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Id_combustible, Nombre
                FROM Combustible
                WHERE Id_combustible = %s
            """, [pk])
            row = cursor.fetchone()

        if not row:
            return Response({"error": "Combustible no encontrado"}, status=404)

        combustible = {"id_combustible": row[0], "nombre": row[1]}
        return Response(combustible)

    def create(self, request):
        data = request.data
        serializer = CombustibleSerializer(data=data)
        if serializer.is_valid():
            with connection.cursor() as cursor:
                # Verificar si el nombre ya existe
                cursor.execute("SELECT COUNT(*) FROM Combustible WHERE Nombre = %s", [data["nombre"]])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El nombre del combustible ya existe"}, status=400)

                # Insertar nuevo combustible
                cursor.execute("""
                    INSERT INTO Combustible (Id_combustible, Nombre)
                    VALUES (%s, %s)
                """, [data["id_combustible"], data["nombre"]])
            return Response({"message": "Combustible creado exitosamente"}, status=201)

        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        data = request.data
        serializer = CombustibleSerializer(data=data)
        if serializer.is_valid():
            with connection.cursor() as cursor:
                # Verificar si el nombre ya existe para otro ID
                cursor.execute("""
                    SELECT COUNT(*) FROM Combustible
                    WHERE Nombre = %s AND Id_combustible != %s
                """, [data["nombre"], pk])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El nombre del combustible ya existe para otro registro"}, status=400)

                # Actualizar combustible
                cursor.execute("""
                    UPDATE Combustible
                    SET Nombre = %s
                    WHERE Id_combustible = %s
                """, [data["nombre"], pk])
            return Response({"message": "Combustible actualizado exitosamente"}, status=200)

        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        # Eliminar un combustible
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Combustible WHERE Id_combustible = %s", [pk])
        return Response({"message": "Combustible eliminado exitosamente"}, status=204)


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
class EstadoViewSet(viewsets.ViewSet):
    def list(self, request):
        # Obtener todos los estados
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Id_estado, Nombre
                FROM Estado
            """)
            rows = cursor.fetchall()

        estados = [
            {"id_estado": row[0], "nombre": row[1]}
            for row in rows
        ]
        return Response(estados)

    def retrieve(self, request, pk=None):
        # Obtener un estado específico
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Id_estado, Nombre
                FROM Estado
                WHERE Id_estado = %s
            """, [pk])
            row = cursor.fetchone()

        if not row:
            return Response({"error": "Estado no encontrado"}, status=404)

        estado = {"id_estado": row[0], "nombre": row[1]}
        return Response(estado)

    def create(self, request):
        data = request.data
        serializer = EstadoSerializer(data=data)
        if serializer.is_valid():
            with connection.cursor() as cursor:
                # Verificar si el nombre ya existe
                cursor.execute("SELECT COUNT(*) FROM Estado WHERE Nombre = %s", [data["nombre"]])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El nombre del estado ya existe"}, status=400)

                # Insertar nuevo estado
                cursor.execute("""
                    INSERT INTO Estado (Id_estado, Nombre)
                    VALUES (%s, %s)
                """, [data["id_estado"], data["nombre"]])
            return Response({"message": "Estado creado exitosamente"}, status=201)

        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        data = request.data
        serializer = EstadoSerializer(data=data)
        if serializer.is_valid():
            with connection.cursor() as cursor:
                # Verificar si el nombre ya existe para otro ID
                cursor.execute("""
                    SELECT COUNT(*) FROM Estado
                    WHERE Nombre = %s AND Id_estado != %s
                """, [data["nombre"], pk])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El nombre del estado ya existe para otro registro"}, status=400)

                # Actualizar estado
                cursor.execute("""
                    UPDATE Estado
                    SET Nombre = %s
                    WHERE Id_estado = %s
                """, [data["nombre"], pk])
            return Response({"message": "Estado actualizado exitosamente"}, status=200)

        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        # Eliminar un estado
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Estado WHERE Id_estado = %s", [pk])
        return Response({"message": "Estado eliminado exitosamente"}, status=204)


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
class ModeloViewSet(viewsets.ViewSet):
    def list(self, request):
        # Obtener todos los modelos
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Id_modelo, Nombre, Id_marca
                FROM Modelo
            """)
            rows = cursor.fetchall()

        modelos = [
            {"id_modelo": row[0], "nombre": row[1], "id_marca": row[2]}
            for row in rows
        ]
        return Response(modelos)

    def retrieve(self, request, pk=None):
        # Obtener un modelo específico
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Id_modelo, Nombre, Id_marca
                FROM Modelo
                WHERE Id_modelo = %s
            """, [pk])
            row = cursor.fetchone()

        if not row:
            return Response({"error": "Modelo no encontrado"}, status=404)

        modelo = {"id_modelo": row[0], "nombre": row[1], "id_marca": row[2]}
        return Response(modelo)

    def create(self, request):
        data = request.data
        serializer = ModeloSerializer(data=data)
        if serializer.is_valid():
            with connection.cursor() as cursor:
                # Verificar si el nombre ya existe
                cursor.execute("SELECT COUNT(*) FROM Modelo WHERE Nombre = %s", [data["nombre"]])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El nombre del modelo ya existe"}, status=400)

                # Verificar si la marca existe
                cursor.execute("SELECT COUNT(*) FROM Marca WHERE Id_marca = %s", [data["id_marca"]])
                if cursor.fetchone()[0] == 0:
                    return Response({"error": "La marca especificada no existe"}, status=400)

                # Insertar nuevo modelo
                cursor.execute("""
                    INSERT INTO Modelo (Id_modelo, Nombre, Id_marca)
                    VALUES (%s, %s, %s)
                """, [data["id_modelo"], data["nombre"], data["id_marca"]])
            return Response({"message": "Modelo creado exitosamente"}, status=201)

        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        data = request.data
        serializer = ModeloSerializer(data=data)
        if serializer.is_valid():
            with connection.cursor() as cursor:
                # Verificar si el nombre ya existe para otro ID
                cursor.execute("""
                    SELECT COUNT(*) FROM Modelo
                    WHERE Nombre = %s AND Id_modelo != %s
                """, [data["nombre"], pk])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El nombre del modelo ya existe para otro registro"}, status=400)

                # Verificar si la marca existe
                cursor.execute("SELECT COUNT(*) FROM Marca WHERE Id_marca = %s", [data["id_marca"]])
                if cursor.fetchone()[0] == 0:
                    return Response({"error": "La marca especificada no existe"}, status=400)

                # Actualizar modelo
                cursor.execute("""
                    UPDATE Modelo
                    SET Nombre = %s, Id_marca = %s
                    WHERE Id_modelo = %s
                """, [data["nombre"], data["id_marca"], pk])
            return Response({"message": "Modelo actualizado exitosamente"}, status=200)

        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        # Eliminar un modelo
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Modelo WHERE Id_modelo = %s", [pk])
        return Response({"message": "Modelo eliminado exitosamente"}, status=204)

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
class TipoTransaccionViewSet(viewsets.ViewSet):
    def list(self, request):
        # Obtener todos los registros de TipoTransaccion
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Id_tipo_transaccion, Nombre
                FROM Tipo_transaccion
            """)
            rows = cursor.fetchall()

        tipos_transaccion = [
            {"id_tipo_transaccion": row[0], "nombre": row[1]}
            for row in rows
        ]
        return Response(tipos_transaccion)

    def retrieve(self, request, pk=None):
        # Obtener un registro específico
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Id_tipo_transaccion, Nombre
                FROM Tipo_transaccion
                WHERE Id_tipo_transaccion = %s
            """, [pk])
            row = cursor.fetchone()

        if not row:
            return Response({"error": "Tipo de transacción no encontrado"}, status=404)

        tipo_transaccion = {"id_tipo_transaccion": row[0], "nombre": row[1]}
        return Response(tipo_transaccion)

    def create(self, request):
        data = request.data
        serializer = TipoTransaccionSerializer(data=data)
        if serializer.is_valid():
            with connection.cursor() as cursor:
                # Verificar si el nombre ya existe
                cursor.execute("SELECT COUNT(*) FROM Tipo_transaccion WHERE Nombre = %s", [data["nombre"]])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El nombre del tipo de transacción ya existe"}, status=400)

                # Insertar nuevo registro
                cursor.execute("""
                    INSERT INTO Tipo_transaccion (Id_tipo_transaccion, Nombre)
                    VALUES (%s, %s)
                """, [data["id_tipo_transaccion"], data["nombre"]])
            return Response({"message": "Tipo de transacción creado exitosamente"}, status=201)

        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        data = request.data
        serializer = TipoTransaccionSerializer(data=data)
        if serializer.is_valid():
            with connection.cursor() as cursor:
                # Verificar si el nombre ya existe para otro ID
                cursor.execute("""
                    SELECT COUNT(*) FROM Tipo_transaccion
                    WHERE Nombre = %s AND Id_tipo_transaccion != %s
                """, [data["nombre"], pk])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El nombre del tipo de transacción ya existe para otro registro"}, status=400)

                # Actualizar registro
                cursor.execute("""
                    UPDATE Tipo_transaccion
                    SET Nombre = %s
                    WHERE Id_tipo_transaccion = %s
                """, [data["nombre"], pk])
            return Response({"message": "Tipo de transacción actualizado exitosamente"}, status=200)

        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        # Eliminar un registro
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Tipo_transaccion WHERE Id_tipo_transaccion = %s", [pk])
        return Response({"message": "Tipo de transacción eliminado exitosamente"}, status=204)

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
class SucursalViewSet(viewsets.ViewSet):
    def list(self, request):
        # Obtener todos los registros de Sucursal
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Id_sucursal, Nombre, Telefono, Id_direccion
                FROM Sucursal
            """)
            rows = cursor.fetchall()

        sucursales = [
            {"id_sucursal": row[0], "nombre": row[1], "telefono": row[2], "id_direccion": row[3]}
            for row in rows
        ]
        return Response(sucursales)

    def retrieve(self, request, pk=None):
        # Obtener un registro específico de Sucursal
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Id_sucursal, Nombre, Telefono, Id_direccion
                FROM Sucursal
                WHERE Id_sucursal = %s
            """, [pk])
            row = cursor.fetchone()

        if not row:
            return Response({"error": "Sucursal no encontrada"}, status=404)

        sucursal = {"id_sucursal": row[0], "nombre": row[1], "telefono": row[2], "id_direccion": row[3]}
        return Response(sucursal)

    def create(self, request):
        data = request.data
        serializer = SucursalSerializer(data=data)
        if serializer.is_valid():
            with connection.cursor() as cursor:
                # Verificar si el nombre ya existe
                cursor.execute("SELECT COUNT(*) FROM Sucursal WHERE Nombre = %s", [data["nombre"]])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El nombre de la sucursal ya existe"}, status=400)

                # Insertar nuevo registro
                cursor.execute("""
                    INSERT INTO Sucursal (Id_sucursal, Nombre, Telefono, Id_direccion)
                    VALUES (%s, %s, %s, %s)
                """, [data["id_sucursal"], data["nombre"], data["telefono"], data["id_direccion"]])
            return Response({"message": "Sucursal creada exitosamente"}, status=201)

        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        data = request.data
        serializer = SucursalSerializer(data=data)
        if serializer.is_valid():
            with connection.cursor() as cursor:
                # Verificar si el nombre ya existe para otro ID
                cursor.execute("""
                    SELECT COUNT(*) FROM Sucursal
                    WHERE Nombre = %s AND Id_sucursal != %s
                """, [data["nombre"], pk])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El nombre de la sucursal ya existe para otro registro"}, status=400)

                # Actualizar registro
                cursor.execute("""
                    UPDATE Sucursal
                    SET Nombre = %s, Telefono = %s, Id_direccion = %s
                    WHERE Id_sucursal = %s
                """, [data["nombre"], data["telefono"], data["id_direccion"], pk])
            return Response({"message": "Sucursal actualizada exitosamente"}, status=200)

        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        # Eliminar un registro de Sucursal
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Sucursal WHERE Id_sucursal = %s", [pk])
        return Response({"message": "Sucursal eliminada exitosamente"}, status=204)
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