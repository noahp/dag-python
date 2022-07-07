# ➿ dag-python (Directed Acyclic Graph) build testing

Using some python 3.9 features to run subprocesses as a build system would, with
dependencies sequenced correctly and parallelized.

```bash
❯ python dag_build.py
[20:56:49.046796] Starting task: buildir
[20:56:50.053453] Finished task: buildir
[20:56:50.054476] Starting task: buildir/a
[20:56:50.055784] Starting task: buildir/b
[20:56:51.060096] Finished task: buildir/a
[20:56:51.062647] Finished task: buildir/b
[20:56:51.063199] Starting task: buildir/c
[20:56:52.069040] Finished task: buildir/c
```

Also can be run by feeding a JSON build spec into stdin:

```bash
❯ echo '{
    "buildir": {"command": ["sleep 1 && mkdir -p buildir"], "dependencies": []},
    "buildir/a": {
        "command": ["sleep 1 && echo a > buildir/a"],
        "dependencies": ["buildir"]
    },
    "buildir/b": {
        "command": ["sleep 1 && echo b > buildir/b"],
        "dependencies": ["buildir"]
    },
    "buildir/c": {
        "command": ["sleep 1 && cat buildir/a buildir/b > buildir/c"],
        "dependencies": ["buildir/a", "buildir/b"]
    },
    "buildir/d": {
        "command": ["sleep 1 && cat buildir/a buildir/b buildir/c > buildir/d"],
        "dependencies": ["buildir/a", "buildir/b", "buildir/c"]
    }
}' | python dag_build.py
[09:59:23.354110] Starting task: buildir
[09:59:24.359827] Finished task: buildir
[09:59:24.360741] Starting task: buildir/a
[09:59:24.362059] Starting task: buildir/b
[09:59:25.365812] Finished task: buildir/a
[09:59:25.367038] Finished task: buildir/b
[09:59:25.367634] Starting task: buildir/c
[09:59:26.373345] Finished task: buildir/c
[09:59:26.374327] Starting task: buildir/d
[09:59:27.379334] Finished task: buildir/d
```
