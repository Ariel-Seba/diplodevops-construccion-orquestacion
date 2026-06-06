# Práctico — Docker Networking

## El problema de seguridad

Por defecto todos los contenedores en un docker-compose comparten la misma red y pueden verse entre sí. Si alguien compromete nginx, puede hablar directamente con la BD.

La solución es **segmentar en dos redes**:

```
host ──► nginx ──► app ──► db
         │                  │
    red: frontend      red: backend
    (nginx + app)      (app + db)
```

- **nginx** solo en `frontend` → no puede ver la BD
- **db** solo en `backend` → no puede ser alcanzada desde el host
- **app** en ambas redes → único intermediario entre nginx y la BD

---

## Arquitectura implementada

### Estructura de archivos

```
3-networking/
├── app/
│   ├── app.py           # Flask API con conexión a PostgreSQL
│   ├── requirements.txt
│   └── Dockerfile
├── nginx/
│   └── nginx.conf       # Reverse proxy hacia app:5000
└── docker-compose.yaml  # Orquestación con redes segmentadas
```

### app.py — Endpoints

```
GET  /          → lista todas las personas
POST /personas  → crea una persona nueva
```

Tabla `personas`: id (PK), nombre, apellido, documento.

### docker-compose.yaml — Redes y servicios

```yaml
services:

  nginx:
    image: nginx:alpine
    ports:
      - "8080:80"          # único punto de entrada desde el host
    networks:
      - frontend            # NO tiene acceso a backend

  app:
    build: ./app
    depends_on:
      db:
        condition: service_healthy   # espera el healthcheck de db
    networks:
      - frontend
      - backend             # puente entre las dos redes

  db:
    image: postgres:15-alpine
    volumes:
      - db-data:/var/lib/postgresql/data   # persistencia
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - backend             # NO tiene acceso a frontend

networks:
  frontend:
  backend:

volumes:
  db-data:
```

---

## Verificación del aislamiento

### Levantar la arquitectura

```bash
podman-compose up --build -d
```

### Probar los endpoints

```bash
# Listar personas (vacío al inicio)
curl http://localhost:8080/

# Crear una persona
curl -X POST http://localhost:8080/personas \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Juan", "apellido": "Perez", "documento": 12345678}'

# Verificar que se guardó
curl http://localhost:8080/
```

### Verificar aislamiento de redes

```bash
# nginx NO puede alcanzar la BD → falla (no resuelve hostname 'db')
podman exec -it 3-networking_nginx_1 sh -c "ping db"

# app SÍ puede alcanzar la BD
podman exec -it 3-networking_app_1 sh -c "ping db"

# app SÍ puede alcanzar nginx
podman exec -it 3-networking_app_1 sh -c "ping nginx"
```

**Resultado:**
```
nginx → db:    ❌ BLOQUEADO (no existe en su red)
app   → db:    ✅ OK
app   → nginx: ✅ OK
```

---

## Conceptos clave

### DNS interno de Docker/Podman
Dentro de una red de compose, cada servicio se resuelve por su nombre (`db`, `app`, `nginx`). Si un contenedor no está en la misma red, el nombre no existe para él — no es que esté bloqueado, directamente no se puede resolver.

### Healthcheck
```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U postgres"]
  interval: 5s
  timeout: 5s
  retries: 5
```
`pg_isready` es el comando nativo de PostgreSQL para verificar que el servidor acepta conexiones. `depends_on: condition: service_healthy` hace que la app espere hasta que el healthcheck pase antes de arrancar — evita errores de conexión en el inicio.

### Volumen para la BD
```yaml
volumes:
  - db-data:/var/lib/postgresql/data
```
Los datos de PostgreSQL persisten aunque se destruya el contenedor. Sin esto, cada `podman-compose down` borra toda la base de datos.
