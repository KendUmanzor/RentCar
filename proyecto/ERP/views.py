from django.shortcuts import render


from .models import *
from .serializer import *
from django.db import connection
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.routers import DefaultRouter

class PaisViewSet(viewsets.ViewSet):

    def list(self, request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT Id_pais, Nombre FROM Pais")
            rows = cursor.fetchall()

        paises = [{"id_pais": row[0], "nombre": row[1]} for row in rows]
        return Response(paises)

    def retrieve(self, request, pk=None):
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

            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM Pais WHERE Id_pais = %s", [data["id_pais"]])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El ID del país ya existe"}, status=status.HTTP_400_BAD_REQUEST)

            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM Pais WHERE Nombre = %s", [data["nombre"]])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El nombre del país ya existe"}, status=status.HTTP_400_BAD_REQUEST)

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

            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM Pais WHERE Id_pais = %s", [pk])
                if cursor.fetchone()[0] == 0:
                    return Response({"error": "País no encontrado"}, status=status.HTTP_404_NOT_FOUND)

            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE Pais SET Nombre = %s WHERE Id_pais = %s",
                    [data["nombre"], pk],
                )
            return Response({"message": "País actualizado correctamente"})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM Pais WHERE Id_pais = %s", [pk])
            if cursor.fetchone()[0] == 0:
                return Response({"error": "País no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Pais WHERE Id_pais = %s", [pk])
        return Response({"message": "País eliminado correctamente"})


class DepartamentoViewSet(viewsets.ViewSet):

    def list(self, request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT Id_departamento, Nombre, Id_pais FROM Departamento")
            rows = cursor.fetchall()

        departamentos = [{"id_departamento": row[0], "nombre": row[1], "id_pais": row[2]} for row in rows]
        return Response(departamentos)

    def retrieve(self, request, pk=None):
        with connection.cursor() as cursor:
            cursor.execute("SELECT Id_departamento, Nombre, Id_pais FROM Departamento WHERE Id_departamento = %s", [pk])
            row = cursor.fetchone()

        if row:
            departamento = {"id_departamento": row[0], "nombre": row[1], "id_pais": row[2]}
            return Response(departamento)
        else:
            return Response({"error": "Departamento no encontrado."}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = DepartamentoSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            id_departamento = data['id_departamento']
            nombre = data['nombre']
            id_pais = data['id_pais']

            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM Pais WHERE Id_pais = %s", [id_pais])
                if cursor.fetchone()[0] == 0:
                    return Response({"error": "El país especificado no existe."}, status=status.HTTP_400_BAD_REQUEST)

                cursor.execute(
                    "SELECT COUNT(*) FROM Departamento WHERE Nombre = %s AND Id_pais = %s",
                    [nombre, id_pais]
                )
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "Ya existe un departamento con ese nombre en este país."}, status=status.HTTP_400_BAD_REQUEST)

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

    def update(self, request, pk=None):
        with connection.cursor() as cursor:
            cursor.execute("SELECT Id_departamento, Nombre, Id_pais FROM Departamento WHERE Id_departamento = %s", [pk])
            row = cursor.fetchone()

        if not row:
            return Response({"error": "Departamento no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DepartamentoSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            id_departamento = data['id_departamento']
            nombre = data['nombre']
            id_pais = data['id_pais']

            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM Pais WHERE Id_pais = %s", [id_pais])
                if cursor.fetchone()[0] == 0:
                    return Response({"error": "El país especificado no existe."}, status=status.HTTP_400_BAD_REQUEST)

                cursor.execute(
                    "SELECT COUNT(*) FROM Departamento WHERE Nombre = %s AND Id_pais = %s AND Id_departamento != %s",
                    [nombre, id_pais, pk]
                )
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "Ya existe un departamento con ese nombre en este país."}, status=status.HTTP_400_BAD_REQUEST)

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

class CiudadViewSet(viewsets.ViewSet):
    def list(self, request):
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
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Ciudad WHERE Id_ciudad = %s", [pk])
        return Response({"message": "Ciudad eliminada exitosamente"}, status=204)

class ColoniaViewSet(viewsets.ViewSet):
    def list(self, request):
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
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Colonia WHERE Id_colonia = %s", [pk])
        return Response({"message": "Colonia eliminada exitosamente"}, status=204)


class DireccionViewSet(viewsets.ViewSet):
    def list(self, request):
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

        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Direccion WHERE Id_direccion = %s", [pk])
        return Response({"message": "Dirección eliminada exitosamente"}, status=204)


class MarcaViewSet(viewsets.ViewSet):
    def list(self, request):
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
                cursor.execute("SELECT COUNT(*) FROM Marca WHERE Nombre = %s", [data["nombre"]])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El nombre de la marca ya existe"}, status=400)

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
                cursor.execute("""
                    SELECT COUNT(*) FROM Marca
                    WHERE Nombre = %s AND Id_marca != %s
                """, [data["nombre"], pk])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El nombre de la marca ya existe para otro registro"}, status=400)

                cursor.execute("""
                    UPDATE Marca
                    SET Nombre = %s
                    WHERE Id_marca = %s
                """, [data["nombre"], pk])
            return Response({"message": "Marca actualizada exitosamente"}, status=200)

        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Marca WHERE Id_marca = %s", [pk])
        return Response({"message": "Marca eliminada exitosamente"}, status=204)

class TipoSeguroViewSet(viewsets.ViewSet):

    def list(self, request):
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
                cursor.execute("SELECT COUNT(*) FROM Tipo_seguro WHERE Nombre = %s", [data["nombre"]])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El nombre del tipo de seguro ya existe"}, status=400)

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
                cursor.execute("""
                    SELECT COUNT(*) FROM Tipo_seguro
                    WHERE Nombre = %s AND Id_tipo_seguro != %s
                """, [data["nombre"], pk])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El nombre del tipo de seguro ya existe para otro registro"}, status=400)

                cursor.execute("""
                    UPDATE Tipo_seguro
                    SET Nombre = %s
                    WHERE Id_tipo_seguro = %s
                """, [data["nombre"], pk])
            return Response({"message": "Tipo de seguro actualizado exitosamente"}, status=200)

        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Tipo_seguro WHERE Id_tipo_seguro = %s", [pk])
        return Response({"message": "Tipo de seguro eliminado exitosamente"}, status=204)



class CombustibleViewSet(viewsets.ViewSet):
    def list(self, request):
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
                cursor.execute("SELECT COUNT(*) FROM Combustible WHERE Nombre = %s", [data["nombre"]])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El nombre del combustible ya existe"}, status=400)

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
                cursor.execute("""
                    SELECT COUNT(*) FROM Combustible
                    WHERE Nombre = %s AND Id_combustible != %s
                """, [data["nombre"], pk])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El nombre del combustible ya existe para otro registro"}, status=400)


                cursor.execute("""
                    UPDATE Combustible
                    SET Nombre = %s
                    WHERE Id_combustible = %s
                """, [data["nombre"], pk])
            return Response({"message": "Combustible actualizado exitosamente"}, status=200)

        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):

        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Combustible WHERE Id_combustible = %s", [pk])
        return Response({"message": "Combustible eliminado exitosamente"}, status=204)


class EstadoViewSet(viewsets.ViewSet):
    def list(self, request):
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

                cursor.execute("SELECT COUNT(*) FROM Estado WHERE Nombre = %s", [data["nombre"]])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El nombre del estado ya existe"}, status=400)


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

                cursor.execute("""
                    SELECT COUNT(*) FROM Estado
                    WHERE Nombre = %s AND Id_estado != %s
                """, [data["nombre"], pk])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El nombre del estado ya existe para otro registro"}, status=400)


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


class ModeloViewSet(viewsets.ViewSet):
    def list(self, request):
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
                cursor.execute("SELECT COUNT(*) FROM Modelo WHERE Nombre = %s", [data["nombre"]])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El nombre del modelo ya existe"}, status=400)

                cursor.execute("SELECT COUNT(*) FROM Marca WHERE Id_marca = %s", [data["id_marca"]])
                if cursor.fetchone()[0] == 0:
                    return Response({"error": "La marca especificada no existe"}, status=400)

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
                cursor.execute("""
                    SELECT COUNT(*) FROM Modelo
                    WHERE Nombre = %s AND Id_modelo != %s
                """, [data["nombre"], pk])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El nombre del modelo ya existe para otro registro"}, status=400)

                cursor.execute("SELECT COUNT(*) FROM Marca WHERE Id_marca = %s", [data["id_marca"]])
                if cursor.fetchone()[0] == 0:
                    return Response({"error": "La marca especificada no existe"}, status=400)


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


class TipoTransaccionViewSet(viewsets.ViewSet):
    def list(self, request):

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
                cursor.execute("SELECT COUNT(*) FROM Tipo_transaccion WHERE Nombre = %s", [data["nombre"]])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El nombre del tipo de transacción ya existe"}, status=400)


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

                cursor.execute("""
                    SELECT COUNT(*) FROM Tipo_transaccion
                    WHERE Nombre = %s AND Id_tipo_transaccion != %s
                """, [data["nombre"], pk])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El nombre del tipo de transacción ya existe para otro registro"}, status=400)


                cursor.execute("""
                    UPDATE Tipo_transaccion
                    SET Nombre = %s
                    WHERE Id_tipo_transaccion = %s
                """, [data["nombre"], pk])
            return Response({"message": "Tipo de transacción actualizado exitosamente"}, status=200)

        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):

        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Tipo_transaccion WHERE Id_tipo_transaccion = %s", [pk])
        return Response({"message": "Tipo de transacción eliminado exitosamente"}, status=204)

class SucursalViewSet(viewsets.ViewSet):
    def list(self, request):

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

                cursor.execute("SELECT COUNT(*) FROM Sucursal WHERE Nombre = %s", [data["nombre"]])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El nombre de la sucursal ya existe"}, status=400)


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

                cursor.execute("""
                    SELECT COUNT(*) FROM Sucursal
                    WHERE Nombre = %s AND Id_sucursal != %s
                """, [data["nombre"], pk])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El nombre de la sucursal ya existe para otro registro"}, status=400)


                cursor.execute("""
                    UPDATE Sucursal
                    SET Nombre = %s, Telefono = %s, Id_direccion = %s
                    WHERE Id_sucursal = %s
                """, [data["nombre"], data["telefono"], data["id_direccion"], pk])
            return Response({"message": "Sucursal actualizada exitosamente"}, status=200)

        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):

        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Sucursal WHERE Id_sucursal = %s", [pk])
        return Response({"message": "Sucursal eliminada exitosamente"}, status=204)


class ParqueoViewSet(viewsets.ViewSet):
    def list(self, request):

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Id_parqueo, Lote, Referencia, Id_sucursal
                FROM Parqueo
            """)
            rows = cursor.fetchall()

        parqueos = [
            {"id_parqueo": row[0], "lote": row[1], "referencia": row[2], "id_sucursal": row[3]}
            for row in rows
        ]
        return Response(parqueos)

    def retrieve(self, request, pk=None):

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Id_parqueo, Lote, Referencia, Id_sucursal
                FROM Parqueo
                WHERE Id_parqueo = %s
            """, [pk])
            row = cursor.fetchone()

        if not row:
            return Response({"error": "Parqueo no encontrado"}, status=404)

        parqueo = {"id_parqueo": row[0], "lote": row[1], "referencia": row[2], "id_sucursal": row[3]}
        return Response(parqueo)

    def create(self, request):
        data = request.data
        serializer = ParqueoSerializer(data=data)
        if serializer.is_valid():
            with connection.cursor() as cursor:

                cursor.execute("SELECT COUNT(*) FROM Parqueo WHERE Lote = %s", [data["lote"]])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El lote ya existe"}, status=400)


                cursor.execute("""
                    INSERT INTO Parqueo (Id_parqueo, Lote, Referencia, Id_sucursal)
                    VALUES (%s, %s, %s, %s)
                """, [data["id_parqueo"], data["lote"], data["referencia"], data["id_sucursal"]])
            return Response({"message": "Parqueo creado exitosamente"}, status=201)

        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        data = request.data
        serializer = ParqueoSerializer(data=data)
        if serializer.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT COUNT(*) FROM Parqueo
                    WHERE Lote = %s AND Id_parqueo != %s
                """, [data["lote"], pk])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El lote ya existe para otro registro"}, status=400)


                cursor.execute("""
                    UPDATE Parqueo
                    SET Lote = %s, Referencia = %s, Id_sucursal = %s
                    WHERE Id_parqueo = %s
                """, [data["lote"], data["referencia"], data["id_sucursal"], pk])
            return Response({"message": "Parqueo actualizado exitosamente"}, status=200)

        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):

        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Parqueo WHERE Id_parqueo = %s", [pk])
        return Response({"message": "Parqueo eliminado exitosamente"}, status=204)


class VehiculoViewSet(viewsets.ViewSet):
    def list(self, request):

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Id_Vehiculo, Ano, Vin, Motor, Matricula, Disponibilidad, Precio,
                       Id_marca, Id_modelo, Id_estado, Id_tipo_transaccion, Id_combustible,
                       Id_sucursal, Id_Parqueo
                FROM Vehiculo
            """)
            rows = cursor.fetchall()

        vehiculos = [
            {
                "id_vehiculo": row[0], "ano": row[1], "vin": row[2], "motor": row[3],
                "matricula": row[4], "disponibilidad": row[5], "precio": row[6],
                "id_marca": row[7], "id_modelo": row[8], "id_estado": row[9],
                "id_tipo_transaccion": row[10], "id_combustible": row[11],
                "id_sucursal": row[12], "id_parqueo": row[13]
            }
            for row in rows
        ]
        return Response(vehiculos)

    def retrieve(self, request, pk=None):

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Id_Vehiculo, Ano, Vin, Motor, Matricula, Disponibilidad, Precio,
                       Id_marca, Id_modelo, Id_estado, Id_tipo_transaccion, Id_combustible,
                       Id_sucursal, Id_Parqueo
                FROM Vehiculo
                WHERE Id_Vehiculo = %s
            """, [pk])
            row = cursor.fetchone()

        if not row:
            return Response({"error": "Vehículo no encontrado"}, status=404)

        vehiculo = {
            "id_vehiculo": row[0], "ano": row[1], "vin": row[2], "motor": row[3],
            "matricula": row[4], "disponibilidad": row[5], "precio": row[6],
            "id_marca": row[7], "id_modelo": row[8], "id_estado": row[9],
            "id_tipo_transaccion": row[10], "id_combustible": row[11],
            "id_sucursal": row[12], "id_parqueo": row[13]
        }
        return Response(vehiculo)

    def create(self, request):
        data = request.data
        serializer = VehiculoSerializer(data=data)
        if serializer.is_valid():
            with connection.cursor() as cursor:

                cursor.execute("SELECT COUNT(*) FROM Vehiculo WHERE Vin = %s", [data["vin"]])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El VIN ya existe"}, status=400)


                cursor.execute("SELECT COUNT(*) FROM Vehiculo WHERE Matricula = %s", [data["matricula"]])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "La matrícula ya existe"}, status=400)


                cursor.execute("""
                    INSERT INTO Vehiculo (Id_Vehiculo, Ano, Vin, Motor, Matricula, Disponibilidad, Precio,
                                          Id_marca, Id_modelo, Id_estado, Id_tipo_transaccion, Id_combustible,
                                          Id_sucursal, Id_Parqueo)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, [data["id_vehiculo"], data["ano"], data["vin"], data["motor"], data["matricula"],
                      data["disponibilidad"], data["precio"], data["id_marca"], data["id_modelo"], data["id_estado"],
                      data["id_tipo_transaccion"], data["id_combustible"], data["id_sucursal"], data["id_parqueo"]])
            return Response({"message": "Vehículo creado exitosamente"}, status=201)

        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        data = request.data
        serializer = VehiculoSerializer(data=data)
        if serializer.is_valid():
            with connection.cursor() as cursor:

                cursor.execute("""
                    SELECT COUNT(*) FROM Vehiculo
                    WHERE Vin = %s AND Id_Vehiculo != %s
                """, [data["vin"], pk])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El VIN ya existe para otro vehículo"}, status=400)


                cursor.execute("""
                    SELECT COUNT(*) FROM Vehiculo
                    WHERE Matricula = %s AND Id_Vehiculo != %s
                """, [data["matricula"], pk])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "La matrícula ya existe para otro vehículo"}, status=400)

                cursor.execute("""
                    UPDATE Vehiculo
                    SET Ano = %s, Vin = %s, Motor = %s, Matricula = %s, Disponibilidad = %s, Precio = %s,
                        Id_marca = %s, Id_modelo = %s, Id_estado = %s, Id_tipo_transaccion = %s,
                        Id_combustible = %s, Id_sucursal = %s, Id_Parqueo = %s
                    WHERE Id_Vehiculo = %s
                """, [data["ano"], data["vin"], data["motor"], data["matricula"], data["disponibilidad"],
                      data["precio"], data["id_marca"], data["id_modelo"], data["id_estado"],
                      data["id_tipo_transaccion"], data["id_combustible"], data["id_sucursal"], data["id_parqueo"], pk])
            return Response({"message": "Vehículo actualizado exitosamente"}, status=200)

        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Vehiculo WHERE Id_Vehiculo = %s", [pk])
        return Response({"message": "Vehículo eliminado exitosamente"}, status=204)

class ColorViewSet(viewsets.ViewSet):
    def list(self, request):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Id_color, Nombre, Id_vehiculo
                FROM Color
            """)
            rows = cursor.fetchall()

        colores = [
            {"id_color": row[0], "nombre": row[1], "id_vehiculo": row[2]}
            for row in rows
        ]
        return Response(colores)

    def retrieve(self, request, pk=None):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Id_color, Nombre, Id_vehiculo
                FROM Color
                WHERE Id_color = %s
            """, [pk])
            row = cursor.fetchone()

        if not row:
            return Response({"error": "Color no encontrado"}, status=404)

        color = {"id_color": row[0], "nombre": row[1], "id_vehiculo": row[2]}
        return Response(color)

    def create(self, request):
        data = request.data
        serializer = ColorSerializer(data=data)
        if serializer.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM Color
                    WHERE Nombre = %s AND Id_vehiculo = %s
                """, [data["nombre"], data["id_vehiculo"]])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El color ya está asignado a este vehículo"}, status=400)

                cursor.execute("""
                    INSERT INTO Color (Id_color, Nombre, Id_vehiculo)
                    VALUES (%s, %s, %s)
                """, [data["id_color"], data["nombre"], data["id_vehiculo"]])
            return Response({"message": "Color creado exitosamente"}, status=201)

        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        data = request.data
        serializer = ColorSerializer(data=data)
        if serializer.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM Color
                    WHERE Nombre = %s AND Id_vehiculo = %s AND Id_color != %s
                """, [data["nombre"], data["id_vehiculo"], pk])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El color ya está asignado a este vehículo"}, status=400)

                cursor.execute("""
                    UPDATE Color
                    SET Nombre = %s, Id_vehiculo = %s
                    WHERE Id_color = %s
                """, [data["nombre"], data["id_vehiculo"], pk])
            return Response({"message": "Color actualizado exitosamente"}, status=200)

        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):

        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Color WHERE Id_color = %s", [pk])
        return Response({"message": "Color eliminado exitosamente"}, status=204)

class RangoViewSet(viewsets.ViewSet):
    def list(self, request):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Id_rango, Inicio, Fin
                FROM Rango
            """)
            rows = cursor.fetchall()

        rangos = [
            {"id_rango": row[0], "inicio": row[1], "fin": row[2]}
            for row in rows
        ]
        return Response(rangos)

    def retrieve(self, request, pk=None):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Id_rango, Inicio, Fin
                FROM Rango
                WHERE Id_rango = %s
            """, [pk])
            row = cursor.fetchone()

        if not row:
            return Response({"error": "Rango no encontrado"}, status=404)

        rango = {"id_rango": row[0], "inicio": row[1], "fin": row[2]}
        return Response(rango)

    def create(self, request):
        data = request.data
        serializer = RangoSerializer(data=data)
        if serializer.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM Rango
                    WHERE Inicio = %s AND Fin = %s
                """, [data["inicio"], data["fin"]])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El rango ya existe"}, status=400)
                cursor.execute("""
                    INSERT INTO Rango (Id_rango, Inicio, Fin)
                    VALUES (%s, %s, %s)
                """, [data["id_rango"], data["inicio"], data["fin"]])
            return Response({"message": "Rango creado exitosamente"}, status=201)

        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        data = request.data
        serializer = RangoSerializer(data=data)
        if serializer.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM Rango
                    WHERE Inicio = %s AND Fin = %s AND Id_rango != %s
                """, [data["inicio"], data["fin"], pk])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El rango ya existe"}, status=400)

                cursor.execute("""
                    UPDATE Rango
                    SET Inicio = %s, Fin = %s
                    WHERE Id_rango = %s
                """, [data["inicio"], data["fin"], pk])
            return Response({"message": "Rango actualizado exitosamente"}, status=200)

        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Rango WHERE Id_rango = %s", [pk])
        return Response({"message": "Rango eliminado exitosamente"}, status=204)

class SarViewSet(viewsets.ViewSet):
    def list(self, request):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Id_sar, Fecha_limite, Num_trans, Id_tipo_transaccion, Id_rango, Id_sucursal
                FROM SAR
            """)
            rows = cursor.fetchall()
        sar_list = [
            {
                "id_sar": row[0],
                "fecha_limite": row[1],
                "num_trans": row[2],
                "id_tipo_transaccion": row[3],
                "id_rango": row[4],
                "id_sucursal": row[5],
            }
            for row in rows
        ]
        return Response(sar_list)

    def retrieve(self, request, pk=None):
        
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Id_sar, Fecha_limite, Num_trans, Id_tipo_transaccion, Id_rango, Id_sucursal
                FROM SAR
                WHERE Id_sar = %s
            """, [pk])
            row = cursor.fetchone()
        if not row:
            return Response({"error": "SAR no encontrado"}, status=404)
        sar = {
            "id_sar": row[0],
            "fecha_limite": row[1],
            "num_trans": row[2],
            "id_tipo_transaccion": row[3],
            "id_rango": row[4],
            "id_sucursal": row[5],
        }
        return Response(sar)

    def create(self, request):
        data = request.data
        serializer = SarSerializer(data=data)
        if serializer.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO SAR (Id_sar, Fecha_limite, Num_trans, Id_tipo_transaccion, Id_rango, Id_sucursal)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, [
                    data["id_sar"], 
                    data["fecha_limite"], 
                    data["num_trans"], 
                    data["id_tipo_transaccion"], 
                    data["id_rango"], 
                    data["id_sucursal"]
                ])
            return Response({"message": "SAR creado exitosamente"}, status=201)
        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        data = request.data
        serializer = SarSerializer(data=data)
        if serializer.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE SAR
                    SET Fecha_limite = %s, Num_trans = %s, Id_tipo_transaccion = %s, Id_rango = %s, Id_sucursal = %s
                    WHERE Id_sar = %s
                """, [
                    data["fecha_limite"], 
                    data["num_trans"], 
                    data["id_tipo_transaccion"], 
                    data["id_rango"], 
                    data["id_sucursal"],
                    pk
                ])
            return Response({"message": "SAR actualizado exitosamente"}, status=200)

        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM SAR WHERE Id_sar = %s", [pk])
        return Response({"message": "SAR eliminado exitosamente"}, status=204)


class DetalleFacturaViewSet(viewsets.ViewSet):
    def list(self, request):
        
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Id_detalle_factura, Descuento, Id_vehiculo
                FROM Detalle_factura
            """)
            rows = cursor.fetchall()

        detalles_list = [
            {
                "id_detalle_factura": row[0],
                "descuento": row[1],
                "id_vehiculo": row[2],
            }
            for row in rows
        ]
        return Response(detalles_list)

    def retrieve(self, request, pk=None):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Id_detalle_factura, Descuento, Id_vehiculo
                FROM Detalle_factura
                WHERE Id_detalle_factura = %s
            """, [pk])
            row = cursor.fetchone()

        if not row:
            return Response({"error": "DetalleFactura no encontrado"}, status=404)

        detalle = {
            "id_detalle_factura": row[0],
            "descuento": row[1],
            "id_vehiculo": row[2],
        }
        return Response(detalle)

    def create(self, request):
        data = request.data
        serializer = DetalleFacturaSerializer(data=data)
        if serializer.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Detalle_factura (Id_detalle_factura, Descuento, Id_vehiculo)
                    VALUES (%s, %s, %s)
                """, [
                    data["id_detalle_factura"], 
                    data["descuento"], 
                    data["id_vehiculo"]
                ])
            return Response({"message": "DetalleFactura creado exitosamente"}, status=201)

        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        data = request.data
        serializer = DetalleFacturaSerializer(data=data)
        if serializer.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE Detalle_factura
                    SET Descuento = %s, Id_vehiculo = %s
                    WHERE Id_detalle_factura = %s
                """, [
                    data["descuento"], 
                    data["id_vehiculo"], 
                    pk
                ])
            return Response({"message": "DetalleFactura actualizado exitosamente"}, status=200)

        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):

        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Detalle_factura WHERE Id_detalle_factura = %s", [pk])
        return Response({"message": "DetalleFactura eliminado exitosamente"}, status=204)



class MetodoPagoViewSet(viewsets.ViewSet):
    def list(self, request):

        with connection.cursor() as cursor:
            cursor.execute("SELECT Id_metodo_pago, Nombre FROM Metodo_pago")
            rows = cursor.fetchall()

        metodos_pago = [{"id_metodo_pago": row[0], "nombre": row[1]} for row in rows]
        return Response(metodos_pago)

    def retrieve(self, request, pk=None):

        with connection.cursor() as cursor:
            cursor.execute("SELECT Id_metodo_pago, Nombre FROM Metodo_pago WHERE Id_metodo_pago = %s", [pk])
            row = cursor.fetchone()

        if row:
            metodo_pago = {"id_metodo_pago": row[0], "nombre": row[1]}
            return Response(metodo_pago)
        return Response({"error": "Método de pago no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = MetodoPagoSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data


            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM Metodo_pago WHERE Nombre = %s", [data["nombre"]])
                if cursor.fetchone()[0] > 0:
                    return Response({"error": "El nombre del método de pago ya existe"}, status=status.HTTP_400_BAD_REQUEST)


            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Metodo_pago (Nombre) VALUES (%s)",
                    [data["nombre"]],
                )
            return Response({"message": "Método de pago creado correctamente"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        serializer = MetodoPagoSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data


            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM Metodo_pago WHERE Id_metodo_pago = %s", [pk])
                if cursor.fetchone()[0] == 0:
                    return Response({"error": "Método de pago no encontrado"}, status=status.HTTP_404_NOT_FOUND)

            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE Metodo_pago SET Nombre = %s WHERE Id_metodo_pago = %s",
                    [data["nombre"], pk],
                )
            return Response({"message": "Método de pago actualizado correctamente"})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM Metodo_pago WHERE Id_metodo_pago = %s", [pk])
            if cursor.fetchone()[0] == 0:
                return Response({"error": "Método de pago no encontrado"}, status=status.HTTP_404_NOT_FOUND)


        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Metodo_pago WHERE Id_metodo_pago = %s", [pk])
        return Response({"message": "Método de pago eliminado correctamente"})


class FacturaViewSet(viewsets.ViewSet):
    def list(self, request):

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Id_factura, Fecha_emision, Total, Id_detalle_factura, Id_tipo_transaccion, 
                    Id_cliente, Id_empleado, Id_sar
                FROM Factura
            """)
            rows = cursor.fetchall()

        facturas_list = [
            {
                "id_factura": row[0],
                "fecha_emision": row[1],
                "total": row[2],
                "id_detalle_factura": row[3],
                "id_tipo_transaccion": row[4],
                "id_cliente": row[5],
                "id_empleado": row[6],
                "id_sar": row[7],
            }
            for row in rows
        ]
        return Response(facturas_list)

    def retrieve(self, request, pk=None):

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Id_factura, Fecha_emision, Total, Id_detalle_factura, Id_tipo_transaccion, 
                    Id_cliente, Id_empleado, Id_sar
                FROM Factura
                WHERE Id_factura = %s
            """, [pk])
            row = cursor.fetchone()

        if not row:
            return Response({"error": "Factura no encontrada"}, status=404)

        factura = {
            "id_factura": row[0],
            "fecha_emision": row[1],
            "total": row[2],
            "id_detalle_factura": row[3],
            "id_tipo_transaccion": row[4],
            "id_cliente": row[5],
            "id_empleado": row[6],
            "id_sar": row[7],
        }
        return Response(factura)

    def create(self, request):
        data = request.data
        serializer = FacturaSerializer(data=data)
        if serializer.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Factura (Id_factura, Fecha_emision, Total, Id_detalle_factura, 
                                        Id_tipo_transaccion, Id_cliente, Id_empleado, Id_sar)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, [
                    data["id_factura"], 
                    data["fecha_emision"], 
                    data["total"], 
                    data["id_detalle_factura"], 
                    data["id_tipo_transaccion"], 
                    data["id_cliente"], 
                    data["id_empleado"], 
                    data["id_sar"]
                ])
            return Response({"message": "Factura creada exitosamente"}, status=201)

        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        data = request.data
        serializer = FacturaSerializer(data=data)
        if serializer.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE Factura
                    SET Fecha_emision = %s, Total = %s, Id_detalle_factura = %s, 
                        Id_tipo_transaccion = %s, Id_cliente = %s, Id_empleado = %s, Id_sar = %s
                    WHERE Id_factura = %s
                """, [
                    data["fecha_emision"], 
                    data["total"], 
                    data["id_detalle_factura"], 
                    data["id_tipo_transaccion"], 
                    data["id_cliente"], 
                    data["id_empleado"], 
                    data["id_sar"], 
                    pk
                ])
            return Response({"message": "Factura actualizada exitosamente"}, status=200)

        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Factura WHERE Id_factura = %s", [pk])
        return Response({"message": "Factura eliminada exitosamente"}, status=204)


class PagoViewSet(viewsets.ViewSet):
    def list(self, request):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Id_pago, Estado, Monto, Fecha_pago, Id_factura, Id_metodo_pago
                FROM Pago
            """)
            rows = cursor.fetchall()

        pagos_list = [
            {
                "id_pago": row[0],
                "estado": row[1],
                "monto": row[2],
                "fecha_pago": row[3],
                "id_factura": row[4],
                "id_metodo_pago": row[5],
            }
            for row in rows
        ]
        return Response(pagos_list)

    def retrieve(self, request, pk=None):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Id_pago, Estado, Monto, Fecha_pago, Id_factura, Id_metodo_pago
                FROM Pago
                WHERE Id_pago = %s
            """, [pk])
            row = cursor.fetchone()

        if not row:
            return Response({"error": "Pago no encontrado"}, status=404)

        pago = {
            "id_pago": row[0],
            "estado": row[1],
            "monto": row[2],
            "fecha_pago": row[3],
            "id_factura": row[4],
            "id_metodo_pago": row[5],
        }
        return Response(pago)

    def create(self, request):
        data = request.data
        serializer = PagoSerializer(data=data)
        if serializer.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Pago (Id_pago, Estado, Monto, Fecha_pago, Id_factura, Id_metodo_pago)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, [
                    data["id_pago"],
                    data["estado"],
                    data["monto"],
                    data["fecha_pago"],
                    data["id_factura"],
                    data["id_metodo_pago"],
                ])
            return Response({"message": "Pago creado exitosamente"}, status=201)

        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        data = request.data
        serializer = PagoSerializer(data=data)
        if serializer.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE Pago
                    SET Estado = %s, Monto = %s, Fecha_pago = %s, Id_factura = %s, Id_metodo_pago = %s
                    WHERE Id_pago = %s
                """, [
                    data["estado"],
                    data["monto"],
                    data["fecha_pago"],
                    data["id_factura"],
                    data["id_metodo_pago"],
                    pk
                ])
            return Response({"message": "Pago actualizado exitosamente"}, status=200)

        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Pago WHERE Id_pago = %s", [pk])
        return Response({"message": "Pago eliminado exitosamente"}, status=204)

def landing_vista(request):
    return render(request, 'index.html')

def facturacion_vista(request):
    return render(request, 'Factiracion.html')

def alquiler_vista(request):
    return render(request, 'alquiler.html')

def login_vista(request):
    return render(request, 'Login.html')

def registro_vista(request):
    return render(request, 'registro.html')

def venta_vista(request):
    return render(request, 'venta.html')


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

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

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