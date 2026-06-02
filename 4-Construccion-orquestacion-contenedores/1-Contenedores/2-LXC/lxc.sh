#! /bin/bash

ROJO='\e[0;31m'
NEGRO='\e[0m'
AZUL='\e[1;34m'
VERDE='\e[1;32m'
AMARILLO='\e[1;33m'

amarillento(){
    echo -e "${AMARILLO}$1${NEGRO}"
}

verdozo(){
    echo -e "${VERDE}$1${NEGRO}"
}

azulado(){
    echo -e "${AZUL}$1${NEGRO}"
}

rojizo(){
    echo -e "${ROJO}$1${NEGRO}"
}

pausa(){
    echo -e "${TEXTO}${VERDE}"
    read -p "Presione alguna tecla para continuar..." -n 1 -s
    echo -e "${NEGRO}"
}

pausa_simple(){
    echo -e "${VERDE}"
    read -p "Presione alguna tecla para continuar..." -n 1 -s
    echo -e "${NEGRO}"
}

TEXTO="
$(amarillento '---- Bienvenido a esta lección breve de LXC ----')

Seguiremos la referencia de la guia oficialaquí:

$(azulado 'https://linuxcontainers.org/lxc/getting-started/')

$( amarillento 'Instalación:')

En Ubuntu, es bastante directo:

$(rojizo 'sudo apt install lxc')

Una vez instalado, puede continuar con este tutorial.

Se recomienda abrir una segunda terminal para interactuar con los contenedores creados.

Cada paso termina con una pausa. Para continuar, persione cualquer tecla.
"

pausa

TEXTO="
Comenzamos creando un contenedor privilegiado. Estos son contenedores creados por $(amarillento 'root'), y ejecutados como $(amarillento 'root').
Estos contenedores son los creados por defecto.

El comando que utilizamos tiene el siguiente formato:

$(rojizo 'lxc-create --name <container-name> --template <image>')

Donde:

- $(amarillento '<container-name>:') Es el nombre que le daremos al contenedor.
- $(amarillento '<image>:') Es la imagen o plantilla base que usaremos. Puede consultar las imagenes disponibles aquí: $(azulado 'https://images.linuxcontainers.org/')

El script ahora ejecutará el siguiente comando: $(verdozo '<-------------------')

$(rojizo 'sudo lxc-create --name DiploDevOps --template download --dist alpine --release 3.22 --arch amd64')
"

pausa
sudo lxc-create --name DiploDevOps --template download -- --dist alpine --release 3.22 --arch amd64
pausa_simple

TEXTO="
Ya hemos creado un contenedor. Ahora resta iniciarlo.
El script ahora ejecutará el siguiente comando: $(verdozo '<-------------------')

$(rojizo 'sudo lxc-start --name DiploDevOps')
"

pausa 
sudo lxc-start --name DiploDevOps
pausa_simple

TEXTO="
Ahora, podemos consultar información sobre el contenedor creado.
El script ahora ejecutará el siguiente comando: $(verdozo '<-------------------')

$(rojizo 'sudo lxc-info --name DiploDevOps')
"

pausa
sudo lxc-info --name DiploDevOps
pausa_simple

TEXTO="
Para listar contenedores, utilize el siguiente comando:
$(amarillento 'sudo lxc-ls --fancy')
"

pausa

TEXTO="
Para ejecutar una shell dentro del contenedor, utilize el siguiente comando:
$(amarillento 'sudo lxc-attach --name DiploDevOps')

Explore un poco el contenedor antes de continuar.
"

pausa

TEXTO="
Podemos ahora detener el contenedor con el siguiente comando:
$(amarillento 'sudo lxc-stop --name DiploDevOps')

Y para reiniciar el contenedor, volvemos a utilizar el comando start:

$(amarillento 'sudo lxc-start --name DiploDevOps')

"
pausa

TEXTO="
Finalmente, para destruir el contenedor es necesario detenerlo primero:

$(amarillento 'lxc-stop --name DiploDevOps')

Y luego lo destruimos con el comando:
$(amarillento 'sudo lxc-destroy --name DiploDevOps')

El script ahora ejecutará los comandos anteriores $(verdozo '<-------------------')
"

pausa
sudo lxc-stop --name DiploDevOps
sudo lxc-destroy --name DiploDevOps
pausa_simple


TEXTO="
Corroboramos que el contenedor se destruyó.
El script ahora ejecutará el siguiente comando: $(verdozo '<-------------------')
$(rojizo 'sudo lxc-ls --fancy')
"
pausa
sudo sudo lxc-ls --fancy
pausa_simple


TEXTO="

---- GRACIAS POR UTILIZAR ESTE MINI TUTORIAL ----

LXC proveé mas características, que escapan al scope de esta materia.
Por otra parte, recordemos que el LXC es un motor de bajo nivel. Por lo tanto, no proveé nativamente
una herramienta para la construcción de las imagenes bases.

Si le interesa el tema, lo invitamos a explorar sobre DISTROBUILDER


$(azulado https://linuxcontainers.org/distrobuilder/docs/latest/tutorials/use/)
"

pausa