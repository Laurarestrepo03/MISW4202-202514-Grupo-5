# 🚀 Experimento de Monitoreo Heartbeat - Táctica de Disponibilidad

Este experimento demuestra la implementación de una **táctica de arquitectura de software** para mejorar la **disponibilidad** del sistema mediante el uso de un **monitor tipo heartbeat**, **ping**, **monitor**

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
- [📽️ Video de evidencia](#️-video-de-evidencia)
- [📚 Referencias](#-referencias)

## 🎯 Objetivo del Experimento

El objetivo es implementar y demostrar cómo funciona una **táctica de monitoreo heartbeat** que:

- ✅ Detecta fallos en servicios de forma temprana
- ✅ Proporciona métricas de disponibilidad en tiempo real
- ✅ Genera alertas automáticas cuando se detectan problemas
- ✅ Mejora la capacidad de respuesta ante incidentes
- ✅ Cantidad de errores detectados en la ejecucion

## 🏗️ Arquitectura del Experimento

```
┌─────────────────┐    ┌─────────────────┐    ┌──────────────────┐
│   Grafana       │◄───┤   Prometheus    │◄───┤ Servicio |Pedidos│
│  (Dashboard)    │    │   (Monitor)     │    │   (Flask App)    │
│  Puerto: 3000   │    │  Puerto: 9090   │    │  Puerto: 8000    │
└─────────────────┘    └─────────────────┘    └──────────────────┘
      
```

### Flujo de Monitoreo Heartbeat:
1. **Prometheus** envía requests cada 10 segundos a `/metrics` del servicio
2. **Docker healthcheck** verifica `/health` cada 30 segundos
3. **Grafana** visualiza métricas y genera alertas

## ⚙️ Prerrequisitos

### Software Requerido

| Software | Versión Mínima | Propósito |
|----------|----------------|-----------|
| **Docker Desktop** | 20.x+ | Containerización |
| **Docker Compose** | 2.x+ | Orquestación de contenedores |
| **Git** | 2.x+ | Control de versiones |
| **curl** | 7.x+ | Pruebas de endpoints |

Los comandos se deben ejecutar en Gitbash si el sistema operativo es Windows

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

### 2. Probar Simulación de Fallos (Ejecutar experimento)
Para ejecutar el comando hay que ejecutar el archivo **test_endpoint.sh**

En caso de ejecutarlo manualmente se puede ejecutar con el siguiente comando bash que repite un ciclo 10 veces

```bash
# Ejecutar múltiples requests. Si la persona quiere hacer una prueba mas larga se puede alterar el ciclo a > 10
start_time=$(date +"%Y-%m-%d %H:%M:%S")
echo "Start time: $start_time"
for i in {1..10}; do
  echo "Request $i"
  time curl -w "HTTP Response Code: %{http_code}\n" http://localhost:8000/orders
  echo "--"
done
end_time=$(date +"%Y-%m-%d %H:%M:%S")
echo "End time: $end_time"
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

### Aclaracion sobre analisis de metricas
Las metricas se visualizan por Graphana pero por su funcionamiento en caso de que dos errores 500 se repitan, no los va a contar como dos errores, sino como un error continuo. Por eso para analizar rigurosamente cada respuesta se debe tener en cuenta la respuesta como error 500 exactamente. 


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

### Configurar Dashboard en Grafana

1. Acceder a Grafana (http://localhost:3000)
2. Login con admin/admin
3. Configurar datasource como **"Prometheus"** (http://prometheus:9090) y seleccionar **Save&test**
4. Ir **Dashboards**, **New**→ **"Import"**
5. Importar el archivo del repositorio `dashboard_grafana.json`
6. Pegar y hacer clic en **"Load"**
7. Seleccionar en time range desde el valor impreso de `start_time` hasta **now** o el valor impreso de `end_time`
8. Para una visualizacion mas rigurosa se puede configurar en el time range la hora de inicio y hora de final del experimento para tener una visualizacion exacta

> Nota: si se configura `start_time` como el tiempo de inicio inmediatamente después de iniciar las peticiones, puede que el dashboard muestre un error de tiempo. Esto es por el delay que tiene Grafana, pero se soluciona después de unos momentos. 

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

## 📽️ Video de evidencia
<!--AGREGAR ENLANCE A VIDEO-->


## 📚 Referencias

### Tecnologías Utilizadas

- [Docker](https://docs.docker.com/) - Containerización
- [Prometheus](https://prometheus.io/docs/) - Monitoreo y métricas
- [Grafana](https://grafana.com/docs/) - Visualización
- [Flask](https://flask.palletsprojects.com/) - Framework web Python


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


