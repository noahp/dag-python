"""
Very basic DAG-based build system example, just a toy for playing with python's
graphlib.
"""

import multiprocessing as mp
import subprocess
from graphlib import TopologicalSorter

from rich.console import Console


def execute_build(tasksinput, graphinput):
    """run the dag build"""
    topological_sorter = TopologicalSorter(graphinput)
    task_queue = mp.Queue()
    finalized_tasks_queue = task_queue

    console = Console(log_time_format="[%X.%f]")

    # keep track of active multiprocessing Process instances, so they can be
    # .join()'d after completing
    running_processes = {}

    def run_task_in_process(taskcmd, node, finalized_tasks_queue):
        """
        Task executor. Fire off the command in a subprocess and wait for it to
        finish. Once done, put a receipt on the queue.
        """
        subprocess.check_call(taskcmd, shell=True)
        finalized_tasks_queue.put(node)

    # use the topological sorter to execute tasks in the correct sequence
    topological_sorter.prepare()
    while topological_sorter.is_active():
        for node in topological_sorter.get_ready():
            # kick off any ready node
            console.log("Starting task:", node)
            process = mp.Process(
                target=run_task_in_process,
                args=(tasksinput[node]["command"], node, finalized_tasks_queue),
            )
            process.start()
            # save it as running
            running_processes[node] = process

        # wait for any running node to finish. this will block as idle until any
        # task finishes. the topological sorter will properly yield only tasks
        # that are ready as the loop proceeds.
        node = finalized_tasks_queue.get()
        running_processes.pop(node).join()

        console.log("Finished task:", node)

        # mark the node as complete
        topological_sorter.done(node)


if __name__ == "__main__":
    import json
    import sys

    if not sys.stdin.isatty():
        tasks = json.load(sys.stdin)
    else:
        # example tasks + dependencies
        print("Loading example tasks")
        tasks = {
            "buildir": {"command": ["sleep 1 && mkdir -p buildir"], "dependencies": []},
            "buildir/a": {
                "command": ["sleep 1 && echo a > buildir/a"],
                "dependencies": ["buildir"],
            },
            "buildir/b": {
                "command": ["sleep 1 && echo b > buildir/b"],
                "dependencies": ["buildir"],
            },
            "buildir/c": {
                "command": ["sleep 1 && cat buildir/a buildir/b > buildir/c"],
                "dependencies": ["buildir/a", "buildir/b"],
            },
        }
    # build the graph of dependencies
    graph = {}
    for task in tasks:
        graph[task] = tasks[task]["dependencies"]

    execute_build(tasks, graph)
