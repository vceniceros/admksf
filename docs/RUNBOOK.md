# RUNBOOK — Consorcio360

Procedimientos operativos para deploy, backups, staging y troubleshooting.
Cualquier miembro del equipo puede seguir estos pasos sin contexto previo.

---

## 1. Deploy a Producción

### 1a. Deploy completo (cambios de frontend/Angular)

Usar cuando se modificaron archivos en `frontend/`.

```bash
ssh prod@10.0.0.1
cd ~/n8n-infra/app-consorcio && git pull
cd ~/n8n-infra
docker compose down
docker volume rm n8n-infra_static_volume n8n-infra_static_angular_volume n8n-infra_templates_volume
docker compose build app-consorcio
docker compose up -d
```

Verificar:
```bash
docker ps --filter "name=app" --format "table {{.Names}}\t{{.Status}}"
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8001
```
Esperar HTTP 200.

### 1b. Deploy rápido (solo cambios de backend Python)

Usar cuando solo se modificaron archivos en `backend/` sin cambios de frontend.

```bash
ssh prod@10.0.0.1
cd ~/n8n-infra/app-consorcio && git pull
cd ~/n8n-infra && docker compose up -d --build app-consorcio
```

### 1c. Deploy a Staging (Coolify)

1. Pushear cambios a GitHub desde local
2. Abrir http://10.0.0.1:8082 (VPN activa)
3. Ir a la app → click **Redeploy**
4. Seguir logs en tiempo real → esperar "New container started"
5. Verificar: `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8002`

---

## 2. Backups PostgreSQL

### Ejecutar backup manual
```bash
ssh prod@10.0.0.1
~/backup-postgres.sh
```

### Verificar backups en R2
```bash
rclone ls r2:consorcio360-backups/Backup/
```

### Ver log de backups
```bash
tail -30 ~/backup-postgres.log
```

### Verificar cron activo
```bash
crontab -l
# Debe mostrar: 0 6,13,21 * * * /home/prod/backup-postgres.sh
```

### Restaurar backup (emergencia)
```bash
# 1. Descargar backup desde R2
rclone copy r2:consorcio360-backups/Backup/backup_n8n_data_YYYYMMDD_HHMMSS.sql.gz ./

# 2. Descomprimir
gunzip backup_n8n_data_YYYYMMDD_HHMMSS.sql.gz

# 3. Restaurar
docker exec -i n8n-infra-postgres-1 psql -U n8n_consorcios360 -d n8n_data < backup_n8n_data_YYYYMMDD_HHMMSS.sql
```

---

## 3. Staging — Seed de datos

Ejecutar después de un deploy limpio de staging.

```bash
ssh prod@10.0.0.1
python3 ~/n8n-infra/app-consorcio/scripts/seed_staging.py
```

Crea: 6 consorcios, 10 propietarios c/u, gastos enero 2026, templates de liquidación.

---

## 4. Base de datos

### Acceder a PostgreSQL
```bash
docker exec -it n8n-infra-postgres-1 psql -U n8n_consorcios360 -d n8n_data
```

### Migraciones Django (producción)
```bash
docker exec n8n-infra-app-1 python manage.py migrate --noinput
```

### Migraciones Django (staging — desde Coolify terminal)
```bash
# Abrir terminal del contenedor staging en Coolify panel → Terminal
python manage.py migrate --noinput
```

### Crear base de datos staging nueva
```bash
docker exec n8n-infra-postgres-1 psql -U n8n_consorcios360 -d n8n_data \
  -c "CREATE DATABASE consorcio360_staging OWNER n8n_consorcios360;"
```

---

## 5. Caddy

### Recargar configuración
```bash
sudo caddy reload --config /etc/caddy/Caddyfile
```

### Ver logs de Caddy
```bash
sudo journalctl -u caddy -f
```

### Validar Caddyfile antes de aplicar
```bash
sudo caddy validate --config /etc/caddy/Caddyfile
```

---

## 6. WireGuard

### Estado de la VPN
```bash
sudo wg show
```

### Levantar WireGuard manualmente (si cayó)
```bash
sudo wg-quick up wg0
```

### Ver peers conectados
```bash
sudo wg show wg0 peers
```

---

## 7. Troubleshooting

### App no responde (producción)

```bash
# 1. Ver estado de contenedores
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# 2. Ver logs de la app
docker logs n8n-infra-app-1 --tail 50

# 3. Ver logs de postgres
docker logs n8n-infra-postgres-1 --tail 20

# 4. Test directo
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8001

# 5. Si todo está caído, levantar
cd ~/n8n-infra && docker compose up -d
```

### Staging no responde

```bash
# Ver contenedor de staging
docker ps --filter "name=dv3aiejieve" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Test
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8002

# Reconectar postgres a red coolify si se perdió
docker network connect coolify n8n-infra-postgres-1
```

### Deploy de Coolify falla con "Permission denied"

```bash
# Verificar permisos
sudo ls -lan /data/coolify/applications/

# Fix si es necesario (no tocar sin entender)
sudo chown 9999:coolify /data/coolify/
sudo chmod 750 /data/coolify/
sudo chown 9999:coolify /data/coolify/applications/
sudo chmod 770 /data/coolify/applications/
sudo chown 9999:coolify-data /data/coolify/applications/dv3aiejieve8cg2lcdlk4265/
sudo chmod 770 /data/coolify/applications/dv3aiejieve8cg2lcdlk4265/
```

### Error 401 en /api/liquidar/

El endpoint requiere `X-Webhook-Token`. Verificar que el header esté presente en el request de n8n.

```bash
# Test correcto
curl -X POST http://127.0.0.1:8001/api/liquidar/ \
  -H "X-Webhook-Token: $(grep N8N_WEBHOOK_SECRET ~/n8n-infra/.env | cut -d= -f2)" \
  -H "Content-Type: application/json" \
  -d '{"test": true}'
```

### DNS no resuelve (post-reinicio)

```bash
# Verificar dnsmasq
sudo systemctl status dnsmasq

# Reiniciar en orden correcto
sudo wg-quick up wg0
sudo systemctl restart dnsmasq
```

---

## 8. Agregar nuevo subdominio DuckDNS

```bash
# 1. Editar docker-compose.yml
nano ~/n8n-infra/docker-compose.yml
# Agregar el nuevo subdominio en: - SUBDOMAINS=haizaraf,n8n-haizaraf,staging-haizaraf,NUEVO

# 2. Aplicar
docker compose up -d duckdns

# 3. Verificar
docker logs n8n-infra-duckdns-1 | tail -5

# 4. Agregar bloque en Caddyfile
sudo nano /etc/caddy/Caddyfile

# 5. Recargar Caddy
sudo caddy reload --config /etc/caddy/Caddyfile
```

---

## 9. Comandos de diagnóstico rápido

```bash
# Estado general de todos los contenedores
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Uso de recursos
docker stats --no-stream

# Espacio en disco
df -h

# Último backup
rclone ls r2:consorcio360-backups/Backup/ | sort | tail -3

# Estado WireGuard
sudo wg show

# Test completo de la app
curl -s -o /dev/null -w "Prod: %{http_code}\n" http://127.0.0.1:8001
curl -s -o /dev/null -w "Staging: %{http_code}\n" http://127.0.0.1:8002
```
