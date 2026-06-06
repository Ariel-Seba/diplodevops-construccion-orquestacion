# Ejercicio 3 — Namespace PID: Diagrama de árbol de procesos

## Comando ejecutado

```bash
sudo unshare --pid --fork --mount-proc /bin/bash
```

## Salida desde adentro del namespace

```
UID          PID    PPID  C STIME TTY          TIME CMD
root           1       0  0 12:27 pts/2    00:00:00 /bin/bash
root           8       1  0 12:29 pts/2    00:00:00 sleep 1000
root           9       1  0 12:29 pts/2    00:00:00 ps -ef
```

## Salida desde el host

```
ubuntu      3478    3477  0 12:27 pts/0    00:00:00 -bash
ubuntu      3534    3533  0 12:27 pts/1    00:00:00 -bash
root        3543    3534  0 12:27 pts/1    00:00:00 sudo unshare --pid --fork --mount-proc /bin/bash
root        3544    3543  0 12:27 pts/2    00:00:00 sudo unshare --pid --fork --mount-proc /bin/bash
root        3545    3544  0 12:27 pts/2    00:00:00 unshare --pid --fork --mount-proc /bin/bash
root        3546    3545  0 12:27 pts/2    00:00:00 /bin/bash
root        3553    3546  0 12:29 pts/2    00:00:00 sleep 1000
```

```
pstree -p | grep -E 'unshare|sleep'
sshd(3487)---sshd(3533)---bash(3534)---sudo(3543)---sudo(3544)---unshare(3545)---bash(3546)---sleep(3553)
```

## Diagrama del árbol de procesos

```
HOST (vista global)                              NAMESPACE PID (vista aislada)
═══════════════════════════════════════════      ══════════════════════════

sshd(3487)
 └─ sshd(3533)
      └─ bash(3534)
           └─ sudo(3543)
                └─ sudo(3544)
                     └─ unshare(3545)
                          └─ bash(3546) ─────────────────► /bin/bash   PID 1
                               └─ sleep(3553) ───────────► sleep 1000  PID 8

                                            ╔══════════════════════════════╗
                                            ║  ps -ef (efímero)   PID 9   ║
                                            ╚══════════════════════════════╝

═══════════════════════════════════════════      ══════════════════════════
                                                         ▲
                                              ┌──────────┴──────────┐
                                              │  límite del namespace │
                                              └─────────────────────┘
```

## Tabla de correspondencia de PIDs

| Proceso       | PID en el host | PID adentro del namespace |
|---------------|----------------|--------------------------|
| `/bin/bash`   | 3546           | **1** (se cree PID 1 = init) |
| `sleep 1000`  | 3553           | **8**                    |
| `unshare`     | 3545           | invisible                |
| cadena sshd → sudo | 3487–3544 | invisible               |

## Conclusiones

- Desde adentro, el bash se ve como **PID 1** (equivalente a init/systemd en un sistema real).
- Los procesos **existen** en el kernel con sus PIDs reales — el namespace solo cambia la *vista*.
- El proceso `unshare` y toda la cadena de padres son **invisibles** desde adentro del namespace.
- `--fork` es necesario porque `unshare(CLONE_NEWPID)` no migra el proceso actual al nuevo namespace, solo afecta a sus hijos.
- `--mount-proc` monta un `/proc` propio para que `ps` muestre los PIDs del namespace y no los del host.
