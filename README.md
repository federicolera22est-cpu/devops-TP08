# TP08 — Monitoreo con Prometheus y Grafana

## Stack completo

| Servicio | Puerto | Función |
|---|---|---|
| App Flask | :5000 (interno) | Expone `/metrics` con prometheus_client |
| Prometheus | :9090 | Scrape cada 15s, retención 15 días |
| Grafana | :3000 | Dashboards + provisioning automático |
| Node Exporter | :9100 (interno) | CPU, RAM, disco, red del host |
| cAdvisor | :8080 (interno) | Métricas de contenedores Docker |

## Acceso

Ejecutar en bash
docker compose up -d
## Grafana: 
http://localhost:3000  →  admin / devops123
## Prometheus: 
http://localhost:9090

Dashboard: 8 paneles
```
•	Requests por segundo (stat)
•	Latencia p50 (stat)
•	Total notas en DB (stat)
•	Tasa de errores 5xx (stat)
•	Requests por endpoint (timeseries)
•	Latencia p50/p95/p99 (timeseries)
•	CPU del host (timeseries)
•	Memoria del host (timeseries)
```
Alertas configuradas
```
•	AppDown — backend caído por más de 1 minuto
•	HighCPU — CPU > 80% por 2 minutos
•	HighErrorRate — errores 5xx > 5% por 1 minuto
•	DiskSpaceLow — disco > 85% por 5 minutos
```
Métricas propias de la app
```
app_requests_total          # contador por método/endpoint/status
app_request_duration_seconds # histograma de latencia
app_notes_total              # gauge: notas en la DB
app_db_errors_total          # contador de errores de DB
app_info                     # versión y entorno
```
