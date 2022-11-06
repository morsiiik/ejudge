#include <iostream>
#include <vector>
#include <set>

class Deque {
    std::string* deque;
    size_t head;
    size_t tail;
    size_t size;
    size_t capacity;
public:
    Deque() : deque(nullptr), head(0), tail(0), size(0), capacity(0) {}

    ~Deque() {
        delete[] deque;
    }

    void set_size(size_t new_size) {
        capacity = new_size;
        deque = new std::string [new_size];
    }


    void push_front(const std::string &element) {
        if (size == capacity) {
            std::cout << "overflow" << std::endl;
            return;
        }
        if (size != 0) {
            if (head == 0) {
                head = capacity;
            }
            --head;
        }
        deque[head] = element;
        ++size;
    }

    void push_back(const std::string &element) {
        if (size == capacity) {
            std::cout << "overflow" << std::endl;
            return;
        }
        if (size != 0) {
            ++tail;
            if (tail == capacity) {
                tail = 0;
            }
        }
        deque[tail] = element;
        ++size;
    }

    std::string pop_front() {
        if (size == 0) {
            return "underflow";
        }
        std::string element = deque[head];
        ++head;
        if (head == capacity) {
            head = 0;
        }
        --size;
        if (size == 0) {
            head = 0;
            tail = 0;
        }
        return element;
    }

    std::string pop_back() {
        if (size == 0) {
            return "underflow";
        }
        std::string element = deque[tail];
        if (tail == 0) {
            tail = capacity;
        }
        --tail;
        --size;
        if (size == 0) {
            head = 0;
            tail = 0;
        }
        return element;
    }

    void print() {

        if (size == 0) {
            std::cout <<"empty"<<std::endl;
            return;
        }
        for (int i = head; i != tail; ++i) {
            if (i == capacity) {
                i = -1;
                continue;
            }
            std::cout << deque[i] << " "; // ?
        }
        std::cout << deque[tail] << std::endl;
    }

};


std::vector<std::string> split(std::string const &str) {
    size_t start=0;
    size_t end = 0;
    std::vector<std::string> result;
    std::string word;
    while (end != std::string::npos)
    {
        end = str.find(' ', start);
        word = str.substr(start, end - start);
        if (word.empty()) { return {}; }
        result.push_back(word);
        start = end+1;
    }
    return result;
}



int main() {
    std::set<std::string> commands_arg = {"set_size", "pushb", "pushf"};
    std::set<std::string> commands_noarg = {"popf", "popb", "print"};
    bool set_flag = false;
    std::string line;
    Deque deque;

    while (getline(std::cin, line)) {
        if (line.empty()) {
            continue;
        }

        auto temp = split(line);
        if (temp.empty() || temp.size() > 2) { std::cout << "error"<<std::endl; continue;}
        std::string command = temp[0];
        if (!set_flag && command != "set_size") { std::cout << "error" << std::endl; continue; }
        if (commands_arg.find(command) != commands_arg.end() && temp.size() == 2) {
            auto arg = temp[1];
            if (command == "set_size") {
                int num = 0;
                try {
                    num = std::stoi(arg);
                }
                catch (std::exception &) {}
                if (num <= 0 || set_flag) {
                    std::cout << "error" << std::endl;
                    continue;
                }
                deque.set_size(num);
                set_flag = true;
            } else if (command == "pushb") {
                deque.push_back(arg);
            } else {
                deque.push_front(arg);
            }

        } else if (commands_noarg.find(command) != commands_noarg.end() && temp.size() == 1) {
            if (command == "popf") {
                std::cout << deque.pop_front() << std::endl;
            } else if (command == "popb") {
                std::cout << deque.pop_back() << std::endl;
            } else {
                deque.print();
            }
        } else {
            std::cout << "error" << std::endl;
        }
    }
}
