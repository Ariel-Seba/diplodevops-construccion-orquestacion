## Seguridad

Temas a ver:
- Service account
- Role
- ClusterRole
- ClusterRoleBinding

## Pod list

Para esta sección utilizaremos el proyecto propuesto en la siguiente entrada de blog: https://devoops.blog/kubernetes-pods-extractor

Aplicamos SOLAMENTE los manifiestos 1 y 2, luego intentamos acceder a la app:

~~~
kubectl port-forward service/kubernetes-pods-extractor-service 8080:80 -n kubernetes-pods-extractor
~~~

Para ver el error, podemos consultar los logs:

~~~
kubectl logs kubernetes-pods-extractor-<ID> -n kubernetes-pods-extractor
~~~

Aplicamos el manifiesto 3 e intentamos nuevamente.

## Tarea
Crear un usuario de solo lectura para todos los recursos del cluster. Conectarse al cluster con dicho usuario. Intentar eliminar o modificar recursos, debería ser rechazado.
Ayuda: debe crear los recursos de SA, role y role bindings necesarios y luego configurar un kubeconfig con tokens para autenticar a ese service account.s
Ayuda 2: Puede utilizar el comando "can-i" para verificar accesos. ej: kubectl auth can-i delete pods --as=system:serviceaccount:intro-k8s:viewer-user -n intro-k8s

### Links de ayuda:
- https://medium.com/@fabrizio.sgura/demystifying-kubernetes-read-only-user-creation-a-hands-on-guide-39224d2bc7dd
- https://www.youtube.com/watch?v=iE9Qb8dHqWI