CREATE SCHEMA consorcio360Bdd;

SET search_path TO consorcio360Bdd;

CREATE TABLE consorcios(
    cuit VARCHAR(11) PRIMARY KEY,
    razon_social VARCHAR(100) NOT NULL,
    calle VARCHAR(100) NOT NULL,
    numero INTEGER NOT NULL CHECK ((numero > 0) AND (numero < 60000)),
    codigo_postal VARCHAR(10) NOT NULL,
    ciudad VARCHAR(50) NOT NULL,
    interes_por_mora DECIMAL(5,2) NOT NULL CHECK (interes_por_mora >= 0),
    redondeo_aumento DECIMAL(5,2) NOT NULL CHECK (redondeo_aumento >= 0)
);

CREATE TABLE propietarios(
    dni VARCHAR(15) PRIMARY KEY CHECK (dni ~~ '^[0-9]+$'),
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(100)
);


CREATE TABLE unidades_funcionales(
    numero_de_unidad_funcional INTEGER,
    cuit_consorcio VARCHAR(11) NOT NULL,
    tipo_de_unidad VARCHAR(50) NOT NULL,
    superficie DECIMAL(7,2) NOT NULL CHECK (superficie > 0),
    dni_propietario VARCHAR(15) NOT NULL,
    FOREIGN KEY (cuit_consorcio) REFERENCES consorcios(cuit),
    FOREIGN KEY (dni_propietario) REFERENCES propietarios(dni),    
    PRIMARY KEY (numero_de_unidad_funcional, cuit_consorcio)
);


CREATE TABLE proveedores(
    cuit VARCHAR(11) PRIMARY KEY,
    razon_social VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(100),
    calle VARCHAR(100) NOT NULL,
    numero INTEGER NOT NULL CHECK ((numero > 0) AND (numero < 60000)),
    codigo_postal VARCHAR(10) NOT NULL,
    ciudad VARCHAR(50) NOT NULL,
    tipo_proveedor VARCHAR(20) NOT NULL CHECK (tipo_proveedor IN ('servicios_mensuales', 'reparaciones_mantenimientos'))
);

-- Especialización: Proveedores de Servicios Mensuales
CREATE TABLE servicios_mensuales(
    cuit VARCHAR(11) PRIMARY KEY,
    numero_cuenta VARCHAR(50) NOT NULL,
    numero_reclamo VARCHAR(50) NOT NULL,
    FOREIGN KEY (cuit) REFERENCES proveedores(cuit) ON DELETE CASCADE
);

-- Especialización: Proveedores de Reparaciones y Mantenimientos
CREATE TABLE reparaciones_mantenimientos(
    cuit VARCHAR(11) PRIMARY KEY,
    numero_reclamo VARCHAR(50) NOT NULL,
    FOREIGN KEY (cuit) REFERENCES proveedores(cuit) ON DELETE CASCADE
);


CREATE TABLE gastos(
    id_gasto SERIAL PRIMARY KEY,
    cuit_consorcio VARCHAR(11) NOT NULL,
    cuit_proveedor VARCHAR(11) NOT NULL,
    periodo DATE NOT NULL,
    descripcion TEXT NOT NULL,
    monto DECIMAL(10,2) NOT NULL CHECK (monto > 0),
    fecha_registro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tipo_gasto VARCHAR(20) NOT NULL CHECK (tipo_gasto IN ('Mantenimiento', 'Servicios', 'Limpieza', 'Seguridad', 'Administracion', 'Otros')) DEFAULT 'Otros',
    estado_pago VARCHAR(20) NOT NULL CHECK (estado_pago IN ('Pendiente', 'Pagado')) DEFAULT 'Pendiente',
    FOREIGN KEY (cuit_consorcio) REFERENCES consorcios(cuit),
    FOREIGN KEY (cuit_proveedor) REFERENCES proveedores(cuit)
);

CREATE TABLE saldo_mensual(
    id_saldo_mensual SERIAL PRIMARY KEY,
    numero_de_unidad_funcional INTEGER NOT NULL,
    cuit_consorcio VARCHAR(11) NOT NULL,
    mes_año DATE NOT NULL,
    saldo_inicial DECIMAL(10,2) NOT NULL DEFAULT 0 CHECK (saldo_inicial >= 0),
    total_gastos DECIMAL(10,2) NOT NULL DEFAULT 0 CHECK (total_gastos >= 0),
    total_pagos DECIMAL(10,2) NOT NULL DEFAULT 0 CHECK (total_pagos >= 0),
    saldo_final DECIMAL(10,2) GENERATED ALWAYS AS (saldo_inicial + total_gastos - total_pagos) STORED,
    fecha_cierre TIMESTAMP,
    UNIQUE(numero_de_unidad_funcional, cuit_consorcio, mes_año),
    FOREIGN KEY (numero_de_unidad_funcional, cuit_consorcio) REFERENCES unidades_funcionales(numero_de_unidad_funcional, cuit_consorcio),
    FOREIGN KEY (cuit_consorcio) REFERENCES consorcios(cuit)
);

CREATE TABLE pagos(
    id_pago SERIAL,
    numero_de_unidad_funcional INTEGER NOT NULL,
    cuit_consorcio VARCHAR(11) NOT NULL,
    dni_propietario VARCHAR(15) NOT NULL,
    monto DECIMAL(10,2) NOT NULL CHECK (monto > 0),
    fecha_pago TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_pago, numero_de_unidad_funcional, cuit_consorcio),
    FOREIGN KEY (numero_de_unidad_funcional, cuit_consorcio) REFERENCES unidades_funcionales(numero_de_unidad_funcional, cuit_consorcio),
    FOREIGN KEY (dni_propietario) REFERENCES propietarios(dni)
);

