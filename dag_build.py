from cProfile import run
from graphlib import TopologicalSorter

import multiprocessing as mp
import subprocess

from rich.console import Console

def run_task_in_process(task, node, finalized_tasks_queue):
    subprocess.check_call(task, shell=True)
    finalized_tasks_queue.put(node)

if __name__ == '__main__':
    # 1. create the graph
    tasks = {
        "buildir": ["sleep 1 && mkdir -p buildir"],
        "buildir/a": ["sleep 1 && echo 'a' > buildir/a"],
        "buildir/b": ["sleep 1 && echo 'b' > buildir/b"],
        "buildir/c": ["sleep 1 && cat buildir/a buildir/b > buildir/c"],

    }
    graph = {
        "buildir": {},
        "buildir/a": {"buildir"},
        "buildir/b": {"buildir"},
        "buildir/c": {"buildir/a", "buildir/b"},
    }

    topological_sorter = TopologicalSorter(graph)
    task_queue = mp.Queue()
    finalized_tasks_queue = task_queue

    topological_sorter.prepare()

    console = Console(log_time_format="[%X.%f]")
    running_processes = dict()
    while topological_sorter.is_active():
        for node in topological_sorter.get_ready():
            # kick off any ready node
            console.log("Starting task:", node)
            p = mp.Process(target=run_task_in_process, args=(tasks[node], node, finalized_tasks_queue))
            p.start()
            # save it as running
            running_processes[node] = p

        # When the work for a node is done, workers put the node in
        # 'finalized_tasks_queue' so we can get more nodes to work on.
        # The definition of 'is_active()' guarantees that, at this point, at
        # least one node has been placed on 'task_queue' that hasn't yet
        # been passed to 'done()', so this blocking 'get()' must (eventually)
        # succeed.  After calling 'done()', we loop back to call 'get_ready()'
        # again, so put newly freed nodes on 'task_queue' as soon as
        # logically possible.
        node = finalized_tasks_queue.get()
        running_processes.pop(node).join()

        console.log("Finished task:", node)
        topological_sorter.done(node)
