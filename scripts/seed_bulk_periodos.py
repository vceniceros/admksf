#!/usr/bin/env python3
"""Seed masivo Consorcio360 STAGING — 36 períodos (ene 2024 → dic 2026).

Carga gastos para los 6 consorcios existentes con inflación mensual ~5%.
NO recrea consorcios, propietarios ni UFs — solo agrega gastos por período.

Uso:
    python3 seed_bulk_periodos.py
"""

import json
from datetime import date
from urllib import error, parse, request

BASE_URL = "http://127.0.0.1:8002"
JSON_HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def generar_periodos():
    periodos = []
    for anio in range(2024, 2027):
        for mes in range(1, 13):
            periodos.append(date(anio, mes, 1))
    return periodos

PERIODOS = generar_periodos()

CONSORCIOS_CUIT = [
    "30800000001",
    "30800000002",
    "30800000003",
    "30800000004",
    "30800000005",
    "30800000006",
]

PROVEEDOR_CUIT = "30698765432"

GASTOS_BASE_2024_01 = [
    {"descripcion": "Seguridad",                "monto_base": 1_800_000.00, "tipo_gasto": "Seguridad"},
    {"descripcion": "Mantenimiento",             "monto_base":   420_000.00, "tipo_gasto": "Mantenimiento"},
    {"descripcion": "Agua",                      "monto_base":   180_000.00, "tipo_gasto": "Servicios"},
    {"descripcion": "Electricidad",              "monto_base":   145_000.00, "tipo_gasto": "Servicios"},
    {"descripcion": "Honorarios administracion", "monto_base":   340_000.00, "tipo_gasto": "Administracion"},
    {"descripcion": "Limpieza",                  "monto_base":   220_000.00, "tipo_gasto": "Mantenimiento"},
    {"descripcion": "Seguro",                    "monto_base":   150_000.00, "tipo_gasto": "Otros"},
]

INFLACION_MENSUAL = 0.05

def monto_para_periodo(monto_base: float, periodo_idx: int) -> str:
    monto = monto_base * ((1 + INFLACION_MENSUAL) ** periodo_idx)
    return f"{monto:.2f}"

def print_ok(msg):     print(f"{GREEN}✅ {msg}{RESET}")
def print_skip(msg):   print(f"{YELLOW}⏭  {msg}{RESET}")
def print_error(msg):  print(f"{RED}❌ {msg}{RESET}")
def print_header(msg): print(f"\n{BOLD}{msg}{RESET}")

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

def get_gastos_existentes(cuit: str) -> set:
    code, data = api_request("GET", f"/api/gastos/consorcio/{cuit}/")
    if code != 200:
        return set()
    existentes = set()
    for g in data.get("data", []):
        periodo = str(g.get("periodo", ""))[:10]
        descripcion = str(g.get("descripcion", ""))
        existentes.add((periodo, descripcion))
    return existentes

def seed_gastos_consorcio(cuit: str, nombre: str):
    print_header(f"Consorcio: {nombre} ({cuit})")
    existentes = get_gastos_existentes(cuit)
    print(f"  Gastos ya existentes: {len(existentes)}")

    creados = 0
    saltados = 0
    errores = 0

    for idx, periodo in enumerate(PERIODOS):
        periodo_str = periodo.strftime("%Y-%m-%d")
        periodo_label = periodo.strftime("%Y-%m")

        for gasto in GASTOS_BASE_2024_01:
            key = (periodo_str, gasto["descripcion"])
            if key in existentes:
                saltados += 1
                continue

            monto = monto_para_periodo(gasto["monto_base"], idx)
            payload = {
                "consorcio":   cuit,
                "proveedor":   PROVEEDOR_CUIT,
                "periodo":     periodo_str,
                "descripcion": gasto["descripcion"],
                "monto":       monto,
                "tipo_gasto":  gasto["tipo_gasto"],
                "estado_pago": "Pagado" if periodo < date(2026, 1, 1) else "Pendiente",
            }
            code, resp = api_request("POST", "/api/gastos/crear/", payload)
            if code == 201:
                creados += 1
                existentes.add(key)
            else:
                errores += 1
                print_error(f"  [{periodo_label}] {gasto['descripcion']} → HTTP {code}: {resp}")

    print_ok(f"  Creados: {creados} | Saltados: {saltados} | Errores: {errores}")
    return creados, errores

def verificar_consorcios():
    print_header("Verificando consorcios en staging...")
    nombres = {}
    for cuit in CONSORCIOS_CUIT:
        code, data = api_request("GET", f"/api/consorcios/{cuit}/")
        if code == 200:
            nombre = data.get("data", {}).get("razon_social") or data.get("razon_social", cuit)
            nombres[cuit] = nombre
            print_ok(f"  {cuit} → {nombre}")
        else:
            print_error(f"  {cuit} → NO ENCONTRADO (HTTP {code})")
            nombres[cuit] = cuit
    return nombres

def main():
    print(f"\n{'='*65}")
    print(f"  SEED MASIVO STAGING — 36 períodos (ene 2024 → dic 2026)")
    print(f"  Inflación mensual aplicada: {INFLACION_MENSUAL*100:.0f}%")
    print(f"  Gastos por consorcio por período: {len(GASTOS_BASE_2024_01)}")
    print(f"  Total gastos a crear (máx): {len(CONSORCIOS_CUIT) * len(PERIODOS) * len(GASTOS_BASE_2024_01)}")
    print(f"{'='*65}\n")

    nombres = verificar_consorcios()

    total_creados = 0
    total_errores = 0

    for cuit in CONSORCIOS_CUIT:
        creados, errores = seed_gastos_consorcio(cuit, nombres[cuit])
        total_creados += creados
        total_errores += errores

    print(f"\n{'='*65}")
    if total_errores == 0:
        print_ok(f"Seed completado. Total creados: {total_creados}")
    else:
        print(f"{YELLOW}⚠️  Seed completado con errores.{RESET}")
        print(f"   Creados: {total_creados} | Errores: {total_errores}")
    print(f"{'='*65}\n")

if __name__ == "__main__":
    main()
