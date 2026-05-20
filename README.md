# TP08 — Monitoreo con Prometheus y Grafana

## Descripción

En este trabajo práctico se implementó un stack completo de monitoreo utilizando Prometheus y Grafana sobre una aplicación Flask ejecutada en contenedores Docker.  

El objetivo fue instrumentar la aplicación para exponer métricas propias, monitorear el estado de los servicios y visualizar la información mediante dashboards en Grafana.

---

# Stack completo

| Servicio | Puerto | Función |
|---|---|---|
| App Flask | :5000 (interno) | Expone métricas mediante `/metrics` |
| Prometheus | :9090 | Recolección y almacenamiento de métricas |
| Grafana | :3000 | Visualización de dashboards |
| Node Exporter | :9100 | Métricas del host: CPU, RAM, disco y red |
| cAdvisor | :8080 (interno) | Métricas de contenedores Docker |

---

# Ejecución

Levantar el stack completo:

```bash
docker compose up -d
```

---

# Accesos

## Grafana
```text
http://localhost:3000
```

Usuario:
```text
admin
```

Contraseña:
```text
devops123
```

## Prometheus
```text
http://localhost:9090
```

---

# Dashboard implementado

El dashboard de Grafana contiene los siguientes paneles:

- Requests por segundo
- Latencia promedio p50
- Total de notas en base de datos
- Tasa de errores HTTP 5xx
- Requests por endpoint
- Latencia p50 / p95 / p99
- Uso de CPU del host
- Uso de memoria RAM del host

---

# Alertas configuradas

## AppDown
Detecta si el backend deja de responder por más de 1 minuto.

## HighCPU
Alerta cuando el uso de CPU supera el 80%.

## HighErrorRate
Detecta una tasa elevada de errores HTTP 5xx.

## DiskSpaceLow
Detecta bajo espacio disponible en disco.

---

# Métricas implementadas

```text
app_requests_total
```
Contador total de requests HTTP.

```text
app_request_duration_seconds
```
Histograma de latencia de requests.

```text
app_notes_total
```
Cantidad total de notas almacenadas.

```text
app_db_errors_total
```
Contador de errores de base de datos.

```text
app_info
```
Información de versión y entorno de la aplicación.

---

# Problema detectado y solución aplicada

Durante la implementación, Prometheus no lograba recolectar métricas desde el backend.  

Al revisar el estado de los contenedores se observó que `notes-backend` se reiniciaba constantemente.

El error encontrado en los logs fue:

```text
exec: gunicorn: not found
```

El problema se debía a que `gunicorn` no estaba instalado dentro de la imagen Docker del backend.

## Solución

Se agregó la dependencia en:

```text
backend/requirements.txt
```

```text
gunicorn==21.2.0
```

Luego se reconstruyó el contenedor:

```bash
docker compose build --no-cache backend
docker compose up -d
```

Después de reconstruir la imagen, el backend quedó funcionando correctamente y Prometheus comenzó a recolectar métricas.

---

# Corrección aplicada a Node Exporter

El script de verificación mostraba el siguiente error:

```text
[FAIL] Node-Exporter → HTTP 000000
```

Esto ocurría porque el servicio utilizaba únicamente `expose`, permitiendo acceso interno entre contenedores, pero no desde el host Ubuntu.

## Solución

Se agregó:

```yaml
ports:
  - "9100:9100"
```

Con esta modificación el endpoint:

```text
http://localhost:9100/metrics
```

quedó accesible correctamente desde el host.

---

# Verificación del stack

```bash
bash scripts/verificar-monitoreo.sh
```

El resultado esperado es:

```text
[OK] notes-backend
[OK] prometheus
[OK] grafana
[OK] node-exporter
[OK] cadvisor
```

---

# Tecnologías utilizadas

- Docker
- Docker Compose
- Flask
- PostgreSQL
- Prometheus
- Grafana
- Node Exporter
- cAdvisor

---

# Conclusión

Se logró implementar un entorno completo de monitoreo para una aplicación Dockerizada utilizando Prometheus y Grafana.  

El sistema permite recolectar métricas en tiempo real, visualizar información mediante dashboards y detectar problemas utilizando alertas automáticas. Además, se resolvieron inconvenientes relacionados con dependencias faltantes y exposición de servicios dentro del entorno Docker.
