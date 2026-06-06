# Práctico — Volúmenes

## ¿Por qué existen los volúmenes?

Los contenedores son **efímeros** — cuando se eliminan, todo lo escrito dentro desaparece. Los volúmenes permiten que los datos sobrevivan al ciclo de vida del contenedor.

---

## Tipos de montaje

### Bind mount
Mapea un directorio del host directamente dentro del contenedor.

```yaml
volumes:
  - ./uploads:/code/src/uploads
```

- Los archivos viven en el filesystem del host (tu Mac)
- Visible y accesible desde el host directamente
- Depende del path absoluto del host
- Útil para desarrollo (hot reload, edición directa)

### Docker Volume
Docker/Podman gestiona el storage en su propio directorio.

```yaml
volumes:
  - uploads-data:/code/src/uploads

volumes:
  uploads-data:
```

- Los archivos viven en la VM de Podman (`/var/home/core/.local/share/containers/storage/volumes/`)
- No visible directamente en el host Mac
- Independiente del path del host
- Recomendado para producción

---

## Ejercicio 1 — Bind mount

### Setup

```bash
# Instalar podman-compose (necesario en macOS — podman compose usa docker-compose externo)
brew install podman-compose

# Levantar la app
cd apps/
podman-compose up -d
```

La app es un servidor Flask que acepta uploads de imágenes (jpg, png, gif) expuesto en `http://localhost:8081`.

### Observaciones

- Al subir una imagen, aparece en `./apps/uploads/` del host inmediatamente
- Al eliminar el contenedor (`podman-compose down`), el archivo persiste en el host
- Al levantar un contenedor nuevo, encuentra los archivos del anterior

| Acción | ¿Qué pasa con los archivos? |
|--------|---------------------------|
| Subís una imagen | Se guarda en `./uploads/` del host |
| Eliminás el contenedor | Los archivos siguen en el host |
| Nuevo contenedor | Encuentra los archivos del anterior |
| Borrás `./uploads/` manualmente | Se pierden para siempre |

---

## Challenge — Migrar a Docker Volume y simular recuperación

### Modificar docker-compose.yaml

```yaml
services:
  app-volumen:
    build: ./app-volumen/
    ports:
      - "8081:8000"
    volumes:
      - uploads-data:/code/src/uploads

volumes:
  uploads-data:
```

### Inspeccionar el volumen

```bash
podman volume ls
# DRIVER      VOLUME NAME
# local       apps_uploads-data   ← podman-compose prefija con el nombre del proyecto

podman volume inspect apps_uploads-data
# Mountpoint: /var/home/core/.local/share/containers/storage/volumes/apps_uploads-data/_data
```

### Simulación de backup y recuperación

**1. Hacer backup del volumen:**
```bash
podman run --rm \
  -v apps_uploads-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/backup-uploads.tar.gz -C /data .
```

**2. Simular desastre (eliminar volumen):**
```bash
podman-compose down
podman volume rm apps_uploads-data
```

**3. Recuperar:**
```bash
podman volume create apps_uploads-data
podman run --rm \
  -v apps_uploads-data:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/backup-uploads.tar.gz -C /data
```

**4. Verificar:**
```bash
podman-compose up -d
# Acceder a http://localhost:8081/uploads/gatito.png
# El archivo está disponible sin haberlo subido de nuevo
```

### Conclusión

El template de la app no lista archivos en la UI — para verificar los archivos restaurados hay que acceder directamente por URL: `http://localhost:8081/uploads/<filename>`.

---

## Bind mount vs Docker Volume — Cuándo usar cada uno

| | Bind mount | Docker Volume |
|--|--|--|
| Dónde viven los datos | Host (path definido) | Gestionado por Docker/Podman |
| Desarrollo | Ideal (edición directa) | No recomendado |
| Producción | No recomendado | Recomendado |
| Portabilidad | Depende del path del host | Independiente |
| Backup | Copiar el directorio | `docker run --rm -v ... tar` |
