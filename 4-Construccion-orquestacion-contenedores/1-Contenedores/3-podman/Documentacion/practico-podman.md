# Práctico Podman

## Instalación en macOS (Homebrew)

```bash
brew install podman
```

Podman en macOS necesita una VM Linux liviana para correr los contenedores (no tiene daemon propio como Docker Desktop).

```bash
podman machine init    # crea la VM
podman machine start   # la arranca
```

Verificar que está corriendo:
```bash
podman machine list
```

---

## Configuración de registries

Podman busca imágenes en los registries definidos en el archivo de configuración. En vez de modificar el global, usamos uno por usuario:

```bash
mkdir -p ~/.config/containers
nano ~/.config/containers/registries.conf
```

Contenido:
```
unqualified-search-registries = ['docker.io', 'quay.io']
```

**Observación**: `podman search httpd` sin prefijo prioriza `docker.io`. Para buscar explícitamente en `quay.io`:
```bash
podman search quay.io/httpd
```

---

## Comandos básicos

### Correr un contenedor en segundo plano
```bash
podman run -d -p 8080:80 docker.io/library/httpd
```
- `-d` → detached, corre en segundo plano
- `-p 8080:80` → mapea el puerto 8080 del Mac al puerto 80 del contenedor
- Resultado: `http://localhost:8080` muestra `It works!`

### Pullear una imagen
```bash
podman pull docker.io/library/nginx
```

### Listar imágenes descargadas
```bash
podman images
```

Salida obtenida:
```
docker.io/library/nginx  latest      dbee862e8e1d  2 weeks ago  185 MB
docker.io/library/httpd  latest      87e0a607bc38  2 weeks ago  150 MB
```

### Listar contenedores corriendo
```bash
podman ps
```

### Limpiar todos los contenedores de golpe
```bash
podman rm -f $(podman ps -aq)
```

---

## Diferencias clave con Docker

| | Docker | Podman |
|--|--------|--------|
| Daemon | Sí (dockerd corriendo siempre) | No (daemonless) |
| Root por defecto | Sí | No (rootless por defecto) |
| Comandos | `docker run`, `docker build`... | idénticos (`podman run`, `podman build`...) |
| Build de imágenes | BuildKit | Buildah (por debajo) |

Los comandos son compatibles — muchos equipos usan `alias docker=podman` al migrar.

---

## Construcción y publicación de imágenes

```bash
podman login <registry>
podman build -t <username>/<image-name> .
podman push <username>/<image-name>
```

Podman es compatible con Dockerfile. El comando `podman build` usa **Buildah** por debajo para construir las imágenes.
