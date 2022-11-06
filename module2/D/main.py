from sys import stdin, argv


class Node:
    def __init__(self, string: str, is_word=True):
        self.string = string
        self.children = dict()
        self.is_word = is_word


class Tree:
    def __init__(self):
        self.root: Node = None

    # ищется общее начало двух строк
    def __find_prefix(self, first: str, second: str) -> int:
        i = 0
        while i < len(second) and i < len(first):
            if first[i] != second[i]:
                break
            i += 1
        return i

    def __service_search(self, string: str):
        current_node: Node = self.root
        index = 0
        while current_node.children and index < len(string):
            temp_symbol = string[index]
            if temp_symbol in current_node.children:
                next_node = current_node.children[temp_symbol]
                temp_string = string[index:index + len(next_node.string)]
                if temp_string != next_node.string:
                    # флаг добавления до ноды
                    return True, next_node, index
                current_node = next_node
                index += len(current_node.string)
            else:
                # флаг добавления после ноды
                return False, current_node, index
        if index == len(string) and current_node.is_word:
            # слово найдено
            return None
        return False, current_node, index

    def search(self, string):
        if not self.root:
            return False
        result = self.__service_search(string)
        if result is None:
            return True
        return False

    '''
    Добавление в сжатое префиксное дерево
    Сначала ищется нода до которой, или после которой надо вставить слово
    К примеру при добавлении слова hela необходимо найти общую часть, а после разделить по ней слово
    root -> hello перейдет в root -> hel -> lo
                                       \-> a
    Сложность добавления O(H), H - высота дерева 
    '''

    def add(self, string: str):
        if not string:
            return
        string = string.lower()
        if self.root is None:
            self.root = Node('', False)
            self.root.children[string[0]] = Node(string)
            return
        values = self.__service_search(string)
        if values is None:
            return
        flag = values[0]
        current_node = values[1]
        index = values[2]
        add_string = string[index:]
        if index == len(string):
            current_node.is_word = True
            return
        if not flag and add_string[0] not in current_node.children:
            current_node.children[add_string[0]] = Node(add_string)
            return
        pref_index = self.__find_prefix(add_string, current_node.string)
        joint = add_string[0:pref_index]
        node_from_current = Node(current_node.string[pref_index:], current_node.is_word)
        node_from_current.children = current_node.children
        current_node.children = {current_node.string[pref_index]: node_from_current}
        temp_str = add_string[pref_index:]
        if temp_str:
            node_from_add = Node(temp_str)
            current_node.children[temp_str[0]] = node_from_add
            current_node.is_word = False
        current_node.string = joint

    '''
    Поиск исправлений для слова
    flag - показывает была ли уже ошибка в слове, если ошибок больше одной, ветка обрывается
    word - исходное слово для поиска
    corrected - формирование исправленного слова
    index - указывает на необработанную часть слова
    current_node - нода с текущей строкой для проверки
    found - массив найденных исправлений
    
    Сложность алгоритма O(n*m), где n - длина слова, m - мощность алфавита, но за счет счетчика ошибок большинство из нод не попадает в перебор
    Обращение к детям отдельной ноды происходит по ключу - первый символ строки ноды, сложность O(1) за счет использование хеш таблицы
    '''

    def __lev_for_str(self, flag: bool, word: str, corrected: str, index: int, current_node: Node, found: list):
        node_string = current_node.string
        word_string = word[index: index + len(node_string)]
        # проверяется полное соответсвие строки ноды с частью слова
        if node_string == word_string:
            # если слово закончилось
            if index + len(node_string) == len(word):
                if current_node.is_word:
                    found.append(corrected + node_string)
            # если в слове остался 1 символ, и не было ошибок
            if not flag and index + len(node_string) == len(word) - 1 and current_node.is_word:
                found.append(corrected + node_string)
            # продолжение перебора
            for kid in current_node.children:
                self.__lev_for_str(flag, word, corrected + node_string, index + len(node_string),
                                   current_node.children[kid], found)
            return
        if flag:
            return
        flag = True
        if len(node_string) - len(word_string) > 1:
            return
        pref_index = self.__find_prefix(word_string, node_string)
        # удаление символа из слова
        temp_str = node_string[pref_index + 1:]
        if temp_str == word_string[pref_index: pref_index + len(temp_str)]:
            if index + len(node_string) - 1 == len(word) and current_node.is_word:
                found.append(corrected + node_string)
            for kid in current_node.children:
                self.__lev_for_str(flag, word, corrected + node_string, index + len(node_string) - 1,
                                   current_node.children[kid], found)

        # вставка символа в слово
        temp_str = node_string[pref_index:]
        if temp_str == word[index + pref_index + 1:index + pref_index + 1 + len(temp_str)]:
            if index + len(node_string) + 1 == len(word) and current_node.is_word:
                found.append(corrected + node_string)

            for kid in current_node.children:
                self.__lev_for_str(flag, word, corrected + node_string, index + len(node_string) + 1,
                                   current_node.children[kid], found)

        # замена символа
        if word_string[pref_index + 1:] == node_string[pref_index + 1:]:
            if index + len(node_string) == len(word) and current_node.is_word:
                found.append(corrected + node_string)

            for kid in current_node.children:
                self.__lev_for_str(flag, word, corrected + node_string, index + len(node_string),
                                   current_node.children[kid],
                                   found)

        # транспозиция символов
        ## если ошибка в последнем символе слова
        if index + pref_index == len(word) - 1:
            return
        ## если ошибка в последнем символе ноды, и надо проверить со следующей нодой
        elif pref_index == len(word_string) - 1 and word[index + pref_index + 1] == node_string[pref_index] and word[
            index + pref_index] in current_node.children:
            new_word = word[0:index + pref_index] + word[index + pref_index + 1] + word[index + pref_index] + word[
                                                                                                              index + pref_index + 2:]
            self.__lev_for_str(flag, new_word, corrected + node_string, index + len(node_string),
                               current_node.children[word[index + pref_index]], found)
        ## если ошибка внутри строки ноды
        elif len(word_string) > 1 and pref_index < len(word_string) - 1:
            temp_str = word_string[pref_index + 1] + word_string[pref_index] + word_string[pref_index + 2:]
            if temp_str == node_string[pref_index:]:
                if index + len(node_string) == len(word) and current_node.is_word:
                    found.append(corrected + node_string)
                for kid in current_node.children:
                    self.__lev_for_str(flag, word, corrected + node_string, index + len(node_string),
                                       current_node.children[kid],
                                       found)

    '''
    Проверка нахождения слова в словаре
    Сначала проверяется наличие слова в исходном виде
    А после начинается перебор всех нод
    '''

    def check(self, word):
        if not self.root:
            return False, []
        word = word.lower()
        if self.search(word):
            return True, None
        else:
            found = []
            for key in self.root.children:
                self.__lev_for_str(False, word, '', 0, self.root.children[key], found)
            return False, found


if __name__ == '__main__':
    a = Tree()
    flag = False
    instream = stdin
    if len(argv) == 2:
        instream = open(argv[1])
    count = int(instream.readline())
    for line in instream:
        line = line.replace('\n', '')
        if not line:
            continue
        if count > 0:
            a.add(line)
            count -= 1
        else:
            result = a.check(line)
            print(line, '-', end='')
            if not result[0]:
                solutions = result[1]
                if not solutions:
                    print('?')
                    continue
                print('> ', end='')
                if len(solutions) == 1:
                    print(solutions[0])
                    continue
                solutions = sorted(solutions)
                print(', '.join(solutions))
                continue
            print(' ok')
