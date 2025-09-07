# 🚀 Experimento de Monitoreo Heartbeat - Táctica de Disponibilidad

Este experimento demuestra la implementación de una **táctica de arquitectura de software** para mejorar la **disponibilidad** del sistema mediante el uso de un **monitor tipo heartbeat**.

## 📋 Tabla de Contenidos

- [🎯 Objetivo del Experimento](#-objetivo-del-experimento)
- [🏗️ Arquitectura del Sistema](#️-arquitectura-del-sistema)
- [⚙️ Prerrequisitos](#️-prerrequisitos)
- [🚀 Configuración del Entorno](#-configuración-del-entorno)
- [📊 Componentes del Sistema](#-componentes-del-sistema)
- [🔧 Ejecución del Experimento](#-ejecución-del-experimento)
- [🧪 Pruebas y Validación](#-pruebas-y-validación)
- [📈 Visualización y Monitoreo](#-visualización-y-monitoreo)
- [🛠️ Solución de Problemas](#️-solución-de-problemas)
- [📚 Referencias](#-referencias)

## 🎯 Objetivo del Experimento

El objetivo es implementar y demostrar cómo funciona una **táctica de monitoreo heartbeat** que:

- ✅ Detecta fallos en servicios de forma temprana
- ✅ Proporciona métricas de disponibilidad en tiempo real
- ✅ Genera alertas automáticas cuando se detectan problemas
- ✅ Mejora la capacidad de respuesta ante incidentes

## 🏗️ Arquitectura del Sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Grafana       │◄───┤   Prometheus    │◄───┤ Servicio |Pedidos│
│  (Dashboard)    │    │   (Monitor)     │    │   (Flask App)   │
│  Puerto: 3000   │    │  Puerto: 9090   │    │  Puerto: 8000   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         ▲                                              │
         │               ┌─────────────────┐           │
         └───────────────┤   MailPit       │◄──────────┘
                         │ (SMTP Testing)  │
                         │  Puerto: 8025   │
                         └─────────────────┘
```

### Flujo de Monitoreo Heartbeat:
1. **Prometheus** envía requests cada 10 segundos a `/metrics` del servicio
2. **Docker healthcheck** verifica `/health` cada 30 segundos
3. **Grafana** visualiza métricas y genera alertas
4. **MailPit** simula el envío de notificaciones por email

## ⚙️ Prerrequisitos

### Software Requerido

| Software | Versión Mínima | Propósito |
|----------|----------------|-----------|
| **Docker Desktop** | 20.x+ | Containerización |
| **Docker Compose** | 2.x+ | Orquestación de contenedores |
| **Git** | 2.x+ | Control de versiones |
| **curl** | 7.x+ | Pruebas de endpoints |

### Verificación de Prerrequisitos

Ejecuta los siguientes comandos para verificar que tienes todo instalado:

```bash
# Verificar Docker
docker --version
# Salida esperada: Docker version 24.x.x, build xxxxxxx

# Verificar Docker Compose
docker compose --version
# Salida esperada: Docker Compose version v2.x.x

# Verificar Git
git --version
# Salida esperada: git version 2.x.x

# Verificar curl
curl --version
# Salida esperada: curl 7.x.x
```

### Puertos Requeridos

Asegúrate de que los siguientes puertos estén disponibles:

| Puerto | Servicio | Descripción |
|--------|----------|-------------|
| **3000** | Grafana | Dashboard de monitoreo |
| **8000** | Flask App | Servicio de pedidos |
| **9090** | Prometheus | Motor de métricas |
| **1025** | MailPit SMTP | Servidor SMTP de prueba |
| **8025** | MailPit Web | Interfaz web para emails |

```bash
# Verificar puertos disponibles (Windows)
netstat -an | findstr "3000 8000 9090 1025 8025"
# No debe mostrar ninguna salida si los puertos están libres
```

## 🚀 Configuración del Entorno

### Paso 1: Clonar el Repositorio

```bash
# Clonar el repositorio
git clone https://github.com/Laurarestrepo03/MISW4202-202514-Grupo-5.git

# Navegar al directorio del proyecto
cd MISW4202-202514-Grupo-5
```

### Paso 2: Navegar al Directorio del Experimento

```bash
# Ir al directorio específico del experimento
cd experimento/pedidos

```

### Paso 3: Verificar Archivos del Proyecto

```bash
# Listar archivos del proyecto
ls -la

# Debes ver estos archivos:
# - docker-compose.yml (configuración de contenedores)
# - app.py (aplicación Flask)
# - Dockerfile (imagen del servicio)
# - prometheus.yml (configuración de Prometheus)
# - requirements.txt (dependencias Python)
# - dashboard_grafana.json (dashboard predefinido)
```

## 📊 Componentes del Sistema

### 1. **Servicio de Pedidos (Flask)**
- **Archivo**: `app.py`
- **Puerto**: 8000
- **Endpoints**:
  - `GET /health` - Endpoint de salud (heartbeat)
  - `GET /orders` - Servicio principal (con fallos simulados)
  - `GET /metrics` - Métricas para Prometheus

### 2. **Prometheus (Monitor)**
- **Imagen**: `prom/prometheus`
- **Puerto**: 9090
- **Configuración**: `prometheus.yml`
- **Función**: Recolecta métricas cada 10 segundos

### 3. **Grafana (Dashboard)**
- **Imagen**: `grafana/grafana`
- **Puerto**: 3000
- **Credenciales**: admin/admin
- **Función**: Visualiza métricas y alertas

### 4. **MailPit (Notificaciones)**
- **Imagen**: `axllent/mailpit`
- **Puertos**: 1025 (SMTP), 8025 (Web)
- **Función**: Simula envío de alertas por email

## 🔧 Ejecución del Experimento

### Ejecución Completa

```bash
# 1. Asegúrate de estar en el directorio correcto
cd experimento/pedidos

# 2. Construir y levantar todos los servicios
docker compose up --build -d

# 3. Verificar que todos los contenedores estén funcionando
docker compose ps
```

### Estado Esperado de los Contenedores

```
NAME                 STATUS
grafana-monitor      Up X seconds
pedidos-pedidos-1    Up X seconds (healthy)
prometheus-monitor   Up X seconds
smtp-monitor         Up X seconds (healthy)
```

## 🧪 Pruebas y Validación

### 1. Verificar el Heartbeat

```bash
# Probar endpoint de salud
curl http://localhost:8000/health

# Respuesta esperada:
# {"status":"healthy","timestamp":"2025-09-07T14:42:17.900702"}
```

### 2. Probar Simulación de Fallos

```bash
# Ejecutar múltiples requests (50% de probabilidad de fallo)
for i in {1..10}; do 
  echo "Request $i:"
  curl -s http://localhost:8000/orders | head -c 100
  echo -e "\n---"
  sleep 1
done
```

**Respuestas Posibles:**
- ✅ **Éxito**: `{"orders":[...], "total_count":3}`
- ❌ **Fallo**: `{"error":"Internal Server Error"}`

### 3. Verificar Métricas

```bash
# Ver métricas de Prometheus
curl http://localhost:8000/metrics | grep flask_http_request_total

# Salida esperada (ejemplo):
# flask_http_request_total{method="GET",status="200"} 5.0
# flask_http_request_total{method="GET",status="500"} 3.0
```

## 📈 Visualización y Monitoreo

### Acceso a las Interfaces

1. **Prometheus** (Motor de métricas):
   - URL: http://localhost:9090
   - Queries útiles:
     - `flask_http_request_total` - Total de requests
     - `flask_http_request_duration_seconds` - Tiempo de respuesta
     - `up` - Estado de los servicios

2. **Grafana** (Dashboard):
   - URL: http://localhost:3000
   - Usuario: `admin`
   - Contraseña: `admin`

3. **MailPit** (Email testing):
   - URL: http://localhost:8025
   - Ver emails de alertas simulados

### Configurar Dashboard en Grafana

1. Acceder a Grafana (http://localhost:3000)
2. Login con admin/admin
3. Configurar datasource como **"Prometheus"** (http://prometheus:9090) y seleccionar **Save&test**
4. Ir **Dashboards**, **New**→ **"Import"**
5. Importar el archivo del repositorio `dashboard_grafana.json`
6. Pegar y hacer clic en **"Load"**
7. Seleccionar en time range **last 5 minutes** mientras se ejecuta el experimento


## 🛠️ Solución de Problemas

### Problema: Contenedores no inician

```bash
# Verificar logs
docker compose logs

# Verificar puertos ocupados
netstat -tlnp | grep -E "3000|8000|9090|1025|8025"

# Limpiar y reiniciar
docker compose down -v
docker compose up --build -d
```

### Problema: Healthcheck fallando

```bash
# Verificar logs del servicio
docker compose logs pedidos

# Probar endpoint manualmente
curl -v http://localhost:8000/health

# Reiniciar servicio específico
docker compose restart pedidos
```

### Problema: Prometheus no encuentra targets

```bash
# Verificar configuración
cat prometheus.yml

# Verificar conectividad de red
docker network ls
docker network inspect monitoring
```

### Problema: Grafana no muestra datos

1. Verificar datasource en Grafana
2. URL debe ser: `http://prometheus:9090` (no localhost)
3. Verificar que Prometheus esté recolectando métricas

## 🔍 Comandos Útiles

### Docker Management

```bash
# Ver logs de todos los servicios
docker compose logs

# Ver logs de un servicio específico
docker compose logs -f pedidos

# Reiniciar un servicio
docker compose restart prometheus

# Detener todos los servicios
docker compose down

# Limpiar completamente (incluyendo volúmenes)
docker compose down -v

# Ver recursos utilizados
docker compose ps
docker system df
```

### Monitoreo en Tiempo Real

```bash
# Ver logs en vivo
docker compose logs -f

# Monitor de recursos
docker stats

# Verificar salud de contenedores
watch -n 5 'docker compose ps'
```

## 📚 Referencias

### Tecnologías Utilizadas

- [Docker](https://docs.docker.com/) - Containerización
- [Prometheus](https://prometheus.io/docs/) - Monitoreo y métricas
- [Grafana](https://grafana.com/docs/) - Visualización
- [Flask](https://flask.palletsprojects.com/) - Framework web Python
- [MailPit](https://mailpit.axllent.org/) - Testing SMTP

### Enlaces Útiles

- [Prometheus Query Language](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Grafana Dashboard Creation](https://grafana.com/docs/grafana/latest/dashboards/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)

---

## 🤝 Soporte

Si encuentras algún problema:

1. Revisa la sección de **Solución de Problemas**
2. Verifica que cumples todos los **Prerrequisitos**
3. Consulta los **logs** de los contenedores
4. Asegúrate de estar en el **directorio correcto**


