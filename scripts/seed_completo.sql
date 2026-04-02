-- ============================================================
-- SEED MASIVO STAGING — Propietarios + UFs + Gastos 36 períodos
-- Consorcios: 6 | Propietarios: ~200 | UFs: ~180 | Gastos: 1512
-- ============================================================

BEGIN;

-- ============================================================
-- 1. PROPIETARIOS (~200 total, actualmente hay 60)
-- ============================================================
INSERT INTO propietarios (dni, nombre, apellido, telefono, email) VALUES
-- Tanda 2 (DNI 20000000–20000039) — 40 propietarios nuevos
('20000001','Valentina','Ruiz','1131000001','valentina.ruiz1@fakemail.com'),
('20000002','Matias','Sosa','1131000002','matias.sosa2@fakemail.com'),
('20000003','Luciana','Medina','1131000003','luciana.medina3@fakemail.com'),
('20000004','Ezequiel','Castro','1131000004','ezequiel.castro4@fakemail.com'),
('20000005','Florencia','Romero','1131000005','florencia.romero5@fakemail.com'),
('20000006','Nicolas','Gutierrez','1131000006','nicolas.gutierrez6@fakemail.com'),
('20000007','Camila','Diaz','1131000007','camila.diaz7@fakemail.com'),
('20000008','Santiago','Vargas','1131000008','santiago.vargas8@fakemail.com'),
('20000009','Agustina','Moreno','1131000009','agustina.moreno9@fakemail.com'),
('20000010','Leandro','Jimenez','1131000010','leandro.jimenez10@fakemail.com'),
('20000011','Micaela','Alvarez','1131000011','micaela.alvarez11@fakemail.com'),
('20000012','Facundo','Herrera','1131000012','facundo.herrera12@fakemail.com'),
('20000013','Rocio','Torres','1131000013','rocio.torres13@fakemail.com'),
('20000014','Ignacio','Flores','1131000014','ignacio.flores14@fakemail.com'),
('20000015','Melina','Reyes','1131000015','melina.reyes15@fakemail.com'),
('20000016','Tomas','Cruz','1131000016','tomas.cruz16@fakemail.com'),
('20000017','Natalia','Ortiz','1131000017','natalia.ortiz17@fakemail.com'),
('20000018','Rodrigo','Ramos','1131000018','rodrigo.ramos18@fakemail.com'),
('20000019','Silvana','Mendez','1131000019','silvana.mendez19@fakemail.com'),
('20000020','Mauricio','Vega','1131000020','mauricio.vega20@fakemail.com'),
('20000021','Daniela','Nunez','1131000021','daniela.nunez21@fakemail.com'),
('20000022','Pablo','Rojas','1131000022','pablo.rojas22@fakemail.com'),
('20000023','Lorena','Aguilar','1131000023','lorena.aguilar23@fakemail.com'),
('20000024','Cristian','Silva','1131000024','cristian.silva24@fakemail.com'),
('20000025','Paola','Paredes','1131000025','paola.paredes25@fakemail.com'),
('20000026','Adrian','Molina','1131000026','adrian.molina26@fakemail.com'),
('20000027','Vanesa','Suarez','1131000027','vanesa.suarez27@fakemail.com'),
('20000028','Claudio','Delgado','1131000028','claudio.delgado28@fakemail.com'),
('20000029','Karina','Ibarra','1131000029','karina.ibarra29@fakemail.com'),
('20000030','Sergio','Pena','1131000030','sergio.pena30@fakemail.com'),
('20000031','Laura','Cabrera','1131000031','laura.cabrera31@fakemail.com'),
('20000032','Ariel','Rios','1131000032','ariel.rios32@fakemail.com'),
('20000033','Patricia','Sandoval','1131000033','patricia.sandoval33@fakemail.com'),
('20000034','Gustavo','Acosta','1131000034','gustavo.acosta34@fakemail.com'),
('20000035','Monica','Miranda','1131000035','monica.miranda35@fakemail.com'),
('20000036','Roberto','Lara','1131000036','roberto.lara36@fakemail.com'),
('20000037','Claudia','Fuentes','1131000037','claudia.fuentes37@fakemail.com'),
('20000038','Eduardo','Ponce','1131000038','eduardo.ponce38@fakemail.com'),
('20000039','Graciela','Carrasco','1131000039','graciela.carrasco39@fakemail.com'),
('20000040','Hugo','Navarro','1131000040','hugo.navarro40@fakemail.com'),
-- Tanda 3 (DNI 20000041–20000100) — 60 propietarios más
('20000041','Beatriz','Espinoza','1131000041','beatriz.espinoza41@fakemail.com'),
('20000042','Oscar','Contreras','1131000042','oscar.contreras42@fakemail.com'),
('20000043','Roxana','Vera','1131000043','roxana.vera43@fakemail.com'),
('20000044','Walter','Dominguez','1131000044','walter.dominguez44@fakemail.com'),
('20000045','Marcela','Guerrero','1131000045','marcela.guerrero45@fakemail.com'),
('20000046','Raul','Campos','1131000046','raul.campos46@fakemail.com'),
('20000047','Susana','Cortez','1131000047','susana.cortez47@fakemail.com'),
('20000048','Jorge','Castillo','1131000048','jorge.castillo48@fakemail.com'),
('20000049','Alicia','Reyna','1131000049','alicia.reyna49@fakemail.com'),
('20000050','Carlos','Villanueva','1131000050','carlos.villanueva50@fakemail.com'),
('20000051','Silvia','Leon','1131000051','silvia.leon51@fakemail.com'),
('20000052','Ricardo','Marquez','1131000052','ricardo.marquez52@fakemail.com'),
('20000053','Alejandra','Avila','1131000053','alejandra.avila53@fakemail.com'),
('20000054','Mario','Montoya','1131000054','mario.montoya54@fakemail.com'),
('20000055','Viviana','Cardenas','1131000055','viviana.cardenas55@fakemail.com'),
('20000056','Hector','Rangel','1131000056','hector.rangel56@fakemail.com'),
('20000057','Norma','Fuentes','1131000057','norma.fuentes57@fakemail.com'),
('20000058','Alberto','Pacheco','1131000058','alberto.pacheco58@fakemail.com'),
('20000059','Liliana','Arias','1131000059','liliana.arias59@fakemail.com'),
('20000060','Fernando','Meza','1131000060','fernando.meza60@fakemail.com'),
('20000061','Rosa','Palacios','1131000061','rosa.palacios61@fakemail.com'),
('20000062','Victor','Escobar','1131000062','victor.escobar62@fakemail.com'),
('20000063','Elsa','Serrano','1131000063','elsa.serrano63@fakemail.com'),
('20000064','Julio','Mora','1131000064','julio.mora64@fakemail.com'),
('20000065','Gloria','Vargas','1131000065','gloria.vargas65@fakemail.com'),
('20000066','Marco','Perez','1131000066','marco.perez66@fakemail.com'),
('20000067','Irma','Calderon','1131000067','irma.calderon67@fakemail.com'),
('20000068','Rafael','Delgado','1131000068','rafael.delgado68@fakemail.com'),
('20000069','Amelia','Salinas','1131000069','amelia.salinas69@fakemail.com'),
('20000070','Felipe','Heredia','1131000070','felipe.heredia70@fakemail.com'),
('20000071','Josefina','Tapia','1131000071','josefina.tapia71@fakemail.com'),
('20000072','Ernesto','Ibarra','1131000072','ernesto.ibarra72@fakemail.com'),
('20000073','Amparo','Fuentes','1131000073','amparo.fuentes73@fakemail.com'),
('20000074','Andres','Soto','1131000074','andres.soto74@fakemail.com'),
('20000075','Esperanza','Vidal','1131000075','esperanza.vidal75@fakemail.com'),
('20000076','Marcos','Bravo','1131000076','marcos.bravo76@fakemail.com'),
('20000077','Olga','Pinto','1131000077','olga.pinto77@fakemail.com'),
('20000078','Alfredo','Bustos','1131000078','alfredo.bustos78@fakemail.com'),
('20000079','Teresa','Cano','1131000079','teresa.cano79@fakemail.com'),
('20000080','Leonardo','Moran','1131000080','leonardo.moran80@fakemail.com'),
('20000081','Yolanda','Parra','1131000081','yolanda.parra81@fakemail.com'),
('20000082','Enrique','Vega','1131000082','enrique.vega82@fakemail.com'),
('20000083','Pilar','Robles','1131000083','pilar.robles83@fakemail.com'),
('20000084','Cesar','Villalba','1131000084','cesar.villalba84@fakemail.com'),
('20000085','Marta','Quiroga','1131000085','marta.quiroga85@fakemail.com'),
('20000086','Luis','Barragan','1131000086','luis.barragan86@fakemail.com'),
('20000087','Elena','Zapata','1131000087','elena.zapata87@fakemail.com'),
('20000088','Ramon','Acevedo','1131000088','ramon.acevedo88@fakemail.com'),
('20000089','Carmen','Salcedo','1131000089','carmen.salcedo89@fakemail.com'),
('20000090','Juan','Cifuentes','1131000090','juan.cifuentes90@fakemail.com'),
('20000091','Ana','Betancourt','1131000091','ana.betancourt91@fakemail.com'),
('20000092','Pedro','Lozano','1131000092','pedro.lozano92@fakemail.com'),
('20000093','Maria','Vergara','1131000093','maria.vergara93@fakemail.com'),
('20000094','Jose','Montero','1131000094','jose.montero94@fakemail.com'),
('20000095','Isabel','Naranjo','1131000095','isabel.naranjo95@fakemail.com'),
('20000096','Manuel','Pulido','1131000096','manuel.pulido96@fakemail.com'),
('20000097','Antonia','Rivas','1131000097','antonia.rivas97@fakemail.com'),
('20000098','Francisco','Duran','1131000098','francisco.duran98@fakemail.com'),
('20000099','Dolores','Blanco','1131000099','dolores.blanco99@fakemail.com'),
('20000100','Guillermo','Iglesias','1131000100','guillermo.iglesias100@fakemail.com')
ON CONFLICT (dni) DO NOTHING;

-- ============================================================
-- 2. UNIDADES FUNCIONALES (~180 UFs, 30 por consorcio)
-- Tipos: edificios → Departamento/PH | barrios → Lote
-- Coeficientes distribuidos proporcionalmente
-- ============================================================

INSERT INTO unidades_funcionales
    (numero_de_unidad_funcional, tipo_de_unidad, estado_de_vivienda, superficie, cuit_consorcio, dni_propietario, coeficiente)
SELECT
    uf.numero,
    uf.tipo,
    uf.estado,
    uf.superficie,
    uf.cuit_consorcio,
    uf.dni_propietario,
    uf.coeficiente
FROM (VALUES
    -- ── Consorcio 30800000001 — Torres del Sol (edificio, 30 UFs, Depto/PH) ──
    (1,'Departamento','Propietario',42.00,'30800000001','20000001',0.0280),
    (2,'Departamento','Propietario',42.00,'30800000001','20000002',0.0280),
    (3,'Departamento','Inquilino',   48.00,'30800000001','20000003',0.0320),
    (4,'Departamento','Propietario',48.00,'30800000001','20000004',0.0320),
    (5,'Departamento','Propietario',55.00,'30800000001','20000005',0.0367),
    (6,'Departamento','Inquilino',   55.00,'30800000001','20000006',0.0367),
    (7,'Departamento','Propietario',60.00,'30800000001','20000007',0.0400),
    (8,'Departamento','Propietario',60.00,'30800000001','20000008',0.0400),
    (9,'Departamento','Vacio',       65.00,'30800000001','20000009',0.0433),
    (10,'Departamento','Propietario',65.00,'30800000001','20000010',0.0433),
    (11,'Departamento','Propietario',42.00,'30800000001','20000011',0.0280),
    (12,'Departamento','Inquilino',  42.00,'30800000001','20000012',0.0280),
    (13,'Departamento','Propietario',48.00,'30800000001','20000013',0.0320),
    (14,'Departamento','Propietario',48.00,'30800000001','20000014',0.0320),
    (15,'Departamento','Propietario',55.00,'30800000001','20000015',0.0367),
    (16,'Departamento','Propietario',55.00,'30800000001','20000016',0.0367),
    (17,'Departamento','Propietario',60.00,'30800000001','20000017',0.0400),
    (18,'Departamento','Vacio',      60.00,'30800000001','20000018',0.0400),
    (19,'Departamento','Propietario',65.00,'30800000001','20000019',0.0433),
    (20,'Departamento','Propietario',65.00,'30800000001','20000020',0.0433),
    (21,'PH','Propietario',          80.00,'30800000001','20000021',0.0533),
    (22,'PH','Propietario',          80.00,'30800000001','20000022',0.0533),
    (23,'Departamento','Propietario',42.00,'30800000001','20000023',0.0280),
    (24,'Departamento','Inquilino',  42.00,'30800000001','20000024',0.0280),
    (25,'Departamento','Propietario',48.00,'30800000001','20000025',0.0320),
    (26,'Departamento','Propietario',48.00,'30800000001','20000026',0.0320),
    (27,'Departamento','Propietario',55.00,'30800000001','20000027',0.0367),
    (28,'Departamento','Propietario',55.00,'30800000001','20000028',0.0367),
    (29,'PH','Propietario',          90.00,'30800000001','20000029',0.0600),
    (30,'PH','Inquilino',            90.00,'30800000001','20000030',0.0600),

    -- ── Consorcio 30800000002 — Palermo Verde (edificio, 30 UFs) ──
    (1,'Departamento','Propietario',38.00,'30800000002','20000031',0.0267),
    (2,'Departamento','Propietario',38.00,'30800000002','20000032',0.0267),
    (3,'Departamento','Propietario',45.00,'30800000002','20000033',0.0317),
    (4,'Departamento','Inquilino',   45.00,'30800000002','20000034',0.0317),
    (5,'Departamento','Propietario',52.00,'30800000002','20000035',0.0367),
    (6,'Departamento','Propietario',52.00,'30800000002','20000036',0.0367),
    (7,'Departamento','Propietario',58.00,'30800000002','20000037',0.0408),
    (8,'Departamento','Vacio',       58.00,'30800000002','20000038',0.0408),
    (9,'Departamento','Propietario',64.00,'30800000002','20000039',0.0450),
    (10,'Departamento','Propietario',64.00,'30800000002','20000040',0.0450),
    (11,'Departamento','Propietario',38.00,'30800000002','20000041',0.0267),
    (12,'Departamento','Inquilino',  38.00,'30800000002','20000042',0.0267),
    (13,'Departamento','Propietario',45.00,'30800000002','20000043',0.0317),
    (14,'Departamento','Propietario',45.00,'30800000002','20000044',0.0317),
    (15,'Departamento','Propietario',52.00,'30800000002','20000045',0.0367),
    (16,'Departamento','Propietario',52.00,'30800000002','20000046',0.0367),
    (17,'Departamento','Vacio',      58.00,'30800000002','20000047',0.0408),
    (18,'Departamento','Propietario',58.00,'30800000002','20000048',0.0408),
    (19,'Departamento','Propietario',64.00,'30800000002','20000049',0.0450),
    (20,'Departamento','Propietario',64.00,'30800000002','20000050',0.0450),
    (21,'PH','Propietario',          85.00,'30800000002','20000051',0.0600),
    (22,'PH','Inquilino',            85.00,'30800000002','20000052',0.0600),
    (23,'Departamento','Propietario',38.00,'30800000002','20000053',0.0267),
    (24,'Departamento','Propietario',38.00,'30800000002','20000054',0.0267),
    (25,'Departamento','Propietario',45.00,'30800000002','20000055',0.0317),
    (26,'Departamento','Inquilino',  45.00,'30800000002','20000056',0.0317),
    (27,'Departamento','Propietario',52.00,'30800000002','20000057',0.0367),
    (28,'Departamento','Propietario',52.00,'30800000002','20000058',0.0367),
    (29,'PH','Propietario',          95.00,'30800000002','20000059',0.0667),
    (30,'PH','Propietario',          95.00,'30800000002','20000060',0.0667),

    -- ── Consorcio 30800000003 — Barrio San Martin (barrio, 30 lotes) ──
    (1,'Lote','Propietario',200.00,'30800000003','20000061',0.6000),
    (2,'Lote','Propietario',200.00,'30800000003','20000062',0.6000),
    (3,'Lote','Propietario',200.00,'30800000003','20000063',0.6000),
    (4,'Lote','Propietario',200.00,'30800000003','20000064',0.6000),
    (5,'Lote','Propietario',200.00,'30800000003','20000065',0.6000),
    (6,'Lote','Propietario',200.00,'30800000003','20000066',0.6000),
    (7,'Lote','Propietario',200.00,'30800000003','20000067',0.6000),
    (8,'Lote','Propietario',200.00,'30800000003','20000068',0.6000),
    (9,'Lote','Propietario',200.00,'30800000003','20000069',0.6000),
    (10,'Lote','Propietario',200.00,'30800000003','20000070',0.6000),
    (11,'Lote','Propietario',250.00,'30800000003','20000071',0.7000),
    (12,'Lote','Propietario',250.00,'30800000003','20000072',0.7000),
    (13,'Lote','Propietario',250.00,'30800000003','20000073',0.7000),
    (14,'Lote','Propietario',250.00,'30800000003','20000074',0.7000),
    (15,'Lote','Propietario',250.00,'30800000003','20000075',0.7000),
    (16,'Lote','Propietario',250.00,'30800000003','20000076',0.7000),
    (17,'Lote','Propietario',250.00,'30800000003','20000077',0.7000),
    (18,'Lote','Propietario',250.00,'30800000003','20000078',0.7000),
    (19,'Lote','Propietario',250.00,'30800000003','20000079',0.7000),
    (20,'Lote','Propietario',250.00,'30800000003','20000080',0.7000),
    (21,'Lote','Propietario',300.00,'30800000003','20000081',0.8000),
    (22,'Lote','Propietario',300.00,'30800000003','20000082',0.8000),
    (23,'Lote','Propietario',300.00,'30800000003','20000083',0.8000),
    (24,'Lote','Propietario',300.00,'30800000003','20000084',0.8000),
    (25,'Lote','Propietario',300.00,'30800000003','20000085',0.8000),
    (26,'Lote','Propietario',350.00,'30800000003','20000086',0.9000),
    (27,'Lote','Propietario',350.00,'30800000003','20000087',0.9000),
    (28,'Lote','Propietario',350.00,'30800000003','20000088',0.9000),
    (29,'Lote','Propietario',350.00,'30800000003','20000089',0.9000),
    (30,'Lote','Propietario',350.00,'30800000003','20000090',0.9000),

    -- ── Consorcio 30800000004 — Tigre Norte (barrio, 30 lotes) ──
    (1,'Lote','Propietario',180.00,'30800000004','20000091',0.6000),
    (2,'Lote','Propietario',180.00,'30800000004','20000092',0.6000),
    (3,'Lote','Propietario',180.00,'30800000004','20000093',0.6000),
    (4,'Lote','Propietario',180.00,'30800000004','20000094',0.6000),
    (5,'Lote','Propietario',180.00,'30800000004','20000095',0.6000),
    (6,'Lote','Propietario',180.00,'30800000004','20000096',0.6000),
    (7,'Lote','Propietario',180.00,'30800000004','20000097',0.6000),
    (8,'Lote','Propietario',180.00,'30800000004','20000098',0.6000),
    (9,'Lote','Propietario',180.00,'30800000004','20000099',0.6000),
    (10,'Lote','Propietario',180.00,'30800000004','20000100',0.6000),
    (11,'Lote','Propietario',230.00,'30800000004','20000001',0.7000),
    (12,'Lote','Propietario',230.00,'30800000004','20000002',0.7000),
    (13,'Lote','Propietario',230.00,'30800000004','20000003',0.7000),
    (14,'Lote','Propietario',230.00,'30800000004','20000004',0.7000),
    (15,'Lote','Propietario',230.00,'30800000004','20000005',0.7000),
    (16,'Lote','Propietario',230.00,'30800000004','20000006',0.7000),
    (17,'Lote','Propietario',230.00,'30800000004','20000007',0.7000),
    (18,'Lote','Propietario',230.00,'30800000004','20000008',0.7000),
    (19,'Lote','Propietario',230.00,'30800000004','20000009',0.7000),
    (20,'Lote','Propietario',230.00,'30800000004','20000010',0.7000),
    (21,'Lote','Propietario',280.00,'30800000004','20000011',0.8000),
    (22,'Lote','Propietario',280.00,'30800000004','20000012',0.8000),
    (23,'Lote','Propietario',280.00,'30800000004','20000013',0.8000),
    (24,'Lote','Propietario',280.00,'30800000004','20000014',0.8000),
    (25,'Lote','Propietario',280.00,'30800000004','20000015',0.8000),
    (26,'Lote','Propietario',320.00,'30800000004','20000016',0.9000),
    (27,'Lote','Propietario',320.00,'30800000004','20000017',0.9000),
    (28,'Lote','Propietario',320.00,'30800000004','20000018',0.9000),
    (29,'Lote','Propietario',320.00,'30800000004','20000019',0.9000),
    (30,'Lote','Propietario',320.00,'30800000004','20000020',0.9000),

    -- ── Consorcio 30800000005 — Recoleta Premium (edificio, 30 UFs) ──
    (1,'Departamento','Propietario',55.00,'30800000005','20000021',0.0314),
    (2,'Departamento','Propietario',55.00,'30800000005','20000022',0.0314),
    (3,'Departamento','Propietario',65.00,'30800000005','20000023',0.0371),
    (4,'Departamento','Inquilino',   65.00,'30800000005','20000024',0.0371),
    (5,'Departamento','Propietario',75.00,'30800000005','20000025',0.0429),
    (6,'Departamento','Propietario',75.00,'30800000005','20000026',0.0429),
    (7,'Departamento','Propietario',85.00,'30800000005','20000027',0.0486),
    (8,'Departamento','Propietario',85.00,'30800000005','20000028',0.0486),
    (9,'Departamento','Vacio',       95.00,'30800000005','20000029',0.0543),
    (10,'Departamento','Propietario',95.00,'30800000005','20000030',0.0543),
    (11,'Departamento','Propietario',55.00,'30800000005','20000031',0.0314),
    (12,'Departamento','Propietario',55.00,'30800000005','20000032',0.0314),
    (13,'Departamento','Inquilino',  65.00,'30800000005','20000033',0.0371),
    (14,'Departamento','Propietario',65.00,'30800000005','20000034',0.0371),
    (15,'Departamento','Propietario',75.00,'30800000005','20000035',0.0429),
    (16,'Departamento','Propietario',75.00,'30800000005','20000036',0.0429),
    (17,'Departamento','Propietario',85.00,'30800000005','20000037',0.0486),
    (18,'Departamento','Vacio',      85.00,'30800000005','20000038',0.0486),
    (19,'Departamento','Propietario',95.00,'30800000005','20000039',0.0543),
    (20,'Departamento','Propietario',95.00,'30800000005','20000040',0.0543),
    (21,'PH','Propietario',         110.00,'30800000005','20000041',0.0629),
    (22,'PH','Propietario',         110.00,'30800000005','20000042',0.0629),
    (23,'Departamento','Propietario',55.00,'30800000005','20000043',0.0314),
    (24,'Departamento','Propietario',65.00,'30800000005','20000044',0.0371),
    (25,'Departamento','Inquilino',  75.00,'30800000005','20000045',0.0429),
    (26,'Departamento','Propietario',75.00,'30800000005','20000046',0.0429),
    (27,'Departamento','Propietario',85.00,'30800000005','20000047',0.0486),
    (28,'Departamento','Propietario',85.00,'30800000005','20000048',0.0486),
    (29,'PH','Propietario',         120.00,'30800000005','20000049',0.0686),
    (30,'PH','Inquilino',           120.00,'30800000005','20000050',0.0686),

    -- ── Consorcio 30800000006 — Los Alamos (barrio, 30 lotes) ──
    (1,'Lote','Propietario',160.00,'30800000006','20000051',0.6000),
    (2,'Lote','Propietario',160.00,'30800000006','20000052',0.6000),
    (3,'Lote','Propietario',160.00,'30800000006','20000053',0.6000),
    (4,'Lote','Propietario',160.00,'30800000006','20000054',0.6000),
    (5,'Lote','Propietario',160.00,'30800000006','20000055',0.6000),
    (6,'Lote','Propietario',160.00,'30800000006','20000056',0.6000),
    (7,'Lote','Propietario',160.00,'30800000006','20000057',0.6000),
    (8,'Lote','Propietario',160.00,'30800000006','20000058',0.6000),
    (9,'Lote','Propietario',160.00,'30800000006','20000059',0.6000),
    (10,'Lote','Propietario',160.00,'30800000006','20000060',0.6000),
    (11,'Lote','Propietario',210.00,'30800000006','20000061',0.7000),
    (12,'Lote','Propietario',210.00,'30800000006','20000062',0.7000),
    (13,'Lote','Propietario',210.00,'30800000006','20000063',0.7000),
    (14,'Lote','Propietario',210.00,'30800000006','20000064',0.7000),
    (15,'Lote','Propietario',210.00,'30800000006','20000065',0.7000),
    (16,'Lote','Propietario',210.00,'30800000006','20000066',0.7000),
    (17,'Lote','Propietario',210.00,'30800000006','20000067',0.7000),
    (18,'Lote','Propietario',210.00,'30800000006','20000068',0.7000),
    (19,'Lote','Propietario',210.00,'30800000006','20000069',0.7000),
    (20,'Lote','Propietario',210.00,'30800000006','20000070',0.7000),
    (21,'Lote','Propietario',260.00,'30800000006','20000071',0.8000),
    (22,'Lote','Propietario',260.00,'30800000006','20000072',0.8000),
    (23,'Lote','Propietario',260.00,'30800000006','20000073',0.8000),
    (24,'Lote','Propietario',260.00,'30800000006','20000074',0.8000),
    (25,'Lote','Propietario',260.00,'30800000006','20000075',0.8000),
    (26,'Lote','Propietario',310.00,'30800000006','20000076',0.9000),
    (27,'Lote','Propietario',310.00,'30800000006','20000077',0.9000),
    (28,'Lote','Propietario',310.00,'30800000006','20000078',0.9000),
    (29,'Lote','Propietario',310.00,'30800000006','20000079',0.9000),
    (30,'Lote','Propietario',310.00,'30800000006','20000080',0.9000)

) AS uf(numero, tipo, estado, superficie, cuit_consorcio, dni_propietario, coeficiente)
ON CONFLICT (numero_de_unidad_funcional, cuit_consorcio) DO NOTHING;

-- ============================================================
-- 3. GASTOS — 36 períodos × 6 consorcios × 7 gastos = 1512
-- ============================================================
INSERT INTO gastos (periodo, descripcion, monto, fecha_registro, tipo_gasto, estado_pago, cuit_consorcio, cuit_proveedor)
SELECT
    periodo,
    descripcion,
    ROUND(monto_base * POWER(1.05, periodo_idx), 2),
    NOW(),
    tipo_gasto,
    CASE WHEN periodo < '2026-01-01' THEN 'Pagado' ELSE 'Pendiente' END,
    cuit_consorcio,
    '30698765432'
FROM (
    SELECT p.periodo, p.periodo_idx, c.cuit_consorcio, g.descripcion, g.monto_base, g.tipo_gasto
    FROM
        (VALUES
            ('2024-01-01'::date,0),('2024-02-01'::date,1),('2024-03-01'::date,2),
            ('2024-04-01'::date,3),('2024-05-01'::date,4),('2024-06-01'::date,5),
            ('2024-07-01'::date,6),('2024-08-01'::date,7),('2024-09-01'::date,8),
            ('2024-10-01'::date,9),('2024-11-01'::date,10),('2024-12-01'::date,11),
            ('2025-01-01'::date,12),('2025-02-01'::date,13),('2025-03-01'::date,14),
            ('2025-04-01'::date,15),('2025-05-01'::date,16),('2025-06-01'::date,17),
            ('2025-07-01'::date,18),('2025-08-01'::date,19),('2025-09-01'::date,20),
            ('2025-10-01'::date,21),('2025-11-01'::date,22),('2025-12-01'::date,23),
            ('2026-01-01'::date,24),('2026-02-01'::date,25),('2026-03-01'::date,26),
            ('2026-04-01'::date,27),('2026-05-01'::date,28),('2026-06-01'::date,29),
            ('2026-07-01'::date,30),('2026-08-01'::date,31),('2026-09-01'::date,32),
            ('2026-10-01'::date,33),('2026-11-01'::date,34),('2026-12-01'::date,35)
        ) AS p(periodo, periodo_idx)
    CROSS JOIN
        (VALUES ('30800000001'),('30800000002'),('30800000003'),('30800000004'),('30800000005'),('30800000006')) AS c(cuit_consorcio)
    CROSS JOIN
        (VALUES
            ('Seguridad',1800000.00,'Seguridad'),
            ('Mantenimiento',420000.00,'Mantenimiento'),
            ('Agua',180000.00,'Servicios'),
            ('Electricidad',145000.00,'Servicios'),
            ('Honorarios administracion',340000.00,'Administracion'),
            ('Limpieza',220000.00,'Mantenimiento'),
            ('Seguro',150000.00,'Otros')
        ) AS g(descripcion, monto_base, tipo_gasto)
) AS datos
WHERE NOT EXISTS (
    SELECT 1 FROM gastos ex
    WHERE ex.cuit_consorcio = datos.cuit_consorcio
      AND ex.periodo = datos.periodo
      AND ex.descripcion = datos.descripcion
);

COMMIT;

-- Verificación final
SELECT 'consorcios' as tabla, COUNT(*) FROM consorcios
UNION ALL SELECT 'propietarios', COUNT(*) FROM propietarios
UNION ALL SELECT 'unidades_funcionales', COUNT(*) FROM unidades_funcionales
UNION ALL SELECT 'gastos', COUNT(*) FROM gastos;
