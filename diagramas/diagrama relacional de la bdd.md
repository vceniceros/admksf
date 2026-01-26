# diagrama relacional de la bdd

- consorcio(<u>**cuit**</u>, nombre_consorcio, calle, ciudad, numero, codigo_postal, interes_por_mora, redondeo)

- -  PK: cuit

- unidad_funcional(<u>**numero de unidad funcional**</u>,<u>**cuit_consorcio**</u>,nombre_unidad, tipo,superficie, prorrateo, <u>_dni_propietario_</u>, estado)

- - PK: numero de unidad funcional, cuit_consorcio
- - FK: cuit_consorcio references consorcio(cuit), dni_propietario references propietario(dni)


- propietario(<u>**dni**</u>, nombre, apellido, telefono, email, deuda)

- - PK: dni

- gasto(<u>**id_gasto**</u>,<u>**cuit_consorcio**</u>, <u>_cuit_proveedor_</u>,periodo, nro_calle, calle,ciudad, codigo_postal,descripcion, monto, fecha, tipo_gasto)

- - PK: id_gasto, cuit_consorcio
- - FK: cuit_consorcio references consorcio(cuit), cuit_proveedor references proveedor(cuit)


- proveedor(<u>**cuit**</u>, razon_social, telefono, email, direccion)

- - PK: cuit

- pago(<u>**id_pago**</u>,<u>**numero de unidad funcional**</u>,<u>**cuit_consorcio**</u>, <u>_dni_propietario_</u>, monto, fecha_pago)

- - PK: id_pago, numero de unidad funcional, cit_consorcio
- - FK: numero de unidad funcional references unidad_funcional(numero de unidad funcional), cuit_consorcio references consorcio(cuit), dni_propietario references propietario(dni)

- saldo_unidad(<u>**numero de unidad funcional**</u>, <u>**dni**</u>,saldo_anterior, fecha_de_vencimiento_anterior, pagos_realizados, saldo_actual, fecha_actualizacion, <u>_cuit_consorcio_</u>)

- - PK: numero de unidad funcional, dni, cuit_consorcio
- - FK: numero de unidad funcional references unidad_funcional(numero de unidad funcional), dni references propietario(dni), cuit_consorcio references consorcio(cuit)

