# Clase 5 - Helm

En esta sección haremos una introducción al administrador de paquetes "helm"
Antes de comenzar, deje instalado el namespace de "intro-k8s"

## Caja de herramientas

- helm lint ./mi-chart: : Verifica que la estructura del chart sea correcta según el estándar.
- helm template ./mi-chart: Muestra en pantalla el YAML final resultante de mezclar tus templates con tus values.yaml. Es ideal para entender qué está pasando "bajo el capó".
- helm install mi-release ./mi-chart --dry-run --debug: Simula la instalación en el cluster y te muestra exactamente qué se enviaría a la API de Kubernetes.
- helm install mi-app-saludo ./mi-chart -n intro-k8s --create-namespace: La instalación real.
- helm list -A: Muestra todas las "Releases" (instancias de charts) instaladas.
- helm status mi-app-saludo: Da información sobre los recursos creados.
- helm upgrade mi-app-saludo ./mi-chart --set replicaCount=3: Enseña cómo cambiar valores sobre la marcha sin editar el archivo.
- helm package ./mi-chart. Esto genera un archivo .tgz que es el artefacto real que se distribuye.

Tenga en cuenta que en la práctica no se suele trabajar con archivos locales. Se registran repositorios y sobre los mismos se hacen push/pull de los paquetes. Se deja para que practiquen esos pasos de tareas, y hagan las consultas necesarias en discord.

### Tarea 1

"Helmificar" los manifiestos de el trabajo final. Hacer push del artifact a un repo de helm compatible

### Tarea 2

En su repo de git, agregar algun mecanismo para validar que los archivos de helm que se estan cargando sean validos. (ej, un precommit hook que aplique el comando "helm template")

### Tarea 3
Explorar alguna aplicación que esté empaquetada en helm, instalarla, probarla, hacer upgrade/rollback y desinstalarla. (Ej: wordpress, grafana, etc)