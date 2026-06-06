# Tarea 3 — El namespace `--cgroup`

## ¿Qué son los cgroups? (contexto necesario)

Los **cgroups** (control groups) son la otra gran tecnología detrás de los contenedores, junto con los namespaces. Mientras los namespaces controlan *qué ve* un proceso, los cgroups controlan *cuánto consume*:

- Máximo de CPU que puede usar
- Máximo de RAM
- Máximo de I/O de disco
- Máximo de procesos que puede crear

El kernel organiza los cgroups en un **árbol jerárquico**:

```
/sys/fs/cgroup/
├── system.slice/
│   ├── docker.service/
│   │   ├── contenedor-A/   ← limitado a 512MB RAM
│   │   └── contenedor-B/   ← limitado a 1GB RAM
│   └── ssh.service/
└── user.slice/
```

## El problema sin namespace cgroup

Sin namespace cgroup, un proceso dentro de un contenedor puede leer `/sys/fs/cgroup/` y ver **todo el árbol** — incluyendo los límites de otros contenedores, cuánta RAM usa el host, qué otros servicios corren. Es una filtración de información.

Peor aún: herramientas como `systemd` dentro del contenedor intentan escribir en ese árbol y chocan con la estructura del host.

## Lo que agrega el namespace cgroup

Le muestra al proceso su propio nodo del árbol como si fuera la raíz `/`. En vez de ver su lugar real:

```
/sys/fs/cgroup/system.slice/docker.service/contenedor-A/
```

Ve esto:

```
/sys/fs/cgroup/   ← cree que es la raíz
```

## ¿Por qué es importante para limitar recursos?

1. **Seguridad**: el contenedor no puede ver los límites ni el consumo de otros contenedores.

2. **`systemd` dentro de contenedores**: systemd asume que es dueño del árbol de cgroups desde la raíz. Sin namespace cgroup, rompe la jerarquía del host. Con el namespace, systemd ve su propio árbol y funciona correctamente.

3. **Herramientas de monitoreo**: `top`, `htop`, `free` dentro del contenedor muestran los límites *del contenedor*, no los del host completo. Sin este namespace, `free -m` dentro de un contenedor con 512MB de límite mostraría los 32GB del host — confundiendo a desarrolladores y herramientas de auto-scaling.

## Resumen

| Sin namespace cgroup | Con namespace cgroup |
|----------------------|----------------------|
| Ve todo el árbol del host | Ve solo su subárbol como raíz |
| Filtra info de otros contenedores | Aislamiento total de la vista |
| `systemd` interno rompe el host | `systemd` funciona correctamente |
| `free` muestra RAM del host | `free` muestra el límite real del contenedor |
