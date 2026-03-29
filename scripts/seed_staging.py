#!/usr/bin/env python3
"""Seed para Consorcio360 STAGING — 6 consorcios, 10 propietarios cada uno.

Uso:
    python seed_staging.py
"""

import json
from urllib import error, parse, request

BASE_URL = "http://localhost:8002"
JSON_HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

PERIODO_FECHA = "2026-01-01"
PERIODO_LIQUIDAR = "2026-01"

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

CONSORCIOS = [
    {"cuit": "30800000001", "razon_social": "Edificio Torres del Sol",    "calle": "Av. Corrientes", "numero": 1234, "codigo_postal": "1043", "ciudad": "Buenos Aires", "interes_por_mora": "5.00", "redondeo_aumento": "0.50", "tipo": "edificio"},
    {"cuit": "30800000002", "razon_social": "Consorcio Palermo Verde",    "calle": "Thames",         "numero": 567,  "codigo_postal": "1414", "ciudad": "Buenos Aires", "interes_por_mora": "5.00", "redondeo_aumento": "0.50", "tipo": "edificio"},
    {"cuit": "30800000003", "razon_social": "Barrio San Martin",          "calle": "Av. San Martin", "numero": 3200, "codigo_postal": "1650", "ciudad": "San Martin",   "interes_por_mora": "5.00", "redondeo_aumento": "0.50", "tipo": "barrio"},
    {"cuit": "30800000004", "razon_social": "Complejo Tigre Norte",       "calle": "Av. Cazadores",  "numero": 890,  "codigo_postal": "1648", "ciudad": "Tigre",        "interes_por_mora": "5.00", "redondeo_aumento": "0.50", "tipo": "barrio"},
    {"cuit": "30800000005", "razon_social": "Edificio Recoleta Premium",  "calle": "Av. Santa Fe",   "numero": 2100, "codigo_postal": "1123", "ciudad": "Buenos Aires", "interes_por_mora": "5.00", "redondeo_aumento": "0.50", "tipo": "edificio"},
    {"cuit": "30800000006", "razon_social": "Barrio Los Alamos",          "calle": "Ruta 8",         "numero": 4500, "codigo_postal": "1667", "ciudad": "Del Viso",     "interes_por_mora": "5.00", "redondeo_aumento": "0.50", "tipo": "barrio"},
]

NOMBRES = [
    ("Ana",      "Garcia",    "1"),
    ("Bruno",    "Lopez",     "2"),
    ("Carolina", "Martinez",  "3"),
    ("Diego",    "Rodriguez", "4"),
    ("Elena",    "Fernandez", "5"),
    ("Federico", "Gonzalez",  "6"),
    ("Gabriela", "Perez",     "7"),
    ("Hernan",   "Sanchez",   "8"),
    ("Irene",    "Torres",    "9"),
    ("Javier",   "Ramirez",   "0"),
]

def build_propietarios(consorcio_idx):
    props = []
    base_dni = 10000000 + consorcio_idx * 10000
    for i, (nombre, apellido, _) in enumerate(NOMBRES):
        dni = str(base_dni + i)
        slug = f"{nombre.lower()}.{apellido.lower()}{consorcio_idx}"
        props.append({"dni": dni, "nombre": nombre, "apellido": apellido, "email": f"{slug}@fakemail.com"})
    return props

def build_unidades(consorcio, propietarios):
    coefs = ["0.6000","0.6000","0.7000","0.7000","0.8000","0.8000","0.9000","0.9000","1.0000","1.0000"]
    sups  = ["45.00","45.00","55.00","55.00","65.00","65.00","75.00","75.00","90.00","90.00"]
    tipo_uf = "Lote" if consorcio["tipo"] == "barrio" else "Departamento"
    return [{"numero_de_unidad_funcional": i+1, "superficie": sups[i], "coeficiente": coefs[i], "propietario": p["dni"], "tipo_uf": tipo_uf} for i, p in enumerate(propietarios)]

GASTOS_BASE = [
    {"descripcion": "Seguridad",                "monto": "3500000.00", "tipo_gasto": "Seguridad"},
    {"descripcion": "Mantenimiento",             "monto": "800000.00",  "tipo_gasto": "Mantenimiento"},
    {"descripcion": "Agua",                      "monto": "350000.00",  "tipo_gasto": "Servicios"},
    {"descripcion": "Electricidad",              "monto": "280000.00",  "tipo_gasto": "Servicios"},
    {"descripcion": "Honorarios administracion", "monto": "650000.00",  "tipo_gasto": "Administracion"},
    {"descripcion": "Limpieza",                  "monto": "420000.00",  "tipo_gasto": "Mantenimiento"},
    {"descripcion": "Seguro",                    "monto": "290000.00",  "tipo_gasto": "Otros"},
]

def print_ok(msg):    print(f"{GREEN}✅ {msg}{RESET}")
def print_skip(msg):  print(f"{YELLOW}⏭ {msg}{RESET}")
def print_error(msg): print(f"{RED}❌ {msg}{RESET}")

def api_request(method, path, payload=None, params=None):
    query = "?" + parse.urlencode(params) if params else ""
    url = f"{BASE_URL}{path}{query}"
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = dict(JSON_HEADERS)
    req = request.Request(url, data=body, headers=headers, method=method.upper())
    try:
        with request.urlopen(req, timeout=15) as resp:
            raw = resp.read().decode("utf-8").strip()
            return resp.getcode(), json.loads(raw) if raw else {}
    except error.HTTPError as exc:
        raw = exc.read().decode("utf-8").strip()
        try:    parsed = json.loads(raw) if raw else {}
        except: parsed = {"raw": raw}
        return exc.code, parsed
    except error.URLError as exc:
        return 0, {"message": f"Error de conexion: {exc.reason}"}
    except Exception as exc:
        return 0, {"message": str(exc)}

def ensure_proveedor():
    code, _ = api_request("GET", f"/api/proveedores/{PROVEEDOR['cuit']}/")
    if code == 200: print_skip(f"Proveedor ya existe."); return True
    code, data = api_request("POST", "/api/proveedores/crear/", PROVEEDOR)
    if code == 201: print_ok(f"Proveedor creado."); return True
    print_error(f"No se pudo crear proveedor. HTTP {code}. {data}"); return False

def ensure_consorcio(c):
    code, _ = api_request("GET", f"/api/consorcios/{c['cuit']}/")
    if code == 200: print_skip(f"Consorcio {c['razon_social']} ya existe."); return True
    payload = {k: v for k, v in c.items() if k != "tipo"}
    code, data = api_request("POST", "/api/consorcios/crear/", payload)
    if code == 201: print_ok(f"Consorcio creado: {c['razon_social']}."); return True
    print_error(f"No se pudo crear consorcio {c['cuit']}. HTTP {code}. {data}"); return False

def ensure_propietarios(propietarios):
    for p in propietarios:
        code, _ = api_request("GET", f"/api/propietarios/{p['dni']}/")
        if code == 200: print_skip(f"Propietario {p['dni']} ya existe."); continue
        code, data = api_request("POST", "/api/propietarios/crear/", p)
        if code == 201: print_ok(f"Propietario: {p['nombre']} {p['apellido']}.")
        else: print_error(f"No se pudo crear propietario {p['dni']}. HTTP {code}. {data}")

def ensure_unidades(consorcio, unidades):
    cuit = consorcio["cuit"]
    code, data = api_request("GET", f"/api/unidades-funcionales/consorcio/{cuit}/")
    existentes = {int(i["numero"]) for i in data.get("data", []) if i.get("numero")} if code == 200 else set()
    for u in unidades:
        n = u["numero_de_unidad_funcional"]
        if n in existentes: print_skip(f"UF {n} ya existe."); continue
        payload = {"numero_de_unidad_funcional": n, "consorcio": cuit, "tipo_de_unidad": u["tipo_uf"], "estado_de_vivienda": "Propietario", "superficie": u["superficie"], "coeficiente": u["coeficiente"], "propietario": u["propietario"]}
        code, resp = api_request("POST", "/api/unidades-funcionales/crear/", payload)
        if code == 201: print_ok(f"UF {n} creada."); existentes.add(n)
        else: print_error(f"No se pudo crear UF {n}. HTTP {code}. {resp}")

def ensure_gastos(consorcio):
    cuit = consorcio["cuit"]
    code, data = api_request("GET", f"/api/gastos/consorcio/{cuit}/")
    existentes = data.get("data", []) if code == 200 else []
    for g in GASTOS_BASE:
        if any(str(e.get("periodo")) == PERIODO_FECHA and str(e.get("descripcion")) == g["descripcion"] for e in existentes):
            print_skip(f"Gasto '{g['descripcion']}' ya existe."); continue
        payload = {"consorcio": cuit, "proveedor": PROVEEDOR["cuit"], "periodo": PERIODO_FECHA, "descripcion": g["descripcion"], "monto": g["monto"], "tipo_gasto": g["tipo_gasto"], "estado_pago": "Pendiente"}
        code, resp = api_request("POST", "/api/gastos/crear/", payload)
        if code == 201: print_ok(f"Gasto creado: {g['descripcion']}.")
        else: print_error(f"No se pudo crear gasto. HTTP {code}. {resp}")

def ensure_template(consorcio):
    cuit = consorcio["cuit"]
    nombre = f"Template {consorcio['razon_social']} v1"
    code, data = api_request("GET", f"/api/expensas/templates/consorcio/{cuit}/")
    if code == 200:
        for item in data.get("data", []):
            if str(item.get("nombre")) == nombre: print_skip(f"Template ya existe."); return item.get("id")
    payload = {"consorcio": cuit, "nombre": nombre, "version": 1, "activo": True, "config": {"rounding": {"metodo": "none"}, "columns": [{"id": "saldo_anterior", "label": "Saldo Anterior", "calc_type": "saldo_anterior", "visible": True}, {"id": "expensa_ordinaria", "label": "Expensa Ordinaria", "calc_type": "prorrateo", "coeficiente": "custom", "visible": True}, {"id": "interes_mora", "label": "Interes Mora", "calc_type": "interes", "metodo": "simple", "base": "saldo_anterior", "tasa": "5", "visible": True}, {"id": "total", "label": "Total", "calc_type": "formula", "expr": "saldo_anterior + expensa_ordinaria + interes_mora", "visible": True}]}}
    code, resp = api_request("POST", "/api/expensas/templates/crear/", payload)
    if code == 201: tid = resp.get("data", {}).get("id"); print_ok(f"Template creado (id={tid})."); return tid
    print_error(f"No se pudo crear template. HTTP {code}. {resp}"); return None

def main():
    print(f"Seed STAGING Consorcio360 → {BASE_URL}")
    print("=" * 60)
    if not ensure_proveedor():
        print_error("Abortando: sin proveedor."); return
    for idx, consorcio in enumerate(CONSORCIOS):
        print(f"\n{'─'*60}\nConsorcio {idx+1}/6: {consorcio['razon_social']}\n{'─'*60}")
        if not ensure_consorcio(consorcio): continue
        propietarios = build_propietarios(idx + 1)
        unidades = build_unidades(consorcio, propietarios)
        ensure_propietarios(propietarios)
        ensure_unidades(consorcio, unidades)
        ensure_gastos(consorcio)
        ensure_template(consorcio)
    print(f"\n{'='*60}")
    print_ok("Seed staging finalizado.")

if __name__ == "__main__":
    main()
