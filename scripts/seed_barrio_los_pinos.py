#!/usr/bin/env python3
"""Seed idempotente para Consorcio360 via API REST (urllib + json).

Uso:
    python scripts/seed_barrio_los_pinos.py
"""

import json
from urllib import error, parse, request


BASE_URL = "http://localhost:8001"
JSON_HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

# Endpoints validados contra los urls.py del backend.
API_PATHS = {
    "consorcios": {
        "crear": "/api/consorcios/crear/",
        "detalle": "/api/consorcios/{cuit}/",
    },
    "propietarios": {
        "crear": "/api/propietarios/crear/",
        "detalle": "/api/propietarios/{dni}/",
    },
    "proveedores": {
        "crear": "/api/proveedores/crear/",
        "detalle": "/api/proveedores/{cuit}/",
    },
    "unidades": {
        "crear": "/api/unidades-funcionales/crear/",
        "detalle": "/api/unidades-funcionales/{numero}/",
        "listar_por_consorcio": "/api/unidades-funcionales/consorcio/{cuit_consorcio}/",
    },
    "gastos": {
        "crear": "/api/gastos/crear/",
        "detalle": "/api/gastos/{id_gasto}/",
        "listar_por_consorcio": "/api/gastos/consorcio/{cuit_consorcio}/",
    },
}

# Colores para consola
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"


CONSORCIO = {
    "cuit": "30712345678",
    "razon_social": "Barrio Los Pinos",
    "calle": "Av. Los Robles",
    "numero": 2500,
    "codigo_postal": "1667",
    "ciudad": "Don Torcuato",
    "interes_por_mora": "5.00",
    "redondeo_aumento": "0.50",
}

PROVEEDOR = {
    "cuit": "30698765432",
    "razon_social": "Servicios Generales del Norte SRL",
    "telefono": "1122334455",
    "email": "contacto@fakemail.com",
    "calle": "Av. Constituyentes",
    "numero": 4500,
    "codigo_postal": "1667",
    "ciudad": "Don Torcuato",
    "tipo_proveedor": "servicios_mensuales",
}

PROPIETARIOS = [
    {"dni": "11223344", "nombre": "Martina", "apellido": "Soria", "email": "martina.soria@fakemail.com"},
    {"dni": "22334455", "nombre": "Rodrigo", "apellido": "Vidal", "email": "rodrigo.vidal@fakemail.com"},
    {"dni": "33445566", "nombre": "Valentina", "apellido": "Ortega", "email": "valentina.ortega@fakemail.com"},
    {"dni": "44556677", "nombre": "Lucas", "apellido": "Ferreyra", "email": "lucas.ferreyra@fakemail.com"},
    {"dni": "55667788", "nombre": "Camila", "apellido": "Mendoza", "email": "camila.mendoza@fakemail.com"},
    {"dni": "66778899", "nombre": "Nicolas", "apellido": "Aguirre", "email": "nicolas.aguirre@fakemail.com"},
    {"dni": "77889900", "nombre": "Sofia", "apellido": "Paredes", "email": "sofia.paredes@fakemail.com"},
    {"dni": "88990011", "nombre": "Matias", "apellido": "Ibanez", "email": "matias.ibanez@fakemail.com"},
]

LOTES = [
    {"numero_de_unidad_funcional": 1, "superficie": "300.00", "coeficiente": "0.6000", "propietario": "11223344"},
    {"numero_de_unidad_funcional": 2, "superficie": "300.00", "coeficiente": "0.6000", "propietario": "22334455"},
    {"numero_de_unidad_funcional": 3, "superficie": "350.00", "coeficiente": "0.7000", "propietario": "33445566"},
    {"numero_de_unidad_funcional": 4, "superficie": "350.00", "coeficiente": "0.7000", "propietario": "44556677"},
    {"numero_de_unidad_funcional": 5, "superficie": "400.00", "coeficiente": "0.8000", "propietario": "55667788"},
    {"numero_de_unidad_funcional": 6, "superficie": "400.00", "coeficiente": "0.8000", "propietario": "66778899"},
    {"numero_de_unidad_funcional": 7, "superficie": "300.00", "coeficiente": "0.6000", "propietario": "77889900"},
    {"numero_de_unidad_funcional": 8, "superficie": "300.00", "coeficiente": "0.6000", "propietario": "88990011"},
]

GASTOS = [
    {"descripcion": "Seguridad Privada", "monto": "4250000.00", "tipo_gasto": "Seguridad"},
    {"descripcion": "Mantenimiento espacios verdes", "monto": "950000.00", "tipo_gasto": "Mantenimiento"},
    {"descripcion": "Agua AYSA", "monto": "380000.00", "tipo_gasto": "Servicios"},
    {"descripcion": "Energia electrica", "monto": "290000.00", "tipo_gasto": "Servicios"},
    {"descripcion": "Honorarios administracion", "monto": "750000.00", "tipo_gasto": "Administracion"},
    {"descripcion": "Recoleccion residuos", "monto": "480000.00", "tipo_gasto": "Mantenimiento"},
    # "Gastos Bancarios" no existe como enum en el backend, se usa "Otros".
    {"descripcion": "Gastos bancarios", "monto": "95000.00", "tipo_gasto": "Otros"},
    {"descripcion": "Seguro integral cuota 1/6", "monto": "305000.00", "tipo_gasto": "Otros"},
]

TEMPLATE_NOMBRE = "Template Barrio Los Pinos v1"
TEMPLATE_VERSION = 1
PERIODO_FECHA = "2026-01-01"
PERIODO_LIQUIDAR = "2026-01"


def print_ok(msg):
    print(f"{GREEN}✅ {msg}{RESET}")


def print_skip(msg):
    print(f"{YELLOW}⏭ {msg}{RESET}")


def print_error(msg):
    print(f"{RED}❌ {msg}{RESET}")


def api_request(method, path, payload=None, params=None):
    query = ""
    if params:
        query = "?" + parse.urlencode(params)
    url = f"{BASE_URL}{path}{query}"
    body = None
    headers = dict(JSON_HEADERS)
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=body, headers=headers, method=method.upper())
    try:
        with request.urlopen(req, timeout=15) as resp:
            raw = resp.read().decode("utf-8").strip()
            data = json.loads(raw) if raw else {}
            return resp.getcode(), data
    except error.HTTPError as exc:
        raw = exc.read().decode("utf-8").strip()
        parsed = {}
        if raw:
            try:
                parsed = json.loads(raw)
            except json.JSONDecodeError:
                parsed = {"raw": raw}
        return exc.code, parsed
    except error.URLError as exc:
        return 0, {"status": "error", "message": f"Error de conexion: {exc.reason}"}
    except Exception as exc:  # noqa: BLE001
        return 0, {"status": "error", "message": str(exc)}


def ensure_consorcio():
    cuit = CONSORCIO["cuit"]
    code, _ = api_request("GET", API_PATHS["consorcios"]["detalle"].format(cuit=cuit))
    if code == 200:
        print_skip(f"Consorcio {cuit} ya existe.")
        return True
    code, data = api_request("POST", API_PATHS["consorcios"]["crear"], CONSORCIO)
    if code == 201:
        print_ok(f"Consorcio creado: {CONSORCIO['razon_social']} ({cuit}).")
        return True
    print_error(f"No se pudo crear consorcio {cuit}. HTTP {code}. {data}")
    return False


def ensure_proveedor():
    cuit = PROVEEDOR["cuit"]
    code, _ = api_request("GET", API_PATHS["proveedores"]["detalle"].format(cuit=cuit))
    if code == 200:
        print_skip(f"Proveedor {cuit} ya existe.")
        return True
    code, data = api_request("POST", API_PATHS["proveedores"]["crear"], PROVEEDOR)
    if code == 201:
        print_ok(f"Proveedor creado: {PROVEEDOR['razon_social']} ({cuit}).")
        return True
    print_error(f"No se pudo crear proveedor {cuit}. HTTP {code}. {data}")
    return False


def ensure_propietarios():
    ok = True
    for p in PROPIETARIOS:
        dni = p["dni"]
        code, _ = api_request("GET", API_PATHS["propietarios"]["detalle"].format(dni=dni))
        if code == 200:
            print_skip(f"Propietario {dni} ya existe.")
            continue
        code, data = api_request("POST", API_PATHS["propietarios"]["crear"], p)
        if code == 201:
            print_ok(f"Propietario creado: {p['nombre']} {p['apellido']} ({dni}).")
        else:
            ok = False
            print_error(f"No se pudo crear propietario {dni}. HTTP {code}. {data}")
    return ok


def ensure_unidades():
    ok = True
    code, data = api_request(
        "GET",
        API_PATHS["unidades"]["listar_por_consorcio"].format(cuit_consorcio=CONSORCIO["cuit"]),
    )
    if code != 200:
        print_error(
            f"No se pudieron listar unidades del consorcio {CONSORCIO['cuit']}. "
            f"HTTP {code}. {data}"
        )
        return False

    unidades_consorcio = data.get("data", [])
    numeros_existentes_consorcio = {
        int(item.get("numero"))
        for item in unidades_consorcio
        if item.get("numero") is not None
    }

    for lote in LOTES:
        numero = lote["numero_de_unidad_funcional"]

        if numero in numeros_existentes_consorcio:
            print_skip(f"Lote {numero} ya existe en el consorcio objetivo.")
            continue

        payload = {
            "numero_de_unidad_funcional": numero,
            "consorcio": CONSORCIO["cuit"],
            "tipo_de_unidad": "Lote",
            "estado_de_vivienda": "Propietario",
            "superficie": lote["superficie"],
            "coeficiente": lote["coeficiente"],
            "propietario": lote["propietario"],
        }
        code, data = api_request("POST", API_PATHS["unidades"]["crear"], payload)
        if code == 201:
            print_ok(f"Lote {numero} creado (coef {lote['coeficiente']}).")
            numeros_existentes_consorcio.add(numero)
        else:
            # obtener_unidad_funcional(numero) no filtra por consorcio; si existe en otro
            # consorcio, el POST suele fallar por colision de PK.
            detail_code, detail_data = api_request(
                "GET", API_PATHS["unidades"]["detalle"].format(numero=numero)
            )
            if detail_code == 200:
                actual = detail_data.get("data", {})
                consorcio_actual = str(actual.get("consorcio", ""))
                if consorcio_actual != CONSORCIO["cuit"]:
                    ok = False
                    print_error(
                        f"Lote {numero} ya existe en otro consorcio ({consorcio_actual}). "
                        "No se puede crear en este consorcio con el mismo numero."
                    )
                    continue
            ok = False
            print_error(f"No se pudo crear lote {numero}. HTTP {code}. {data}")
    return ok


def ensure_gastos():
    ok = True
    code, data = api_request(
        "GET",
        API_PATHS["gastos"]["listar_por_consorcio"].format(cuit_consorcio=CONSORCIO["cuit"]),
    )
    existentes = []
    if code == 200:
        existentes = data.get("data", [])
    elif code != 500:
        print_error(f"No se pudieron listar gastos del consorcio. HTTP {code}. {data}")

    for g in GASTOS:
        match = False
        for e in existentes:
            id_gasto = e.get("id")
            if id_gasto:
                api_request("GET", API_PATHS["gastos"]["detalle"].format(id_gasto=id_gasto))
            if (
                str(e.get("periodo")) == PERIODO_FECHA
                and str(e.get("descripcion")) == g["descripcion"]
                and str(e.get("monto")) == g["monto"]
                and str(e.get("tipo_gasto")) == g["tipo_gasto"]
            ):
                match = True
                break
        if match:
            print_skip(f"Gasto ya existe: {g['descripcion']}.")
            continue

        payload = {
            "consorcio": CONSORCIO["cuit"],
            "proveedor": PROVEEDOR["cuit"],
            "periodo": PERIODO_FECHA,
            "descripcion": g["descripcion"],
            "monto": g["monto"],
            "tipo_gasto": g["tipo_gasto"],
            "estado_pago": "Pendiente",
        }
        code, resp = api_request("POST", API_PATHS["gastos"]["crear"], payload)
        if code == 201:
            print_ok(f"Gasto creado: {g['descripcion']} (${g['monto']}).")
        else:
            ok = False
            print_error(f"No se pudo crear gasto '{g['descripcion']}'. HTTP {code}. {resp}")
    return ok


def ensure_template():
    code, data = api_request(
        "GET",
        "/api/expensas/templates/",
        params={"consorcio": CONSORCIO["cuit"]},
    )
    if code != 200:
        print_error(f"No se pudieron listar templates. HTTP {code}. {data}")
        return None

    for item in data.get("data", []):
        if (
            str(item.get("nombre")) == TEMPLATE_NOMBRE
            and int(item.get("version", 0)) == TEMPLATE_VERSION
        ):
            print_skip(f"Template ya existe (id={item.get('id')}).")
            return item.get("id")

    template_payload = {
        "consorcio": CONSORCIO["cuit"],
        "nombre": TEMPLATE_NOMBRE,
        "version": TEMPLATE_VERSION,
        "activo": True,
        "config": {
            "rounding": {"metodo": "none"},
            "columns": [
                {
                    "id": "saldo_anterior",
                    "label": "Saldo Anterior",
                    "calc_type": "saldo_anterior",
                    "visible": True,
                },
                {
                    "id": "expensa_ordinaria",
                    "label": "Expensa Ordinaria",
                    "calc_type": "prorrateo",
                    "coeficiente": "custom",
                    "visible": True,
                },
                {
                    "id": "interes_mora",
                    "label": "Interes Mora",
                    "calc_type": "interes",
                    "metodo": "simple",
                    "base": "saldo_anterior",
                    "tasa": "5",
                    "visible": True,
                },
                {
                    "id": "total",
                    "label": "Total",
                    "calc_type": "formula",
                    "expr": "saldo_anterior + expensa_ordinaria + interes_mora",
                    "visible": True,
                },
            ]
        },
    }
    code, resp = api_request("POST", "/api/expensas/templates/crear/", template_payload)
    if code == 201:
        template_id = resp.get("data", {}).get("id")
        print_ok(f"Template creado (id={template_id}).")
        return template_id
    print_error(f"No se pudo crear template. HTTP {code}. {resp}")
    return None


def run_liquidacion(template_id):
    coeficientes_custom = {}
    for lote in LOTES:
        coeficientes_custom[str(lote["numero_de_unidad_funcional"])] = lote["coeficiente"]

    payload = {
        "template_id": template_id,
        "consorcio": CONSORCIO["cuit"],
        "periodo": PERIODO_LIQUIDAR,
        "cerrar": False,
        "parametros": {
            "coeficientes_custom": coeficientes_custom,
        },
    }

    code, data = api_request("POST", "/api/liquidar/", payload)
    if code not in (200, 201):
        print_error(f"No se pudo liquidar. HTTP {code}. {data}")
        return False

    resultado = data.get("data", {})
    unidades = resultado.get("unidades", [])
    if not unidades:
        print_error("Liquidacion sin unidades en la respuesta.")
        return False

    print_ok("Liquidacion de prueba ejecutada.")
    print("")
    print("Tabla de liquidacion por lote")
    print("-" * 94)
    print(
        f"{'Lote':<6} {'Propietario':<26} {'Saldo Ant.':>12} "
        f"{'Exp. Ord.':>12} {'Interes':>12} {'Total':>12}"
    )
    print("-" * 94)

    for uf in sorted(unidades, key=lambda x: int(x.get("numero_unidad_funcional", 0))):
        valores = uf.get("valores", {})
        titular = f"{uf.get('propietario', '')} {uf.get('apellido', '')}".strip()
        print(
            f"{str(uf.get('numero_unidad_funcional', '')):<6} "
            f"{titular[:26]:<26} "
            f"{str(valores.get('saldo_anterior', '0.00')):>12} "
            f"{str(valores.get('expensa_ordinaria', '0.00')):>12} "
            f"{str(valores.get('interes_mora', '0.00')):>12} "
            f"{str(valores.get('total', '0.00')):>12}"
        )
    print("-" * 94)
    return True


def main():
    print("Seed Barrio Los Pinos -> API Consorcio360")
    print(f"Base URL: {BASE_URL}")
    print("")

    ok = True
    if not ensure_consorcio():
        ok = False
    if not ensure_proveedor():
        ok = False
    if not ensure_propietarios():
        ok = False
    if not ensure_unidades():
        ok = False
    if not ensure_gastos():
        ok = False

    template_id = ensure_template()
    if not template_id:
        ok = False
    else:
        if not run_liquidacion(template_id):
            ok = False

    print("")
    if ok:
        print_ok("Seed finalizado sin errores.")
    else:
        print_error("Seed finalizado con errores. Revisar mensajes anteriores.")


if __name__ == "__main__":
    main()
