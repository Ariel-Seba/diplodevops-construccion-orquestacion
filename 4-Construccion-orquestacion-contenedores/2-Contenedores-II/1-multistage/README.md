## Multistage builds

En esta sección estudiaremos un poco algunas tecnicas basicas para optimizar nuestras imagenes.
Mas precisamente:

- Definicion de contexto
- dockerignore
- multistage build
- inspeccionando nuestras imagenes con dive

Es importante que de ahora en mas tenga estos conceptos en mente cada vez que construya una imagen. Puede ser un punto a revisar al momento de presentar el trabajo final.

_Pregunta al público, ¿Que es el "contexto" al momento de construir una imagen?_

_¿Cómo acomodaría el contexto en el directorio del proyecto actual?_


## Ejercicio 1: Single stage build

Construimos la imagen con **Dockerfile-single**
~~~
docker build -t go-single -f Dockerfile-single .
~~~


## Ejercicio 2: Multistage build


Similar al caso anterior:

~~~
docker build -t go-multi -f Dockerfile-multistage .
~~~

Inspeccione ambas imágenes creadas.

- ¿Qué concluciones puede sacar?
- ¿Qué ventaja puede ver?
- ¿Se le ocurre alguna desventaja?

## Ejercicio 3: Exploramos con dive

Para esta sección, utilizaremos la herramienta [Dive](https://github.com/wagoodman/dive) para inspeccionar las imágenes.

Una vez instalada, simplemente ejecutar:

~~~
dive <imagen a explorar>
~~~

## Tarea 1

Aplicar los conceptos vistos en esta sección en la aplicación que se dió como tarea la clase anterior (aplicación simple con conexión a BD).

## Challenge 1

Implementar un multistage build donde, en alguna de las etapas, se ejecute alguna etapa de validación intermedia (ej, lint, test estático, etc)