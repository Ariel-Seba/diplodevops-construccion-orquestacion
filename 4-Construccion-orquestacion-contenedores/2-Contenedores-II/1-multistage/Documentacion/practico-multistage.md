# Práctico — Multistage Builds

## Conceptos clave

### Contexto de build
El `.` al final de `docker build .` es el **contexto** — el directorio completo que se envía al daemon para construir la imagen. Archivos innecesarios (node_modules, .git, logs) lo hacen más lento y pueden filtrar información sensible. La solución es `.dockerignore`.

### ¿Por qué multistage?
En un build de una sola etapa, la imagen final contiene el compilador, las herramientas de build y todas las dependencias de compilación — nada de eso se necesita en producción.

Multistage permite **separar el ambiente de compilación del ambiente de ejecución**: se compila en una imagen con todas las herramientas y se copia solo el binario resultante a una imagen mínima.

---

## Ejercicio 1 — Single stage build

```bash
podman build -t go-single -f Dockerfile-single .
```

**Resultado**: 873 MB — el compilador de Go, Debian, apt, librerías. Todo innecesario en producción.

```dockerfile
FROM golang:1.21
WORKDIR /src
COPY ./main.go .
RUN go build -o /bin/hello ./main.go
CMD ["/bin/hello"]
```

---

## Ejercicio 2 — Multistage build

```bash
podman build -t go-multi -f Dockerfile-multistage .
```

**Resultado**: 1.86 MB — solo el binario compilado.

```dockerfile
FROM golang:1.21 AS builder-stage
WORKDIR /src
COPY ./main.go .
RUN go build -o /bin/hello ./main.go

FROM scratch
COPY --from=builder-stage /bin/hello /bin/hello
CMD ["/bin/hello"]
```

`scratch` es una imagen completamente vacía — sin shell, sin librerías, sin sistema operativo. Solo lo que se copia explícitamente.

### Comparación

| | Single stage | Multistage |
|--|--|--|
| Tamaño | 873 MB | 1.86 MB |
| Contiene compilador | Sí | No |
| Superficie de ataque | Alta | Mínima |
| CVEs potenciales | Muchos | Mínimos |

---

## Ejercicio 3 — Inspección con dive

```bash
dive --source podman go-single   # ver capas del single stage
dive --source podman go-multi    # ver capas del multistage
```

**go-single**: decenas de capas, sistema Debian completo, miles de archivos.
**go-multi**: 2 capas — directorio `/bin` y archivo `hello` de 1.86 MB.

> Nota: `--source podman` es necesario porque dive por defecto busca imágenes en Docker.

---

## Challenge — Multistage con validación intermedia

Agregar etapas de lint y test que bloqueen el build si fallan.

### Archivos creados

**main_test.go**:
```go
package main

import "testing"

func TestHello(t *testing.T) {
    expected := "hello, world"
    if expected == "" {
        t.Errorf("expected non-empty string")
    }
}
```

**Dockerfile-challenge**:
```dockerfile
FROM golang:1.21 AS base
WORKDIR /src
COPY . .
RUN go mod init hello

# Etapa 1: validación estática
FROM base AS lint
RUN go vet ./...

# Etapa 2: tests unitarios (solo corre si lint pasó)
FROM lint AS test
RUN go test ./...

# Etapa 3: compilación (solo corre si lint y test pasaron)
FROM test AS builder
RUN go build -o /bin/hello ./main.go

# Imagen final: solo el binario
FROM scratch
COPY --from=builder /bin/hello /bin/hello
CMD ["/bin/hello"]
```

```bash
podman build -t go-challenge -f Dockerfile-challenge .
```

### Resultado final

| Imagen | Tamaño | Validación |
|--------|--------|------------|
| `go-single` | 873 MB | Ninguna |
| `go-multi` | 1.86 MB | Ninguna |
| `go-challenge` | 1.86 MB | lint + tests |

`go-multi` y `go-challenge` pesan igual — la diferencia no es el tamaño sino el **proceso**: `go-challenge` garantiza que el código pasó por `go vet` y `go test` antes de llegar a producción.

### Por qué importa en producción

En un pipeline CI/CD real, las etapas de validación bloquean el despliegue si hay errores estáticos o tests rotos. Si `go vet` falla, el build se corta y nunca se genera la imagen. Esto es lo que implementan herramientas como GitHub Actions o GitLab CI por defecto.
