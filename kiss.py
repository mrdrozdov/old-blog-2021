"""
Keep It Simple Skeleton
"""

import argparse
import json
import logging
import subprocess
import sys
import time

# multi-thread
import threading
from queue import Queue


def initialize_logger():
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger


def read_skeleton(path):
    with open(path) as f:
        data = json.loads(f.read())
    return data


class DAG(object):
    def __init__(self, tasks, strict=True):
        self.dag = self.build_dag(tasks, strict)
        self.logger = initialize_logger()

    def build_dag(self, tasks, strict=True):
        dag = {}

        # First pass to get tasks.
        for t in tasks:
            name = t['name']
            depends = t.get('depends', [])
            command = t['command'] if strict else t.get('command')

            if name in dag:
                raise ValueError('The name {} exists more than once.'.format(name))

            dag[name] = dict(depends=depends, command=command, parent=[])

        # Second pass to assign parents.
        for n, node in dag.items():
            for m in node['depends']:
                dag[m]['parent'].append(n)

        return dag

    def iterate_over_tasks(self):
        """
        Uses Kahn's Algorithm for topological sort.

        Depends are incoming edges. Parent are outgoing edges.
        """
        names = self.dag.keys()
        this_batch = []
        edges = {}  # incoming edges.

        # Initialization. Get all nodes with no incoming edges.
        for n in names:
            node = self.dag[n]
            if len(node['depends']) == 0:
                this_batch.append(n)
            edges[n] = set(node['depends'])

        # Run topological sort.
        while True:
            batch = []
            next_batch = []
            while len(this_batch) > 0:
                n = this_batch.pop()
                batch.append(n)
                node = self.dag[n]
                
                add_to_order = False
                for m in node['parent']:
                    __edges = edges[m]
                    __edges.remove(n)

                    # If no more incoming edges, then extract.
                    if len(__edges) == 0:
                        next_batch.append(m)

            # Return the current batch (all tasks within a batch can run in parallel).
            yield batch

            # If no batch is coming next, then exit.
            if len(next_batch) == 0:
                break

            # Assign the next batch.
            this_batch = next_batch

        # Check for cycles.
        for n, incoming in edges.items():
            if len(incoming) > 0:
                raise RuntimeError('Cycle detected.')

    def run(self, n_jobs=4):

        def worker():
            while True:
                # start
                name = q.get()

                # do work
                node = self.dag[name]
                command = node['command']
                self.run_command(command)

                # finish
                q.task_done()

        # Create the queue and thread pool.
        q = Queue()
        for i in range(n_jobs):
             t = threading.Thread(target=worker)
             t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
             t.start()

        for batch in self.iterate_over_tasks():
            for name in batch:
                q.put(name)
            q.join()

    def run_command(self, command):
        start = time.perf_counter()
        completed = subprocess.run(command, shell=True, check=True)
        elapsed = time.perf_counter() - start

        self.logger.debug('Command: {}'.format(command))
        self.logger.debug('ReturnCode: {}, Time: {:.4}'.format(completed.returncode, elapsed))


def run(skeleton):
    tasks = skeleton['tasks']
    dag = DAG(tasks)
    dag.run(n_jobs=options.n_jobs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--skeleton', type=str, default='kiss.json')
    parser.add_argument('--n_jobs', type=int, default=4)
    options = parser.parse_args()

    skeleton = read_skeleton(options.skeleton)

    run(skeleton)
