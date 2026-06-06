# Práctico LXC

## ¿Qué es LXC?

LXC (Linux Containers) es la tecnología de contenedores más cercana al kernel. Encaja en la siguiente escala de abstracción:

```
Namespaces / cgroups  →  LXC  →  Docker / Podman
     (kernel puro)     (bajo nivel)   (alto nivel)
```

A diferencia de `unshare` (que crea namespaces individuales a mano), LXC combina todo automáticamente:
- Descarga una imagen base real (Alpine, Ubuntu, Debian...)
- Crea un filesystem completo para el contenedor
- Configura la red (IP propia)
- Aplica cgroups para limitar recursos
- Gestiona el ciclo de vida completo

## Setup

Requiere Linux. Se ejecutó en la VM `ns-lab` (Ubuntu 22.04 via multipass).

```bash
sudo apt install -y lxc
```

## Ciclo de vida de un contenedor LXC

### 1. Crear el contenedor
```bash
sudo lxc-create --name DiploDevOps --template download -- --dist alpine --release 3.22 --arch amd64
```
Descarga la imagen de Alpine Linux 3.22 y crea el filesystem del contenedor en `/var/lib/lxc/DiploDevOps/`. Equivalente a `docker pull` + `docker create` juntos.

### 2. Arrancar el contenedor
```bash
sudo lxc-start --name DiploDevOps
```
LXC crea los namespaces (UTS, PID, NET, MNT) y los cgroups automáticamente — lo mismo que se hace a mano con `unshare`, pero de una sola vez.

### 3. Ver información del contenedor
```bash
sudo lxc-info --name DiploDevOps
```
Muestra el estado, la IP asignada, el PID raíz en el host y el uso de memoria.

### 4. Listar contenedores
```bash
sudo lxc-ls --fancy
```
Lista todos los contenedores con estado, IP y si están corriendo.

### 5. Entrar al contenedor
```bash
sudo lxc-attach --name DiploDevOps
```
Equivalente a `docker exec -it`. Desde adentro se ve como root en Alpine.

### 6. Detener y destruir
```bash
sudo lxc-stop --name DiploDevOps
sudo lxc-destroy --name DiploDevOps
```
Detiene el contenedor y elimina su filesystem completo.

### 7. Verificar que se destruyó
```bash
sudo lxc-ls --fancy
```

## LXC vs Docker/Podman

| | LXC | Docker / Podman |
|--|-----|----------------|
| Nivel | Bajo nivel | Alto nivel |
| Imágenes | Plantillas (no registry) | Registry (Docker Hub, quay.io...) |
| Dockerfile | No | Sí |
| Orquestación | No | Sí (Compose, K8s) |
| Uso hoy | Proxmox, hosting compartido | Desarrollo, microservicios |

## Nota

LXC es un motor de bajo nivel — no provee nativamente herramienta para construir imágenes base. Para eso existe **Distrobuilder**: https://linuxcontainers.org/distrobuilder/docs/latest/tutorials/use/

Docker usaba LXC como backend en sus primeras versiones antes de crear `libcontainer`. Hoy son independientes pero comparten los mismos conceptos del kernel.
