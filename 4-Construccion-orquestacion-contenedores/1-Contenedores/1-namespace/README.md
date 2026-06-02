# Práctico: Namespaces de Linux

> **Objetivo**: mostrar qué son los namespaces, qué tipos existen, y cómo "verlos" desde la línea de comandos para entender cómo funcionan los contenedores por debajo.

## 0. Antes de empezar

### ¿Qué es un namespace?

Un **namespace** es una característica del kernel de Linux que **aísla y virtualiza recursos del sistema** para un grupo de procesos. Desde adentro de un namespace, los procesos ven una "vista" propia del recurso (su propio hostname, su propia tabla de procesos, su propia red, etc.), mientras que el resto del sistema sigue funcionando con la vista global.

Los contenedores **no son magia ni una tecnología nueva**: son una combinación de:
- **Namespaces** → aíslan _qué ve_ el proceso (este práctico).
- **Cgroups** → limitan _cuánto consume_ el proceso (próximas clases).
- **Capabilities / seccomp** → restringen _qué puede hacer_ el proceso.

### Tipos de namespaces

| Tipo | Aísla |
|------|-------|
| `mnt` | Puntos de montaje del filesystem |
| `pid` | Tabla de procesos (PIDs) |
| `net` | Interfaces de red, rutas, firewall |
| `ipc` | Colas de mensajes, semáforos, memoria compartida |
| `uts` | Hostname y domainname |
| `user` | UIDs y GIDs (permite "ser root" sin serlo de verdad) |
| `cgroup` | Vista del árbol de cgroups |
| `time` | Reloj monotónico y boot time (kernel ≥ 5.6) |

### Requisitos

- Linux (no funciona en macOS/Windows nativo, ver setup más abajo).
- Permisos de `sudo` (los namespaces requieren capacidades privilegiadas, salvo `user`).
- Paquete `util-linux` (provee `unshare`, `nsenter`, `lsns`).

### Setup en macOS con multipass

`multipass` levanta VMs Ubuntu livianas en Mac (usa el hypervisor nativo en Apple Silicon, sin necesidad de Docker Desktop). **Importante**: Docker Desktop por sí solo no alcanza, porque no nos da una shell con acceso a `unshare`/`nsenter` sobre un kernel propio.

1. **Instalar multipass** (vía Homebrew):
   ```bash
   brew install --cask multipass
   ```

2. **Lanzar una VM** dedicada al práctico:
   ```bash
   multipass launch --name ns-lab --cpus 2 --memory 2G --disk 10G 22.04
   ```
   > El último argumento es la versión de Ubuntu. `lts` también funciona. Listar imágenes disponibles: `multipass find`.

3. **Entrar a la VM**:
   ```bash
   multipass shell ns-lab
   ```

4. **Instalar las herramientas** (dentro de la VM):
   ```bash
   sudo apt update
   sudo apt install -y util-linux iproute2 strace psmisc
   ```
   > `util-linux` trae `unshare`, `nsenter`, `lsns`. `iproute2` trae `ip`. `psmisc` trae `pstree`.

5. **(Opcional) Compartir un directorio** del Mac con la VM, p. ej. para tener el repo a mano:
   ```bash
   # Desde el Mac (no desde la VM):
   multipass mount ~/Documents/Craftech/DiploDevOps ns-lab:/home/ubuntu/diplo
   ```
   Para desmontar: `multipass umount ns-lab:/home/ubuntu/diplo`.

6. **Ciclo de uso**:
   ```bash
   multipass stop ns-lab     # apagar al terminar
   multipass start ns-lab    # volver a usarla
   multipass list            # ver VMs y su estado
   multipass delete ns-lab && multipass purge   # eliminar definitivamente
   ```

7. **Verificar que todo funciona** (dentro de la VM):
   ```bash
   uname -r                       # debe mostrar un kernel Linux
   ls /proc/$$/ns                 # deben aparecer los namespaces
   sudo unshare --uts /bin/bash   # si abre una shell, estás listo
   ```

#### Alternativas en macOS
- **Lima** (`brew install lima`) — similar a multipass, muy popular en la comunidad.
- **OrbStack** — rápido y cómodo, pero requiere licencia para uso laboral.
- **UTM** — GUI completa, útil si querés una VM "visible".
- **Docker Desktop** — sirve para correr `docker run` en los prácticos posteriores, pero **no** para este (no expone una shell sobre el kernel de la VM interna).

#### Setup en Windows
Usar **WSL2** con una distro Ubuntu (`wsl --install -d Ubuntu`). Una vez adentro, los pasos 4 y 7 son iguales.

---

## Ejercicio 1: ¿Dónde "viven" los namespaces?

Cada proceso en Linux pertenece a un conjunto de namespaces, expuestos como enlaces simbólicos especiales en `/proc/<pid>/ns/`.

```bash
ls -l /proc/$$/ns
```

Cada entrada tiene la forma `<tipo>:[<inode>]`. El **inode** identifica unívocamente al namespace: dos procesos con el mismo inode comparten ese namespace.

```bash
readlink /proc/self/ns/uts
readlink /proc/self/ns/pid
```

> ℹ️ Estos no son symlinks "comunes": apuntan a un objeto del kernel (un _file handle_) que se puede pasar a la syscall `setns(2)` para "entrar" a ese namespace.

**Listar todos los namespaces del sistema:**

```bash
sudo lsns
```

#### Pregunta para discutir
- ¿Cuál es la diferencia entre `ls /proc/$$/ns` y `ls /proc/self/ns`? (Pista: ¿quién es `$$` y quién es `self` durante la ejecución de `ls`?)

---

## Ejercicio 2: Namespace UTS (hostname aislado)

Es el más simple: aísla el hostname y el domainname del sistema.

**Terminal A (host):**
```bash
hostname
readlink /proc/self/ns/uts
```

**Terminal B (creamos un namespace UTS nuevo):**
```bash
sudo unshare --uts /bin/bash
hostname mi-contenedor
hostname
readlink /proc/self/ns/uts
```

**Volver a la Terminal A** y ejecutar `hostname` otra vez.

#### ¿Qué observar?
- El inode de `uts` es **distinto** entre las dos terminales.
- Cambiar el hostname adentro **no afecta** al host.
- Salir del shell con `exit` destruye el namespace (si nadie más lo referencia).

---

## Ejercicio 3: Namespace PID (tabla de procesos aislada)

Este es el que más se acerca a la "ilusión" de un contenedor: el proceso adentro se ve a sí mismo como **PID 1**.

```bash
sudo unshare --pid --fork --mount-proc /bin/bash
```

Adentro:
```bash
ps -ef
echo "Mi PID es $$"
```

#### Flags importantes
- `--fork`: imprescindible. La syscall `unshare(CLONE_NEWPID)` no migra el proceso actual al nuevo namespace; solo afecta a sus _hijos_. `--fork` resuelve esto haciendo que el shell sea hijo de `unshare`.
- `--mount-proc`: monta un `/proc` propio para que `ps` muestre los PIDs del nuevo namespace y no los del host.

#### Observar la jerarquía desde el host

En el "contenedor":
```bash
sleep 1000 &
```

En el host:
```bash
pstree -p | grep -E 'unshare|sleep'
ps -ef | grep sleep
```

#### Para discutir
- ¿Cuántos PIDs tiene el `sleep`? ¿Cuál es su "verdadero" PID?
- ¿Qué pasa si matás al PID 1 desde adentro del contenedor? ¿Y desde afuera?

---

## Ejercicio 4: Namespace MNT (montajes aislados)

```bash
sudo unshare --mount /bin/bash
mkdir /tmp/aislado
mount -t tmpfs tmpfs /tmp/aislado
echo "secreto del contenedor" > /tmp/aislado/file
mount | grep aislado
```

En **otra terminal del host**:
```bash
mount | grep aislado    # no aparece
ls /tmp/aislado         # vacío o no existe
```

#### Caso de uso
Cada contenedor monta su propio rootfs (la imagen) sin que esos montajes contaminen el host ni a otros contenedores. Esto es lo que permite que dos contenedores tengan **dos `/etc/hostname` distintos** sobre el mismo kernel.

---

## Ejercicio 5: Namespace NET (red aislada)

```bash
sudo unshare --net /bin/bash
ip link
ip addr
```

Adentro solo se ve `lo` (y encima _down_). No hay eth0, no hay rutas, no hay conectividad.

```bash
ip link set lo up
ping 127.0.0.1
ping 8.8.8.8       # falla: no hay ruta al exterior
```

#### Caso de uso
Esto es exactamente lo que ve un contenedor recién creado **antes** de que Docker/Podman le conecte un `veth pair` a su bridge. La conectividad no es del namespace, la _agrega_ el runtime.

---

## Ejercicio 6: Namespace USER (root falso)

Este es el único namespace que **no requiere `sudo`** para crearse:

```bash
unshare --user /bin/bash
id
```

Adentro: `uid=65534(nobody)` (sin mapeo). Con mapeo:

```bash
unshare --user --map-root-user /bin/bash
id           # uid=0(root) ¡pero solo dentro del namespace!
whoami       # root
touch /etc/shadow   # falla: no sos root afuera
```

#### Por qué importa
Es la base de los **rootless containers** (Podman por defecto, Docker en modo rootless). Permite correr contenedores como "root" sin riesgo real para el host.

---

## Cierre: juntando las piezas

Un contenedor "típico" combina varios namespaces a la vez. Probá:

```bash
sudo unshare --uts --pid --net --mount --ipc --fork --mount-proc /bin/bash
hostname contenedor-completo
ps -ef
ip link
mount | head
```

Esto se acerca mucho a lo que hace `docker run` por dentro.

### Reflexión final

> _Justificá: un contenedor **no** es una máquina virtual._

Pistas:
- Los procesos del contenedor aparecen en `pstree` del host (con otros PIDs, pero existen ahí).
- Comparten **el mismo kernel** que el host.
- No hay hypervisor, no hay arranque de SO, no hay BIOS virtual.

---

## Challenge: ¿cómo lo usa el runtime?

Mientras `containerd`/`dockerd` corre, observá las syscalls relacionadas con namespaces al levantar un contenedor:

```bash
# Terminal 1
sudo strace -f -e trace=unshare,clone,setns,mount -p $(pidof containerd) -o /tmp/strace.log

# Terminal 2
docker run --rm -it alpine sh
```

En `/tmp/strace.log`, buscar las flags `CLONE_NEW*` (`CLONE_NEWPID`, `CLONE_NEWNET`, etc.). Esas son **exactamente las mismas** que usaste con `unshare` en este práctico, solo que invocadas vía syscall directa.

---

## Tareas para entregar

1. **Diagrama**: dibujar el árbol de procesos del Ejercicio 3 mostrando los PIDs visibles desde el contenedor y desde el host. Marcar el "límite" del namespace.
2. **Caso de uso de `mnt`**: describir un escenario real (no de este práctico) donde aislar montajes resuelva un problema concreto.
3. **Investigar**: ¿qué namespace agrega `--cgroup` y por qué podría ser importante para limitar recursos?
---

## Links

- https://man7.org/linux/man-pages/man7/namespaces.7.html
- https://man7.org/linux/man-pages/man1/unshare.1.html
- https://www.toptal.com/linux/separation-anxiety-isolating-your-system-with-linux-namespaces
- https://medium.com/@teddyking/linux-namespaces-850489d3ccf
- https://theboreddev.com/understanding-linux-namespaces/
- https://www.ianlewis.org/en/almighty-pause-container
- https://unix.stackexchange.com/questions/105403/how-to-list-namespaces-in-linux
