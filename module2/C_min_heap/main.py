from sys import stdin, argv


class Heap:
    class Node:
        def __init__(self, key: int, value: str):
            self.key = key
            self.value = value

    def __init__(self):
        self.elements = []
        self.elements_table = {}

    def size(self):
        return len(self.elements)

    @staticmethod
    def parent(i: int) -> int:
        return int((i - 1) / 2)

    @staticmethod
    def left_child(i: int) -> int:
        return 2 * i + 1

    @staticmethod
    def right_child(i: int) -> int:
        return 2 * i + 2

    def __heapify(self, i: int):
        it = i
        while True:
            current = it
            left_child = self.left_child(current)
            right_child = self.right_child(current)
            if left_child < self.size() and self.elements[left_child].key < self.elements[current].key:
                current = left_child
            if right_child < self.size() and self.elements[right_child].key < self.elements[current].key:
                current = right_child
            if current != it:
                self.elements_table[self.elements[it].key] = current
                self.elements_table[self.elements[current].key] = it
                self.elements[it], self.elements[current] = self.elements[current], self.elements[it]
                it = current
            elif it:
                it = self.parent(it)
            else:
                break

    def add(self, key: int, value: str):
        if key in self.elements_table:
            raise RuntimeError
        self.elements.append(Heap.Node(key, value))
        i = self.size() - 1
        parent = self.parent(i)
        while i and self.elements[parent].key > key:
            self.elements[i], self.elements[parent] = self.elements[parent], self.elements[i]
            self.elements_table[self.elements[i].key] = i
            i = parent
            parent = self.parent(i)
        self.elements_table[key] = i

    def set(self, key: int, value: str):
        if key not in self.elements_table:
            raise RuntimeError
        self.elements[self.elements_table[key]].value = value

    def search(self, key: int) -> Node:
        if key in self.elements_table:
            index = self.elements_table[key]
            return self.elements[index]
        return None

    def delete(self, key: int):
        if key not in self.elements_table:
            raise RuntimeError
        index = self.elements_table[key]
        self.elements_table.pop(key)
        if index == self.size() - 1:
            self.elements.pop(-1)
            return
        self.elements[-1], self.elements[index] = self.elements[index], self.elements[-1]
        self.elements_table[self.elements[index].key] = index
        self.elements.pop(-1)
        self.__heapify(index)

    def extract(self):
        if not self.size():
            raise RuntimeError
        key = self.elements[0].key
        value = self.elements[0].value
        self.elements[-1], self.elements[0] = self.elements[0], self.elements[-1]
        self.elements_table[self.elements[0].key] = 0
        self.elements_table.pop(key)
        self.elements.pop(-1)
        self.__heapify(0)
        return Heap.Node(key, value)

    def min(self):
        if self.size():
            return self.elements[0]
        raise RuntimeError

    def max(self):
        if not self.size():
            raise RuntimeError
        if self.size() == 1:
            return self.elements[0]
        parent_index = self.parent(self.size() - 1)
        max_leaf_index = parent_index + 1
        for i in range(max_leaf_index, self.size()):
            if self.elements[max_leaf_index].key < self.elements[i].key:
                max_leaf_index = i
        return self.elements[max_leaf_index]


def Print(heap: Heap):
    if heap.size() == 0:
        print('_')
        return
    level_len = 1
    it = 0
    while it < heap.size():
        for i in range(level_len):
            if it < heap.size():
                node = heap.elements[it]
                if it == 0:
                    print('[{} {}]'.format(node.key, node.value), end='')
                else:
                    parent_key = heap.elements[heap.parent(it)].key
                    if i == 0:
                        print('[{} {} {}]'.format(node.key, node.value, parent_key), end='')
                    else:
                        print(' [{} {} {}]'.format(node.key, node.value, parent_key), end='')
            else:
                print(' _', end='')
            it += 1
        print()
        level_len *= 2


no_arg = {
    'min', 'max', 'print', 'extract'
}

one_arg = {
    'delete', 'search'
}

two_args = {
    'add', 'set'
}


def parse(line: str):
    space_count = line.count(' ')
    split_line = line.split()
    if not split_line:
        return False
    if not split_line:
        return False
    if split_line[0] not in no_arg | one_arg | two_args:
        return False, None
    if split_line[0] in no_arg and space_count != 0:
        return False, None
    if split_line[0] in one_arg and space_count != 1:
        return False, None
    if split_line[0] in two_args and space_count != 2:
        return False, None
    return True, split_line


if __name__ == '__main__':
    heap = Heap()
    instream = stdin
    if len(argv) == 2:
        instream = open(argv[1])
    for line in instream:
        line = line.replace('\n', '')
        if not line:
            continue
        success, command = parse(line)
        if not success:
            print('error')
            continue
        try:
            if command[0] == 'min':
                result = heap.min()
                print(result.key, 0, result.value)
            elif command[0] == 'max':
                result = heap.max()
                print(result.key, heap.elements_table[result.key], result.value)
            elif command[0] == 'extract':
                result = heap.extract()
                print(result.key, result.value)
            elif command[0] == 'print':
                Print(heap)
            else:
                command[1] = int(command[1])
            if command[0] == 'add':
                value = ''
                if len(command) == 3:
                    value = command[2]
                result = heap.add(command[1], value)
            elif command[0] == 'set':
                value = ''
                if len(command) == 3:
                    value = command[2]
                heap.set(command[1], value)
            elif command[0] == 'delete':
                heap.delete(command[1])
            elif command[0] == 'search':
                result = heap.search(command[1])
                if result:
                    print(1, heap.elements_table[result.key], result.value)
                else:
                    print(0)
        except:
            print('error')
