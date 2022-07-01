# dag-python (Directed Acyclic Graph) build testing

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
