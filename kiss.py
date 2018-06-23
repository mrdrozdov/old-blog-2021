"""
Keep It Simple Skeleton
"""

import argparse
import json
import os


def read_skeleton(path):
    with open(path) as f:
        data = json.loads(f.read())
    return data


class DAG(object):
    def __init__(self, tasks, strict=True):
        self.dag = self.build_dag(tasks, strict)

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
        bookkeeper = []
        order = []
        edges = {}  # incoming edges.

        # Initialization. Get all nodes with no incoming edges.
        for n in names:
            node = self.dag[n]
            if len(node['depends']) == 0:
                bookkeeper.append(n)
            edges[n] = set(node['depends'])

        # Run topological sort.
        while len(bookkeeper) > 0:
            n = bookkeeper.pop()
            order.append(n)
            node = self.dag[n]
            
            add_to_order = False
            for m in node['parent']:
                __edges = edges[m]
                __edges.remove(n)

                # If no more incoming edges, then extract.
                if len(__edges) == 0:
                    bookkeeper.append(m)

        # Check for cycles.
        for n, incoming in edges.items():
            if len(incoming) > 0:
                raise RuntimeError('Cycle detected.')

        return order

    def run(self):
        for name in self.iterate_over_tasks():
            node = self.dag[name]
            command = node['command']
            self.run_command(command)

    def run_command(self, command):
        os.system(command)


def run(skeleton):
    tasks = skeleton['tasks']
    dag = DAG(tasks)
    dag.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--skeleton', type=str, default='kiss.json')
    options = parser.parse_args()

    skeleton = read_skeleton(options.skeleton)

    run(skeleton)
