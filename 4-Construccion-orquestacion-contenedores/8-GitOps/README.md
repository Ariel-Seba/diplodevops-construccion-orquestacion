## Clase 8 - Gitops con ArgoCD

En este práctico aplicaremos lo aprendido en la clase referido a la modalidad GitOps

Comenzamos creando un cluster de pruebas:

```
k3d cluster create diplodevops-lab08 --config 16-k3d-setup-lab.yaml --kubeconfig-switch-context
k3d kubeconfig write diplodevops-lab08

```

Luego, para configurar ArgoCD es muy simple. 
Para instalarlo, creamos un namespace y lo instalamos dentro del mismo con un simple apply:

```
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
````

Una vez arriba, hacemos port forward sobre el service de argocd server. Para iniciar sesión por primera vez, usar user admin, y la password se encuentra dentro del secret `inital-admin-secret`.

Creamos una aplicacion. Tomamos los datos del repositorio, el cual es publico:
Repo URL: https://gitlab.com/diplodevops1/2026/DiploDevOps.git
Ref: HEAD
Path: 4-Construccion-orquestacion-contenedores/8-GitOps/helm/charts

Para este caso no es necesario crear de antemano el namespace ni pedirle a argo que lo cree por nosotros ya que se encuentra como temaplate en el chart. Considerar que no siempre es este el caso.



Para limpiar el cluster:
```
k3d cluster delete diplodevops-lab08
```


## Tarea

- Agregar un ingress para el server.
- Crear credenciales diferentes a las default
- Habiltiar la web terminal https://argo-cd.readthedocs.io/en/latest/operator-manual/web_based_terminal/