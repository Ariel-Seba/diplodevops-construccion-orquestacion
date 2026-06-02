## SetUp Laboratorio

En este práctico se realizaran los pasos para instalar un cluster local de pruebas utilizando K3d. El objetivo es familiarisarse con las herramientas a utilizar.


## Instalacion k3d

Instrucciones: https://k3d.io/stable/#installation

Utilizando el archivo `01-k3d-setup-lab.yaml` se puede iniciar un cluster:

```
k3d cluster create diplodevops-lab01 --config 01-k3d-setup-lab.yaml --kubeconfig-switch-context
```

Parametros:
 - `diplodevops-lab01`: Nombre del cluster a crear 
 - `--config`: Especifica el archivo de configuracion K3D a usarse para crear el cluster.
 - `--kubeconfig-switch-context`: Luego de crear el cluster cambia el contexto automáticamente a dicho cluster. 

Cuando se trabaja con múltiples clusters, es recomendable generar un archivo *KUBECONFIG* para cada uno.
```
k3d kubeconfig write diplodevops-lab01
```

Este comando nos genera un kubeconfig en `$HOME/.k3d/diplodevops-lab01.yaml`
luego podemos generar un alias como los siguientes:

```
alias update-k8s-diplo-01='export KUBECONFIG=$HOME/.k3d/diplodevops-lab01.yaml'
alias unset-k8s-diplo-01='unset KUBECONFIG'
```

Obtenemos infor del cluster:

```
kubectl cluster-info
kubectl get nodes -o wide
kubectl get pods -A
```

Para eliminar cluster:
```
k3d cluster delete diplodevops-lab01
```

Referencias:
- https://k3d.io/v5.3.0/usage/kubeconfig/
