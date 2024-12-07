create table Pais(
	Id_pais int primary key,
	Nombre varchar (50) unique,
)
go
create table Departamento(
	Id_departamento int primary key,
	Nombre varchar (50) ,
	Id_pais int foreign key references Pais(Id_pais)
	unique(Id_pais,Nombre)
)
go
create table Ciudad(
	Id_ciudad int primary key,
	Nombre varchar (50) unique,
	Id_pais int foreign key references Pais(Id_pais),
	Id_departamento int foreign key references Departamento(Id_departamento),
	unique(Id_departamento,Nombre)
)
go
create table Colonia(
	Id_colonia int primary key,
	Nombre varchar (50) unique,
	Id_pais int foreign key references Pais(Id_pais),
	Id_departamento int foreign key references Departamento(Id_departamento),
	Id_ciudad int foreign key references Ciudad(Id_ciudad),
	unique(Id_ciudad,Nombre)
)
go
create table Direccion(
	Id_direccion int primary key,
	d_pais int foreign key references Pais(Id_pais),
	Id_departamento int foreign key references Departamento(Id_departamento),
	Id_ciudad int foreign key references Ciudad(Id_ciudad),
	Id_colonia int foreign key references Colonia(Id_colonia),

)
go
create table Marca(
	Id_marca int primary key,
	Nombre varchar (50) unique,

)
go
create table Tipo_seguro(
	Id_tipo_seguro int primary key,
	Nombre varchar (50) unique,
)
go
create table Combustible(
	Id_combustible int primary key,
	Nombre varchar (50) unique,

)
go
create table Estado(
	Id_estado int primary key,
	Nombre varchar (50) unique,

)
go
create table Modelo(
	Id_modelo int primary key,
	Nombre varchar (50) unique,
	Id_marca int foreign key references Marca(Id_marca),
)
go
create table Tipo_transaccion(
	Id_tipo_transaccion int primary key,
	Nombre varchar (50) unique,

)
go
create table Sucursal(
	Id_sucursal int primary key,
	Nombre varchar (50) unique,
	telefono int,
	Id_direccion int foreign key references Direccion(id_direccion)
)
go
create table Parqueo(
	Id_parqueo int primary key,
	Lote int unique,
	Referencia varchar (100),
	Id_sucursal int foreign key references Sucursal(Id_sucursal),
)
go

create table Usuario(
	Id_usuario int primary key,
	Nombre varchar (50) ,
	Nombre_pila varchar (50), 
	Apellido varchar (50) ,
	Apellido_pila varchar (50), 
	Correo varchar (50) unique,
	Telefono int,
	Contraseña varchar (50),
	fecha_ingreso date,
	fecha_salida date null,
	Id_direccion int foreign key references Direccion(Id_direccion),

)
go
create table Cliente(
	Id_cliente int primary key,
	Id_usuario int foreign key references Usuario(Id_usuario)
)
go
create table Empleado(
	Id_Empleado int primary key,
	Id_usuario int foreign key references Usuario(Id_usuario),
	Id_sucursal int foreign key references Sucursal(Id_sucursal),
)
go
create table Vehiculo(
	Id_Vehiculo int primary key,
	Ano int,
	Vin int unique,
	Motor int,
	Matricula varchar (50) unique,
	Disponibilidad bit,
	Precio int,
	Id_marca int foreign key references Marca(Id_marca),
	Id_modelo int foreign key references Modelo(Id_modelo),
	Id_estado int foreign key references Estado(Id_estado),
	Id_tipo_transaccion int foreign key references Tipo_transaccion(Id_tipo_transaccion),
	Id_combustible int foreign key references Combustible(Id_combustible),
	Id_sucursal int foreign key references Sucursal(Id_sucursal),
	Id_Parqueo int foreign key references Parqueo(Id_parqueo),
)
go
create table Color(
	Id_color int primary key,
	Nombre varchar (50) unique,
	Id_vehiculo int foreign key references Vehiculo(Id_vehiculo),
	unique(Nombre,Id_vehiculo),
)
go

create table Rango(
	Id_rango int primary key,
	Inicio int unique,
	Fin int unique,
	unique(Inicio,Fin)
)
go
create table SAR(
	Id_sar int primary key,
	Fecha_limite date,
	Num_trans int,
	Id_tipo_transaccion int foreign key references Tipo_transaccion(Id_tipo_transaccion),
	Id_rango int foreign key references Rango(Id_rango),
	Id_sucursal int foreign key references Sucursal(Id_sucursal),

)
go

create table Detalle_factura(
	Id_detalle_factura int primary key,
	descuento int null,
	Id_vehiculo int foreign key references Vehiculo(Id_vehiculo),
)
go

create table Metodo_pago(
	Id_metodo_pago int primary key,
	Nombre varchar (50) unique,
)
go
create table Factura(
	Id_factura int primary key,
	Fecha_emision date,
	Total int,
	Id_detalle_factura int foreign key references Detalle_factura(Id_detalle_factura),
	Id_tipo_transaccion int foreign key references Tipo_transaccion(Id_tipo_transaccion),
	Id_cliente int foreign key references Cliente(Id_cliente),
	Id_empleado int foreign key references Empleado(Id_empleado),
	Id_sar int foreign key references SAR(Id_sar),
)
go


create table Pago(
	Id_pago int primary key,
	Estado bit,
	Monto int,
	fecha_pago date,
	Id_factura int foreign key references Factura(Id_factura),
	Id_metodo_pago int foreign key references Metodo_pago(Id_metodo_pago),
)
go

CREATE PROCEDURE InsertarCliente
    @Nombre VARCHAR(50),
    @NombrePila VARCHAR(50),
    @Apellido VARCHAR(50),
    @ApellidoPila VARCHAR(50),
    @Correo VARCHAR(50),
    @Telefono BIGINT,
    @Contraseña VARCHAR(50),
    @FechaIngreso DATE,
    @IdColonia INT
AS
BEGIN
    BEGIN TRANSACTION;
    BEGIN TRY

        DECLARE @IdDireccion INT;
        INSERT INTO Direccion (Id_colonia)
        VALUES (@IdColonia);
        SET @IdDireccion = SCOPE_IDENTITY();


        DECLARE @IdUsuario INT;
        INSERT INTO Usuario (Nombre, Nombre_pila, Apellido, Apellido_pila, Correo, Telefono, Contraseña, Fecha_ingreso, Id_direccion)
        VALUES (@Nombre, @NombrePila, @Apellido, @ApellidoPila, @Correo, @Telefono, @Contraseña, @FechaIngreso, @IdDireccion);
        SET @IdUsuario = SCOPE_IDENTITY();


        INSERT INTO Cliente (Id_usuario)
        VALUES (@IdUsuario);

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
GO

CREATE PROCEDURE ActualizarDisponibilidadVehiculo
    @IdVehiculo INT,
    @Disponibilidad BIT
AS
BEGIN
    BEGIN TRY

        UPDATE Vehiculo
        SET Disponibilidad = @Disponibilidad
        WHERE Id_vehiculo = @IdVehiculo;

        PRINT 'Disponibilidad del vehículo actualizada correctamente.';
    END TRY
    BEGIN CATCH
        PRINT 'Error al actualizar la disponibilidad del vehículo.';
        THROW;
    END CATCH
END;
GO


CREATE VIEW VEHICULOS AS 
SELECT 
    V.Id_vehiculo AS VehiculoID,
    M.Nombre AS Marca,
    Mo.Nombre AS Modelo,
    V.Precio AS Precio,
    V.Ano AS Año,
    V.Matricula AS Matricula,
    E.Nombre AS Estado,
    S.Nombre AS Sucursal
FROM 
    Vehiculo V
    INNER JOIN Marca M ON V.Id_marca = M.Id_marca
    INNER JOIN Modelo Mo ON V.Id_modelo = Mo.Id_modelo
    INNER JOIN Estado E ON V.Id_estado = E.Id_estado
    INNER JOIN Sucursal S ON V.Id_sucursal = S.Id_sucursal
WHERE 
    V.Disponibilidad = 1;
go

CREATE VIEW Vista_Facturas_Detalladas AS
SELECT 
    f.Id_factura,
    f.Fecha_emision,
    f.Total,
    

    df.Id_detalle_factura,
    df.descuento,
    v.Id_vehiculo,

    
    tt.Id_tipo_transaccion,
    tt.Nombre AS Tipo_Transaccion_Nombre,

    c.Id_cliente,
    u_cli.Id_usuario AS Cliente_Id_Usuario,
    u_cli.Nombre AS Cliente_Nombre,


    e.Id_empleado,
    u_emp.Id_usuario AS Empleado_Id_Usuario,
    u_emp.Nombre AS Empleado_Nombre,
    s_emp.Id_sucursal AS Empleado_Id_Sucursal,
    s_emp.Nombre AS Sucursal_Empleado_Nombre,


    sar.Id_sar,
    sar.Fecha_limite AS Sar_Fecha_Limite,
    sar.Num_trans AS Sar_Num_Trans,
    tt_sar.Id_tipo_transaccion AS Sar_Id_Tipo_Transaccion,
    r.Id_rango AS Sar_Id_Rango,
    s_sar.Id_sucursal AS Sar_Id_Sucursal

FROM Factura f
LEFT JOIN Detalle_factura df ON f.Id_detalle_factura = df.Id_detalle_factura
LEFT JOIN Vehiculo v ON df.Id_vehiculo = v.Id_vehiculo
LEFT JOIN Tipo_transaccion tt ON f.Id_tipo_transaccion = tt.Id_tipo_transaccion
LEFT JOIN Cliente c ON f.Id_cliente = c.Id_cliente
LEFT JOIN Usuario u_cli ON c.Id_usuario = u_cli.Id_usuario
LEFT JOIN Empleado e ON f.Id_empleado = e.Id_empleado
LEFT JOIN Usuario u_emp ON e.Id_usuario = u_emp.Id_usuario
LEFT JOIN Sucursal s_emp ON e.Id_sucursal = s_emp.Id_sucursal
LEFT JOIN SAR sar ON f.Id_sar = sar.Id_sar
LEFT JOIN Tipo_transaccion tt_sar ON sar.Id_tipo_transaccion = tt_sar.Id_tipo_transaccion
LEFT JOIN Rango r ON sar.Id_rango = r.Id_rango
LEFT JOIN Sucursal s_sar ON sar.Id_sucursal = s_sar.Id_sucursal;
go

Select * from factura;
select * from usuario;
select * from pais;
SELECT * FROM Vista_Facturas_Detalladas;
SELECT * FROM VEHICULOS;
Select * from Marca;

EXEC ActualizarDisponibilidadVehiculo
    @IdVehiculo = 1,
    @Disponibilidad = 1; 