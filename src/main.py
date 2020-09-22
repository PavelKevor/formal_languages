from pygraphblas import *
from pyformlang import *
import sys




class Graph:
    def __init__(self):
        self.start_states = []
        self.final_states = []
        self.label_matrix = {}
        self.num = 0

    def read_triples(self, name):
        self.__init__()
        
        file = open(name, 'r')
        
        if file.read() == '':
            file.close()
            return self
        
        for l in file:
            line = l.split(" ")
            q1 = int(line[0])
            m = line[1]
            q2 = int(line[2])

            self.num = max(max(q1, q2) + 1, self.num)

            if m not in self.label_matrix:
                bool_matrix = Matrix.sparse(BOOL, self.num, self.num)
                bool_matrix[q1, q2] = 1
                self.label_matrix[m] = bool_matrix
            else:
                if self.num > self.label_matrix[m].nrows:
                    self.label_matrix[m].resize(self.num, self.num)
                self.label_matrix[m][q1, q2] = 1

        self.start_states = [i for i in range(self.num)]
        self.final_states = [i for i in range(self.num)]
        file.close()

        return self

    def read_regexp(self, name):
        self.__init__()
       
        file = open(name, 'r')
        
        if file.read() == '':
            print('test')
            file.close()
            return self
        
        DFA = regular_expression.Regex(file.read().rstrip()).to_epsilon_nfa().to_deterministic().minimize()
        file.close()

        states = {}
        for s in DFA._states:
            if s not in states:
                states[s] = len(states)
        self.num = len(states)

        for i in DFA._states:
            for s in DFA._input_symbols:
                for j in DFA._transition_function(i, s):
                    if s in self.label_matrix:
                        self.label_matrix[s][states[i], states[j]] = 1
                    else:
                        bool_matrix = Matrix.sparse(BOOL, self.num, self.num)
                        bool_matrix[states[i], states[j]] = 1
                        self.label_matrix[s] = bool_matrix

        self.start_states.append(states[DFA.start_state])

        for s in DFA._final_states:
            self.final_states.append(states[s])

        return self

    def intersection(self, graph2):
        output = Graph()

        for i in self.label_matrix:
            if i in graph2.label_matrix:
                output.label_matrix[i] = self.label_matrix[i].kronecker(graph2.label_matrix[i])

        output.num = self.num * graph2.num
        for i in self.start_states:
            for j in graph2.start_states:
                output.start_states.append(i * self.num + j)

        for i in self.final_states:
            for j in graph2.final_states:
                output.final_states.append(i * self.num + j)

        return output

    def reach_from_all_pairs(self):
        output = Matrix.random(BOOL, self.num, self.num, 0).full(0)

        for i in self.bool_matrix:
            if self.bool_matrix[i].nrows < self.num:
                self.bool_matrix[i].resize(self.num, self.num)
            output = output | self.bool_matrix[label]

        for i in range(self.num):
            output += output @ output

        return output

    def reach_from_set(self, s):
        output = self.reach_from_all_pairs()

        for i in range(self.num):
            if i not in s:
                output.assign_row(i, Vector.sparse(BOOL, self.num).full(0))

        return output

    def reach_from_set_to_set(self, s1, s2):
        output = self.reach_from_all_pairs()

        for i in range(self.num):
            if i not in s1:
                output.assign_row(i, Vector.sparse(BOOL, self.num).full(0))
            if i not in s2:
                output.assign_col(i, Vector.sparse(BOOL, self.num).full(0))

        return output


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("incorrect input")
    else:
        graph = Graph()
        DFA = Graph()
        graph.read_triples(sys.argv[1])
        DFA.read_regexp(sys.argv[2])
        DFA.intersection(graph)
