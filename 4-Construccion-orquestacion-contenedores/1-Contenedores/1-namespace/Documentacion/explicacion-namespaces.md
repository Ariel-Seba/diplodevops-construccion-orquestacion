# Linux Namespaces — Explicación completa

---

## El problema que resuelven los namespaces

Imaginá que tenés un servidor con un solo sistema operativo. Querés correr dos aplicaciones que:
- Las dos quieren ser `root`
- Las dos quieren escuchar en el puerto 80
- Las dos tienen sus propios archivos de configuración en `/etc`

Sin aislamiento, se pisan entre sí. La solución tradicional era una VM completa por aplicación — costoso y lento. Los namespaces son la solución del kernel Linux: **aislamiento liviano sin necesidad de un SO separado**.

---

## ¿Qué es exactamente un namespace?

Es una **característica del kernel** que le da a un grupo de procesos una **vista propia** de un recurso del sistema.

La clave es esa palabra: **vista**. No hay dos kernels, no hay dos sistemas de archivos reales, no hay dos redes reales. Hay **un solo kernel** que le muestra cosas distintas a distintos grupos de procesos.

Analogía: es como dos personas mirando el mismo edificio desde distintos pisos. El edificio es uno solo, pero cada uno ve un paisaje diferente por su ventana.

---

## Los 8 tipos de namespaces

| Tipo | ¿Qué aísla? | Ejemplo práctico |
|------|-------------|-----------------|
| `uts` | Hostname y domainname | Cada contenedor tiene su propio nombre |
| `pid` | Tabla de procesos | Un contenedor ve solo sus propios procesos |
| `mnt` | Puntos de montaje | Cada contenedor tiene su propio filesystem |
| `net` | Red (interfaces, rutas, firewall) | Cada contenedor tiene su propio `eth0` |
| `ipc` | Colas de mensajes, semáforos | Procesos aislados no se comunican accidentalmente |
| `user` | UIDs y GIDs | Ser "root" dentro sin serlo afuera |
| `cgroup` | Vista del árbol de cgroups | Ver solo tus propios límites de recursos |
| `time` | Reloj monotónico y boot time | Distinto "tiempo de arranque" por contenedor |

---

## Ejercicio por ejercicio — qué aprendimos

### Ejercicio 1: `/proc/$$/ns` — donde viven los namespaces

```bash
ls -l /proc/$$/ns
```

Cada proceso en Linux tiene una carpeta en `/proc/<pid>/ns/` con un **symlink por cada namespace al que pertenece**. Esos symlinks tienen la forma:

```
uts -> uts:[4026531838]
pid -> pid:[4026531836]
```

El número entre corchetes es el **inode del namespace**. Si dos procesos tienen el mismo inode en el mismo tipo de namespace → **comparten ese namespace**. Si tienen inodes distintos → están aislados.

Esto es importante porque el kernel identifica namespaces por inode, no por nombre. Cuando hacés `docker run`, lo que Docker hace por debajo es crear procesos con inodes de namespace distintos al del host.

**La pregunta `$$` vs `self`:** `$$` es el PID del shell actual, evaluado *antes* de que `ls` arranque. `self` es resuelto por el kernel en el momento en que el proceso hace la syscall — o sea apunta al proceso que está leyendo, que es `ls`. Son el mismo namespace pero son conceptualmente distintos.

---

### Ejercicio 2: UTS namespace — hostname aislado

```bash
sudo unshare --uts /bin/bash
hostname mi-contenedor
```

`unshare` es el comando que le dice al kernel: *"creá un namespace nuevo de tipo UTS y poné este proceso adentro"*.

Lo que vimos:
- El inode de `uts` **cambia** → confirmación de que estamos en un namespace nuevo
- Cambiar el hostname adentro **no afecta** al host → el aislamiento funciona
- Al hacer `exit` → el namespace se destruye (porque ningún proceso lo referencia más)

Este es el namespace más simple y sirve para entender el mecanismo base antes de ver los más complejos.

---

### Ejercicio 3: PID namespace — tabla de procesos aislada (el más importante)

```bash
sudo unshare --pid --fork --mount-proc /bin/bash
```

Este es el que más se parece a lo que hace un contenedor real. Lo que vimos en la VM:

**Desde adentro:**
```
PID 1 → /bin/bash
PID 8 → sleep 1000
```

**Desde el host:**
```
PID 3546 → /bin/bash    (el mismo proceso)
PID 3553 → sleep 1000   (el mismo proceso)
```

El bash **cree que es PID 1** — el proceso init, el rey del sistema. En un Linux real, si PID 1 muere, el kernel entra en pánico. Dentro del namespace, si matás PID 1 (el bash), todos los procesos del namespace mueren. Desde afuera podés matar PID 3546 y lograr el mismo efecto.

**¿Por qué `--fork`?**
La syscall `unshare(CLONE_NEWPID)` tiene una particularidad: no mete al proceso actual en el nuevo namespace, sino solo a sus **hijos**. Si no usás `--fork`, el bash seguiría en el namespace viejo. Con `--fork`, unshare se clona a sí mismo y el hijo (el bash) queda dentro del namespace nuevo.

**¿Por qué `--mount-proc`?**
`ps` no lee procesos directamente del kernel — lee `/proc`. Si no montás un `/proc` propio dentro del namespace, `ps` sigue leyendo el `/proc` del host y ve todos los procesos del sistema. Con `--mount-proc` montás un tmpfs fresco en `/proc` que solo refleja los PIDs del namespace actual.

---

### Ejercicio 4: MNT namespace — sistema de archivos aislado

```bash
sudo unshare --mount /bin/bash
mount -t tmpfs tmpfs /tmp/aislado
```

Este namespace aísla los **puntos de montaje**. Lo que montás adentro no aparece afuera, y viceversa.

Este es el namespace que permite que Docker funcione: cuando corrés `docker run ubuntu`, el contenedor monta la imagen de Ubuntu en su `/` sin que eso afecte el filesystem del host. Cada contenedor puede tener **su propio `/etc`, `/usr`, `/var`** — todos son montajes aislados sobre el mismo kernel.

**Caso de uso real:** Un job de CI/CD monta sus credenciales en `/run/secrets/token`. Con namespace MNT, otro job corriendo en paralelo no puede ver ese montaje aunque comparta el mismo host.

---

### Ejercicio 5: NET namespace — red aislada

```bash
sudo unshare --net /bin/bash
ip link   # solo ves 'lo', y está down
```

Cada namespace NET tiene su propia tabla de interfaces, rutas y reglas de firewall. Un namespace NET recién creado tiene solo `lo` (loopback) y sin conectividad.

Esto es **exactamente** lo que ve un contenedor Docker recién creado. La conectividad que tiene un contenedor con el exterior no viene del namespace — la agrega Docker por fuera, conectando un par de interfaces virtuales (`veth pair`): un extremo dentro del namespace del contenedor, el otro en el bridge `docker0` del host.

Sin esa intervención del runtime, el contenedor está completamente incomunicado.

---

### Ejercicio 6: USER namespace — root falso

```bash
unshare --user --map-root-user /bin/bash
id        # uid=0(root)
touch /etc/shadow   # Permission denied
```

Este es el namespace más interesante desde el punto de vista de seguridad. Permite que un proceso **crea que es root** (UID 0) dentro del namespace, pero el kernel sabe que en realidad es un usuario sin privilegios del host.

Es la base de los **rootless containers** — Podman por defecto los usa así. Podés correr contenedores como root sin que un escape del contenedor comprometa el host, porque el "root" dentro no tiene capacidades reales afuera.

---

### El cierre: todo junto

```bash
sudo unshare --uts --pid --net --mount --ipc --fork --mount-proc /bin/bash
```

Eso es esencialmente lo que hace `docker run` — combina múltiples namespaces de golpe. La diferencia entre Docker y lo que hicimos nosotros es que Docker también:
1. Prepara un filesystem (imagen) y lo monta con `overlayfs`
2. Conecta interfaces de red (`veth pair`)
3. Aplica límites de recursos con **cgroups** (próximo tema)
4. Aplica restricciones de syscalls con **seccomp**

---

## La conclusión grande: un contenedor NO es una VM

| | VM | Contenedor |
|--|----|----|
| Kernel | Propio (virtualizado) | **Compartido con el host** |
| Arranque | Minutos (boot completo) | Milisegundos |
| Aislamiento | Hypervisor (hardware) | Namespaces (kernel) |
| Overhead | Alto | Mínimo |
| Visibilidad | Opaca para el host | Los procesos aparecen en `pstree` del host |

Los procesos de los contenedores aparecen en `pstree` del host con PIDs reales — el kernel los ve a todos. Los namespaces son una ilusión controlada, no un aislamiento físico.
