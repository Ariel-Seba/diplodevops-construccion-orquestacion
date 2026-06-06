# Práctico — Primeros manifiestos en Kubernetes

## Declarativo vs Imperativo

**Imperativo** → le decís al sistema qué hacer:
```bash
kubectl run mi-pod --image=nginx
```

**Declarativo** → describís el estado deseado en YAML:
```bash
kubectl apply -f manifiesto.yaml
```

En producción siempre se usa el enfoque declarativo — los archivos YAML son la fuente de verdad, versionables en git. K8s se encarga de llegar al estado descrito: si el recurso no existe lo crea, si ya existe lo actualiza, si murió lo recrea.

---

## Estructura base de un manifiesto

```yaml
apiVersion: apps/v1   # versión de la API de K8s
kind: Deployment      # tipo de objeto
metadata:
  name: mi-app        # nombre único en el namespace
  namespace: default  # namespace donde vive
  labels:             # etiquetas clave:valor
    app: mi-app
spec:                 # estado deseado
  ...
```

---

## Ejercicio — Namespace + Pod + Service

### 1. Crear el Namespace

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: intro-k8s
  labels:
    name: intro-k8s-namespace
```

```bash
kubectl apply -f k8s/1-namespace.yaml
kubectl get namespaces
```

### 2. Crear el Pod y el Service

```yaml
# Pod
apiVersion: v1
kind: Pod
metadata:
  name: app-saludo-pod
  namespace: intro-k8s
  labels:
    app: app-saludo       # el Service usa este label para encontrar el Pod
spec:
  containers:
    - name: app-saludo
      image: matiops/intro-k8s:app-saludo
      ports:
        - containerPort: 8000
      resources:
        requests:
          memory: "64Mi"
          cpu: "100m"     # 100 milicores = 0.1 CPU
        limits:
          memory: "128Mi"
          cpu: "150m"
---
# Service
apiVersion: v1
kind: Service
metadata:
  name: app-saludo-service
  namespace: intro-k8s
spec:
  type: NodePort
  ports:
    - port: 8081          # puerto del Service en el cluster
      targetPort: 8000    # puerto del contenedor
  selector:
    app: app-saludo       # conecta con Pods que tengan este label
```

```bash
kubectl apply -f k8s/2-app-saludo.yaml
kubectl get pods -n intro-k8s
kubectl get services -n intro-k8s
```

### Flujo de tráfico

```
Mac:8080 → k3d loadbalancer → nodo:30277 → Service:8081 → Pod:8000
```

```bash
curl http://localhost:8080   # → "It works!"
```

---

## kubectl describe — Anatomía de un Pod

```bash
kubectl describe pod app-saludo-pod -n intro-k8s
```

Campos importantes:

| Campo | Significado |
|-------|-------------|
| `Node` | En qué worker cayó el Pod (elige el Scheduler) |
| `IP` | IP dinámica del Pod dentro del cluster |
| `Requests/Limits` | Recursos garantizados vs máximos |
| `QoS Class: Burstable` | requests < limits → prioridad media |
| `Events` | Historia completa: Scheduled → Pulling → Pulled → Created → Started |

### QoS Classes

| Clase | Condición | Prioridad |
|-------|-----------|-----------|
| `Guaranteed` | requests == limits | Alta (nunca se mata primero) |
| `Burstable` | requests < limits | Media |
| `BestEffort` | sin requests ni limits | Baja (se mata primero) |

### Volumen automático inyectado

K8s inyecta en todo Pod un token de acceso a la API y el certificado del cluster:
```
kube-api-access-xxxxx (Projected volume)
```
Permite que el contenedor se comunique con la API de K8s si lo necesita.

---

## Comandos útiles

```bash
# Ver recursos de un namespace
kubectl get all -n intro-k8s

# Ver logs del Pod
kubectl logs app-saludo-pod -n intro-k8s

# Entrar al contenedor
kubectl exec -it app-saludo-pod -n intro-k8s -- sh

# Eliminar recursos
kubectl delete -f k8s/2-app-saludo.yaml
kubectl delete -f k8s/1-namespace.yaml
```
