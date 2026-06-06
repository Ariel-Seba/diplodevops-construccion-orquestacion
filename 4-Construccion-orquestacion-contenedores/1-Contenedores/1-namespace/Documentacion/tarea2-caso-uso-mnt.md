# Tarea 2 — Caso de uso real del namespace MNT

## El escenario: servidor de CI/CD con múltiples jobs en paralelo

Imaginá una plataforma tipo GitHub Actions o Jenkins corriendo en un solo servidor Linux. Cuando un desarrollador hace push, se disparan 3 jobs al mismo tiempo:

- **Job A** — deploy de la app de pagos (tiene credenciales de la base de datos de producción)
- **Job B** — deploy de la app de usuarios (tiene un token de API de Stripe)
- **Job C** — tests de integración (no debería ver ninguna credencial de prod)

Cada job necesita montar sus secretos en `/run/secrets/` para que la app los lea.

## Sin namespace MNT — el problema

```
/run/secrets/db_password     ← Job A lo montó
/run/secrets/stripe_token    ← Job B lo montó
```

Los tres jobs comparten el mismo filesystem. Job C puede leer `db_password` aunque no debería. Un bug en Job C o código malicioso en una dependencia puede filtrar credenciales de producción.

## Con namespace MNT — la solución

Cada job corre dentro de su propio namespace MNT:

```
Namespace de Job A:          Namespace de Job B:          Namespace de Job C:
/run/secrets/db_password     /run/secrets/stripe_token    /run/secrets/   (vacío)
```

El montaje de Job A es **invisible** para Job B y Job C. Comparten el mismo kernel, pero cada uno ve solo su propia vista del filesystem.

## Conexión con contenedores

Esto es exactamente lo que hacen Docker y Kubernetes cuando montás un Secret como volumen en un Pod — cada Pod tiene su namespace MNT propio. El Secret aparece como un archivo dentro del contenedor, pero es invisible para cualquier otro contenedor del mismo nodo.
