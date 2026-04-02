# Integración Resend SMTP — Archivo de Continuidad
**Fecha:** 01 Abril 2026
**Estado:** 🟡 EN PROGRESO — pendiente completar

---

## Decisiones tomadas

| Flujo | Responsable | Proveedor | Estado |
|-------|-------------|-----------|--------|
| Reset de contraseña | Django directo | Resend SMTP | 🟡 Falta settings.py |
| Envío masivo liquidaciones PDF | n8n workflow | Resend API | 🔴 Pendiente (cuando n8n activo) |

**Una sola cuenta Resend, dos consumidores distintos.**
- Django usa credenciales SMTP
- n8n usa API key (nodo nativo Resend en n8n 2.4.8)

---

## Estado de infraestructura al cierre

### ✅ Hecho
- Cuenta Resend creada
- API key generada (key anterior expuesta en chat → **regenerada**)
- Variable `RESEND_API_KEY` cargada en Coolify (staging) ✅
- Redeploy staging realizado → variable confirmada dentro del contenedor ✅
- Conectividad puerto 587 desde contenedor staging verificada ✅ (`smtp.resend.com:587` OK)

### ❌ Pendiente
- `settings.py` — bloque EMAIL_* incompleto (solo tiene `EMAIL_BACKEND`, resto en defaults de Django)
- `docker-compose.yml` — falta agregar `RESEND_API_KEY` en environment de `app-consorcio` (producción)
- `.env` servidor producción — falta agregar `RESEND_API_KEY`
- Test de `send_mail()` en staging — no ejecutado (bloqueado por settings.py incompleto)
- Credencial Resend en panel n8n — pendiente

---

## Cambio pendiente en settings.py

Buscar la línea existente:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
```

Reemplazar el bloque completo por:
```python
# Email — Resend SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.resend.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'resend'
EMAIL_HOST_PASSWORD = env('RESEND_API_KEY')
DEFAULT_FROM_EMAIL = 'noreply@consorcio360.com'
```

---

## Cambio pendiente en docker-compose.yml

Bajo `environment` del servicio `app-consorcio` agregar:
```yaml
- RESEND_API_KEY=${RESEND_API_KEY}
```

---

## Cambio pendiente en .env (producción)

```bash
ssh prod@10.0.0.1
echo "RESEND_API_KEY=<key>" >> ~/n8n-infra/.env
```

---

## Flujo de retoma — checklist en orden

```
□ 1. Valentino agrega bloque EMAIL_* a settings.py en la rama activa
□ 2. Agregar RESEND_API_KEY a docker-compose.yml (environment app-consorcio)
□ 3. git push → rama 9-integracion-produccion-zonejs-expensas
□ 4. Coolify redeploy staging
□ 5. Test send_mail() desde shell del contenedor staging:

      docker exec -it $(docker ps --format '{{.Names}}' | grep dv3aiejieve8cg2lcdlk4265) python manage.py shell
      >>> from django.core.mail import send_mail
      >>> send_mail('Test Resend staging', 'Funciona.', 'noreply@consorcio360.com', ['tu@mail.com'])

□ 6. Verificar en dashboard Resend: resend.com/emails
□ 7. Si OK → agregar RESEND_API_KEY al .env de producción
□ 8. Deploy producción completo (rebuild con volúmenes)
□ 9. Configurar credencial Resend en panel n8n (http://localhost:5679 via SSH tunnel)
□ 10. Documentar en RUNBOOK procedimiento de reset manual como fallback:
       docker exec -it n8n-infra-app-1 python manage.py changepassword <usuario>
```

---

## Consideraciones plan gratuito Resend

| Límite | Valor | Impacto |
|--------|-------|---------|
| Mails/día | 100 | ⚠️ Controlar en demos con pruebas masivas |
| Mails/mes | 3.000 | ✅ Karina: ~318/mes (6 consorcios, 318 UFs total) |

**Distribución de liquidaciones vía n8n:** diseñar workflow con nodo de espera para respetar límite diario de 100. No requiere plan pago — requiere lotes por consorcio en días distintos.

---

## Futuro — migración a dominio DonWeb

Cuando migren de DuckDNS al dominio DonWeb, agregar 3 registros DNS en el panel de DonWeb:

```
SPF   → TXT  @                   "v=spf1 include:amazonses.com ~all"
DKIM  → TXT  resend._domainkey   <clave que provee Resend al verificar dominio>
DMARC → TXT  _dmarc              "v=DMARC1; p=none"
```

Luego cambiar en settings.py:
```python
DEFAULT_FROM_EMAIL = 'noreply@<dominio-donweb>'
```

Un solo cambio de variable, resto del stack intacto.

---

## Fallback operacional (documentar en RUNBOOK)

Si Resend falla y un usuario no puede recuperar contraseña:
```bash
docker exec -it n8n-infra-app-1 python manage.py changepassword <username>
```
