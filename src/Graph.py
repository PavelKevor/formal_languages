from pygraphblas import *
from pyformlang import *
from pyformlang.regular_expression import Regex
import os

class Graph:
    def __init__(self):
        self.start_states = []
        self.final_states = []
        self.label_matrix = {}
        self.num = 0

    def read_triples(self, name):
        self.__init__()
        
        if os.path.getsize(name) <= 1:
            return self
        
        file = open(name, 'r')

        edges = []
        
        for l in file:
            line = l.split(" ")
            q1 = int(line[0])
            m = line[1]
            q2 = int(line[2])

            edges.append((q1, m, q2))

            self.num = max(max(q1, q2) + 1, self.num)

        for q1, m, q2 in edges:

            if m not in self.label_matrix:
                self.label_matrix[m] = Matrix.sparse(BOOL, self.num, self.num)
                self.label_matrix[m][q1, q2] = True
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
       
        if os.path.getsize(name) <= 1:
            return self
        
        file = open(name, 'r')
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
                        self.label_matrix[s][states[i], states[j]] = True
                    else:
                        self.label_matrix[s] = Matrix.sparse(BOOL, self.num, self.num)
                        self.label_matrix[s][states[i], states[j]] = True
                        

        self.start_states.append(states[DFA.start_state])

        for s in DFA._final_states:
            self.final_states.append(states[s])

        return self

    def tc_with_sqr(self):
        output = Matrix.sparse(BOOL, self.num, self.num)
        
        for i in self.label_matrix:
            output += self.label_matrix[i]
            
        for i in range(self.num):
            priveous = output.nvals
            with semiring.LOR_LAND_BOOL:
                output += output @ output
            if priveous == output.nvals:
                break
            
        return output

    def tc_with_adjacency_matrix(self):
        output = Matrix.sparse(BOOL, self.num, self.num)
        
        for i in self.label_matrix:
            output = output | self.label_matrix[i]
        adjacency_matrix = output.dup()
        
        for i in range(self.num):
            priveous = output.nvals
            with semiring.LOR_LAND_BOOL:
                output += adjacency_matrix @ output
            if priveous == output.nvals:
                break
            
        return output

    

    def intersection(self, graph1, graph2):
        self.__init__()
        
        for l in graph1.label_matrix:
            if l in graph2.label_matrix:
                self.label_matrix[l] = graph1.label_matrix[l].kronecker(graph2.label_matrix[l])
                
        self.num = graph1.num * graph2.num
        for i in graph1.start_states:
            for j in graph2.start_states:
                self.start_states.append(i * graph1.num + j)
                
        for i in graph1.final_states:
            for j in graph2.final_states:
                self.final_states.append(i * graph1.num + j)
                
        return self

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
