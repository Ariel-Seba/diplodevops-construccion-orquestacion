# Práctico — Setup Kubernetes con K3D

## ¿Qué es Kubernetes?

Orquestador de contenedores que gestiona múltiples máquinas como una unidad. Resuelve:
- Alta disponibilidad: si un contenedor muere, lo recrea automáticamente
- Escalabilidad: aumenta o reduce réplicas según demanda
- Distribución: decide en qué máquina corre cada contenedor

## ¿Qué es K3D?

K3D levanta un cluster Kubernetes completo dentro de contenedores Podman/Docker. Ideal para aprender sin necesidad de cloud.

```
Tu Mac
└── Podman VM
    ├── k3d-server-0  (control plane)
    ├── k3d-server-1  (control plane)
    ├── k3d-server-2  (control plane)
    ├── k3d-agent-0   (worker)
    ├── k3d-agent-1   (worker)
    └── k3d-serverlb  (load balancer nginx)
```

## Arquitectura del cluster

### Control Plane (cerebro)
- **API Server** → punto de entrada, recibe todos los comandos kubectl
- **Scheduler** → decide en qué worker corre cada Pod
- **etcd** → base de datos distribuida con el estado del cluster
- **Controller Manager** → vigila que el estado real coincida con el deseado

### Worker Nodes (músculos)
- **kubelet** → agente que recibe órdenes y gestiona contenedores del nodo
- **kube-proxy** → maneja networking del nodo
- **containerd** → runtime que corre los contenedores

## Crear el cluster

```bash
k3d cluster create diplodevops-lab01 --config 01-k3d-setup-lab.yaml --kubeconfig-switch-context
```

El archivo `01-k3d-setup-lab.yaml` configura:
- 3 nodos control plane (modo HA)
- 2 workers
- Puerto 8080 del Mac → puerto 80 del cluster

## Verificar el cluster

```bash
k3d cluster list
kubectl cluster-info
kubectl get nodes -o wide
kubectl get pods -A          # ver todos los pods del sistema
```

## Componentes que K3s instala automáticamente

| Componente | Función |
|-----------|---------|
| `coredns` | DNS interno del cluster |
| `traefik` | Ingress Controller (enruta tráfico HTTP) |
| `metrics-server` | Métricas de CPU y memoria |
| `local-path-provisioner` | Crea PersistentVolumes automáticamente |
| `svclb-traefik` | Load Balancer liviano (uno por nodo) |

## Kubeconfig y contextos

El `--kubeconfig-switch-context` cambia automáticamente el contexto activo. El prompt muestra el contexto actual:

```
k3d-diplodevops-lab01 kube
```

Para trabajar con múltiples clusters:
```bash
k3d kubeconfig write diplodevops-lab01
# genera: $HOME/.k3d/diplodevops-lab01.yaml

alias update-k8s-diplo-01='export KUBECONFIG=$HOME/.k3d/diplodevops-lab01.yaml'
```

## Eliminar el cluster

```bash
k3d cluster delete diplodevops-lab01
```

## Nota sobre puertos

El puerto 8080 del Mac debe estar libre antes de crear el cluster. Si hay contenedores usando ese puerto (ej: docker-compose), bajarlos primero con `podman-compose down`.
