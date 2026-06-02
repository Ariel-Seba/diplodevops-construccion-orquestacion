## Construccion y orquestación de contenedores - Clase 1

### Setup del laboratorio

Para poder cursar sin problemas esta materia, es necesario:

- Tener acceso al repositorio actual. Para ello, asegúrese de enviarle al profesor su usuario de Gitlab
- Disponer de una cuenta en algun container registry, con posibilidad de tener un repositorio privado.
- Disponer de algún entorno de Kubernetes. 

## Tarea (A usarse en el TP final):

Crear una aplicación simple, en el lenguaje de su preferencia, que realize las siguientes acciones:
- Se conecte a una base de datos
- Pueda realizar consultas para lectura y escritura de datos.
- No se necesita autenticación. Pero si agrega alguna característica relacionada, es un bonus.
- La BD almacena datos simples. A modo de ejemplo, puede ser solo una tabla con los siguientes campos: | Id (pk) | Nombre (string) | Apellido (string) | documento (int) |
- Conteneirizar dicha app. Publicarla en algún registry (preferentemente, privado). 


## Extra

Si bien no es obligatorio, se presenta la siguiente tool que puede complementar su proceso de aprendizaje: 
https://github.com/Manoj-engineer/k8squest