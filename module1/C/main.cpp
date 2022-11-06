#include <iostream>
#include <string>
#include <unordered_set>
#include <set>
#include <list>
#include <utility>
#include <algorithm>
#include <vector>
#include <sstream>
#include <stack>
#include <fstream>


class Node {
    std::string name_;
    std::unordered_set<std::string> parents_;
    std::vector<std::vector<std::string>> direct_ways;
    bool is_done_ = false;
    bool is_direct_;
public:
    Node() : is_direct_(false) {}

    ~Node() = default;

    Node(Node &&oth) = default;;

    Node &operator=(Node &&oth) = default;

    Node(const Node &) = delete;

    Node &operator=(const Node &oth) = delete;


    explicit Node(std::string name) : name_(std::move(name)), is_direct_(false) {}

    explicit Node(std::string name, bool is_direct) : name_(std::move(name)), is_direct_(is_direct) {}

    void add_parent(const std::string &parent) {
        parents_.insert(parent);
    }

    bool operator==(const Node &oth) const {
        return name_ == oth.name_;
    }

    bool operator!=(const Node &oth) const {
        return !(name_ == oth.name_);
    }

    bool operator<(const Node &oth) const {
        return name_ < oth.name_;
    }

    [[nodiscard]] std::string get_name() const {
        return name_;
    }

    [[nodiscard]] const std::unordered_set<std::string> &get_parents() const {
        return parents_;

    }

    [[nodiscard]] bool is_direct() const {
        return is_direct_;
    }

    bool is_done() const {
        return is_done_;
    }

    void set_direct(bool value) {
        is_direct_ = value;
    }

    void add_direct_way(const std::vector<std::string>& way) {
        direct_ways.push_back(way);
    }

    const std::vector<std::vector<std::string>>& get_direct_ways() const{
        return direct_ways;
    }

    void set_done() {
        is_done_ = true;
    }

};

template<>
class std::hash<Node> {
public:
    size_t operator()(const Node &node) const {
        return std::hash<std::string>{}(node.get_name());
    }
};

std::vector<std::string> split(const std::string &line) {
    std::vector<std::string> result;
    std::stringstream ss(line);
    std::string word;
    while (ss >> word) {
        result.push_back(word);
    }
    return result;
}

void print_stack_and_add_ways(std::stack<std::string> stack, std::unordered_set<Node>& nodes) {
    size_t size = stack.size();
    std::vector<std::string> way;
    for (size_t i = 0; i < size - 1; ++i) {
        std::cout << stack.top() << " ";
        way.push_back(stack.top());
        auto node = nodes.extract(Node(stack.top()));
        auto lib = std::move(node.value());
        lib.add_direct_way(way);
        nodes.insert(std::move(lib));
        stack.pop();
    }
    std::cout << stack.top() << std::endl;
}

void print_stack(std::stack<std::string> stack) {
    size_t size = stack.size();
    for (size_t i = 0; i < size - 1; ++i) {
        std::cout << stack.top() << " ";
        stack.pop();
    }
    std::cout << stack.top() << std::endl;
}

void print_way(const std::vector<std::string>& way) {
    for (auto& pos: way) {
        std::cout << pos <<" ";
    }
}

void find_ways(const std::string &name, std::unordered_set<Node> &nodes,
               std::stack<std::string> &work_stack, std::unordered_set<std::string> &visited) {
    auto it = nodes.find(Node(name));
    if (it == nodes.end()) { return; }

    if (!visited.insert(name).second) { return; }
    work_stack.push(name);

    auto parents = it->get_parents();

    if (it->is_direct()) {
        print_stack_and_add_ways(work_stack, nodes);
    }


    for (auto &parent: parents) {
        if (visited.find(parent) != visited.end()) { continue; }
        if ((it = nodes.find(Node(parent)))->is_done()) {
            auto ways = it->get_direct_ways();
            for (auto& way: ways) {
                print_way(way);
                print_stack(work_stack);
            }
            continue;
        }

        find_ways(parent, nodes, work_stack, visited);
    }

    visited.erase(work_stack.top());
    auto node = nodes.extract(Node(work_stack.top()));
    auto lib = std::move(node.value());
    lib.set_done();
    nodes.insert(std::move(lib));
    work_stack.pop();
}

int main() {

    std::unordered_set<Node> nodes;
    std::string line;
    std::ifstream ss("../test13.txt");
    std::vector<std::string> vuln_libs;
    bool is_vuln = true;
    bool is_direct = false;
    while (getline(ss, line)) {
        auto libs = split(line);
        // заполнение уязвимых библиотек и прямых зависимостей
        if (is_vuln || is_direct) {
            for (auto &pos: libs) {
                Node lib(pos, is_direct);
                auto ins = nodes.insert(std::move(lib));
                if (is_vuln && ins.second) { vuln_libs.push_back(pos); }
                if (!ins.second && is_direct) {
                    auto node = nodes.extract(ins.first);
                    Node new_lib = std::move(node.value());
                    new_lib.set_direct(true);
                    nodes.insert(std::move(new_lib));
                }
            }
            if (is_direct) { is_direct = false; }
            else if (is_vuln) { std::swap(is_vuln, is_direct); }
        }
            // оставшиеся случаи
        else {
            // библиотека
            if (libs.empty()) { continue; }
            Node work_lib(libs.front());
            auto node = nodes.extract(work_lib);
            if (!node.empty()) {
                work_lib = std::move(node.value());
            }
            // ее зависимости

            for (size_t i = 1; i < libs.size(); ++i) {
                if (libs[i] == libs.front()) { continue; }
                Node temp_lib(libs[i]);
                node = nodes.extract(temp_lib);
                if (!node.empty()) {
                    temp_lib = std::move(node.value());
                }

                temp_lib.add_parent(work_lib.get_name());
                nodes.insert(std::move(temp_lib));
            }
            nodes.insert(std::move(work_lib));
        }
    }
    std::stack<std::string> work_stack;
    std::unordered_set<std::string> visited_table;
    for (auto &lib: vuln_libs) {
        find_ways(lib, nodes, work_stack, visited_table);
    }
}
