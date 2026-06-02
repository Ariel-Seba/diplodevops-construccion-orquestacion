## Construccion y orquestación de contenedores - Clase 3

## Temas a ver:
- Introduccion
- Setup del laboratorio
- Primer despliegue: namespace, pod, service

## 01 - Setup del laboratorio

Para esta materia necesitamos levantar y mantener un cluster k8s donde realizaremos las prácticas. No hay un requisito estricto sobre que cluster levantar. Puede ser:

- Amazon EKS
- Azure AKS
- Digital Ocean k8s (DOKS)
- Minikube
- Microk8s
- Tanzu
- Huawei CCE
- etc

Es a gusto y elección de cada estudiante cual "distribución" utilizará. Incluso, se lo anima a probar distintas distribuciones, para luego poner en común sus experiencias.

Sin embargo, a findes de estandarizar y simplificar el proceso, _oficialmente_ utilizaremos [__K3D__](https://k3d.io/stable/).

Por otra parte, es necesaria la instalación de [kubectl](https://kubernetes.io/docs/tasks/tools/).

Otra herramienta útil será alguna "IDE" para monitorear el estado del cluster, por ejemplo, **lens** o **k9s**. Nuevamente, queda a libre elección del estudiante. Se incentiva a instalar varios y probar con cual se siente mas a gusto. 

Una última recomendación es instalar algún plugin para terminal que facilite el trabajo con K8S, como ser kube-ps1, alias-tip etc.

