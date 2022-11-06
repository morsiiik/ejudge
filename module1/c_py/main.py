import sys
from collections import deque


class Node:
    def __init__(self, name: str, is_direct: bool):
        self.name_ = name
        self.is_direct_ = is_direct
        self.parents_ = set()

    def set_direct(self):
        self.is_direct_ = True

    def add_parent(self, parent: str):
        self.parents_.add(parent)


def find_ways(lib: str, nodes: dict, stack: deque, visited_table: set):
    if lib not in nodes or lib in visited_table:
        return
    visited_table.add(lib)
    stack.appendleft(lib)
    if nodes[lib].is_direct_:
        print(*stack)
    parents = nodes[lib].parents_
    for parent in parents:
        if parent in visited_table:
            continue
        find_ways(parent, nodes, stack, visited_table)
    visited_table.discard(stack[0])
    stack.popleft()


if __name__ == '__main__':

    vuln = False
    direct = False
    vuln_libs = set()
    nodes = {}
    with open('/home/mors/Downloads/test3.txt') as file:
        for line in file:
            libs = line.split()
            if not libs:
                if not vuln or not direct:
                    break
                continue
            # уязвимые библиотеки
            if not vuln:
                vuln_libs = set(libs.copy())
                nodes = {lib: Node(lib, False) for lib in vuln_libs}
                vuln = True
                continue
            # прямые зависимости
            if not direct:
                for lib in libs:
                    if lib not in nodes:
                        nodes[lib] = Node(lib, True)
                    nodes[lib].set_direct()
                direct = True
                continue
            # остальные зависимости
            for i in range(0, len(libs)):
                if libs[i] not in nodes:
                    nodes[libs[i]] = Node(libs[i], False)
                if i > 0 and libs[i] != libs[0]:
                    nodes[libs[i]].add_parent(libs[0])

    stack = deque()
    visited_table = set()
    for lib in vuln_libs:
        find_ways(lib, nodes, stack, visited_table)
