from sys import stdin, argv



class SplaySet:
    class Node:
        def __init__(self, key, value=None, parent=None, left_child=None, right_child=None):
            self.key_ = key
            self.value_ = value
            self.parent_: SplaySet.Node = parent
            self.left_child_: SplaySet.Node = left_child
            self.right_child_: SplaySet.Node = right_child

        def set_parent(self, parent):
            self.parent_ = parent

    def __init__(self, root=None):
        self.root_ = root

    def __find_max(self, v: Node):
        temp = v
        while temp.right_child_ is not None:
            temp = temp.right_child_
        return temp

    def __find_min(self, v: Node):
        temp = v
        while temp.left_child_ is not None:
            temp = temp.left_child_
        return temp

    def __rotation(self, parent: Node, child: Node):
        grandparent = parent.parent_
        if grandparent is not None:
            if grandparent.left_child_ == parent:
                grandparent.left_child_ = child
            else:
                grandparent.right_child_ = child
        if parent.left_child_ == child:
            parent.left_child_, child.right_child_ = child.right_child_, parent
        else:
            parent.right_child_, child.left_child_ = child.left_child_, parent
        child.parent_ = grandparent

        if child.left_child_ is not None:
            child.left_child_.set_parent(child)
        if child.right_child_ is not None:
            child.right_child_.set_parent(child)
        if parent.left_child_ is not None:
            parent.left_child_.set_parent(parent)
        if parent.right_child_ is not None:
            parent.right_child_.set_parent(parent)

    def __splay(self, node: Node):
        while node.parent_ is not None:
            parent: SplaySet.Node = node.parent_
            grandparent = parent.parent_
            if grandparent is None:
                self.__rotation(parent, node)
                return node
            one_direct = (grandparent.left_child_ == parent) == (parent.left_child_ == node)
            if one_direct:
                self.__rotation(grandparent, parent)
                self.__rotation(parent, node)
            else:
                self.__rotation(parent, node)
                self.__rotation(grandparent, node)
        return node

    def find(self, key):
        success, node = self.__not_splay_find(key)
        if node is not None:
            self.__splay(node)
            self.root_ = node
        return success, node

    def __not_splay_find(self, key):
        current_v: SplaySet.Node = self.root_
        while current_v is not None and current_v.key_ != key:
            if key > current_v.key_:
                if current_v.right_child_ is None:
                    return False, current_v
                current_v = current_v.right_child_
            else:
                if current_v.left_child_ is None:
                    return False, current_v
                current_v = current_v.left_child_
        if current_v is not None:
            return True, current_v
        return False, None

    def set(self, key, value):
        success, node = self.find(key)
        if not success:
            return False
        node.value_ = value
        return True

    def insert(self, key, value):
        success, node = self.__not_splay_find(key)
        if success:
            self.__splay(node)
            self.root_ = node
            return False
        if node is None:
            self.root_ = SplaySet.Node(key, value)
            return True
        new_node = SplaySet.Node(key, value, node)
        if key > node.key_:
            node.right_child_ = new_node
        else:
            node.left_child_ = new_node
        self.__splay(new_node)
        self.root_ = new_node
        return True

    def remove(self, key):
        success, node = self.find(key)
        if not success:
            return False
        if node.left_child_ is not None:
            right_tree = node.right_child_
            left_tree = node.left_child_
            left_tree.parent_ = None
            if right_tree is not None:
                max_left = self.__find_max(node.left_child_)
                self.__splay(max_left)
                self.root_ = max_left
                max_left.right_child_ = right_tree
                right_tree.parent_ = max_left
            else:
                self.root_ = left_tree
        elif node.right_child_ is not None:
            node.right_child_.parent_ = None
            self.root_ = node.right_child_
            node.right_child = None
        else:
            self.root_ = None
        return True

    def max(self):
        node = self.__find_max(self.root_)
        self.__splay(node)
        self.root_ = node
        return node

    def min(self):
        node = self.__find_min(self.root_)
        self.__splay(node)
        self.root_ = node
        return node

    def empty(self):
        return self.root_ is None


def print_set(set: SplaySet):
    if set.root_ is None:
        print('_')
        return
    cur_level_len = 1
    cur_level_nodes = {0: set.root_}
    next_level_nodes = dict()
    flag = True
    while flag:
        flag = False
        for i in range(cur_level_len):
            node = None
            if i in cur_level_nodes:
                node = cur_level_nodes.pop(i)
            if node is not None:
                if node == set.root_:
                    print('[{} {}]'.format(node.key_, node.value_), end='')
                else:
                    if i != 0:
                        print(' [{} {} {}]'.format(node.key_, node.value_, node.parent_.key_), end='')
                    else:
                        print('[{} {} {}]'.format(node.key_, node.value_, node.parent_.key_), end='')
                if node.right_child_ is not None:
                    next_level_nodes[i * 2 + 1] = node.right_child_
                    flag = True
                if node.left_child_ is not None:
                    next_level_nodes[i * 2] = node.left_child_
                    flag = True
            else:
                if i != 0:
                    print(' _', end='')
                else:
                    print('_', end='')
        print()
        cur_level_len *= 2
        cur_level_nodes = next_level_nodes
        next_level_nodes = dict()


no_arg = {
    'min', 'max', 'print'
}

one_arg = {
    'delete', 'search'
}

two_args = {
    'add', 'set'
}


def parse(line: str):
    space_count = line.count(' ')
    line = line.replace('\n', '')
    if not line:
        return False
    split_line = line.split()
    if not split_line:
        return False
    if split_line[0] not in no_arg | one_arg | two_args:
        return False, None
    if split_line[0] in no_arg and (len(split_line) != 1 or space_count != 0):
        return False, None
    if split_line[0] in one_arg and (len(split_line) != 2 or space_count != 1):
        return False, None
    if split_line[0] in two_args and space_count != 2:
        return False, None
    return True, split_line


if __name__ == '__main__':
    set = SplaySet()
    instream = stdin
    if len(argv) == 2:
        instream = open(argv[1])
    for line in instream:
        success, command = parse(line)
        if not success:
            print('error')
            continue
        if (command[0] == 'min' or command[0] == 'max') and set.empty():
            success = False
        elif command[0] == 'add':
            try:
                command[1] = int(command[1])
            except ValueError:
                print('error')
                continue
            value = ''
            if len(command) == 3:
                value = command[2]
            success = set.insert(command[1], value)
        elif command[0] == 'set':
            try:
                command[1] = int(command[1])
            except ValueError:
                print('error')
                continue
            value = ''
            if len(command) == 3:
                value = command[2]
            success = set.set(command[1], value)

        elif command[0] == 'delete':
            try:
                command[1] = int(command[1])
            except ValueError:
                print('error')
                continue
            success = set.remove(command[1])
        elif command[0] == 'search':
            try:
                command[1] = int(command[1])
            except ValueError:
                print('error')
                continue
            success, node = set.find(command[1])
            if success:
                print(1, node.value_)
            else:
                print(0)
                continue
        elif command[0] == 'min':
            node = set.min()
            print(node.key_, node.value_)

        elif command[0] == 'max':
            node = set.max()
            print(node.key_, node.value_)

        else:
            print_set(set)
            success = True

        if not success:
            print('error')
