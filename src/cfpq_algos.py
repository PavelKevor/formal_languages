from pyformlang.cfg import CFG, Epsilon, Production, Variable, Terminal
from collections import defaultdict
from pygraphblas import *
from Graph import Graph
from main import *


def tensor(cfgrammar, graph):
    
    if graph.num == 0:
        return False
    rec_automaton = Graph()
   
    heads_set = {}
    num = 0
    for p in cfgrammar.productions:
        if len(p.body) > 0:
            num += len(p.body) + 1
    rec_automaton.num = num
    v = 0
    
    for p in cfgrammar.productions:
        len_of_body = len(p.body)
        if len_of_body > 0:
            rec_automaton.start_states.append(v)
            
            for i in range(len_of_body):
                val = list(p.body)[i].value
                if val not in rec_automaton.label_matrix:
                    bool_matrix= Matrix.sparse(BOOL, rec_automaton.num, rec_automaton.num)
                    bool_matrix[v, v+1] = 1
                    rec_automaton.label_matrix[val] = bool_matrix
                else:
                    rec_automaton.label_matrix[val][v, v+1] = 1
                v += 1
            rec_automaton.final_states.append(v)
            heads_set[v - len_of_body, v] = p.head.value
            v += 1
            
    intersect = Graph()
    if cfgrammar.generate_epsilon():
        graph.label_matrix[cfgrammar.start_symbol.value] += Matrix.identity(BOOL, graph.num)
    tranzitive_closure = intersect.intersection(graph, rec_automaton).tc_with_sqr()
    num = intersect.num
    is_Done = False
    
    while not is_Done:
        nvals = tranzitive_closure.nvals
        for i in range(num):
            for j in range(num):
                if (i, j) in tranzitive_closure:
                    start = i % rec_automaton.num
                    final = j % rec_automaton.num
                    if (start in rec_automaton.start_states) and (final in rec_automaton.final_states):
                        a = i // rec_automaton.num
                        b = j // rec_automaton.num

                        val = heads_set[start, final]
                        if val not in graph.label_matrix:
                            bool_matrix= Matrix.sparse(BOOL, graph.num, graph.num)
                            bool_matrix[a, b] = 1
                            graph.label_matrix[val] = bool_matrix
                        else:
                            graph.label_matrix[val][a, b] = 1
                    
        tranzitive_closure = intersect.intersection(graph, rec_automaton).tc_with_sqr()
        
        if tranzitive_closure.nvals == nvals:
            is_Done = True
    return graph.label_matrix[cfgrammar.start_symbol.value]


def MxM(cfgrammar, graph):
    
    if graph.num == 0:
        return False
    
    output = Graph()
    output.num = graph.num
    output.label_matrix[cfgrammar.start_symbol] = Matrix.sparse(BOOL, output.num, output.num)
    
    term = defaultdict(list)
    for i, s in enumerate(list(map(check_eps, cfgrammar.productions))):
        term[s].append(i)
    term.pop(None)

    if cfgrammar.generate_epsilon():
        output.label_matrix[cfgrammar.start_symbol] += Matrix.identity(BOOL, graph.num)

    
    for i in graph.label_matrix:
        
        T = Terminal(i)
        if T in term:
            for j in range(len(term[T])):
                head = list(cfgrammar.productions)[term[T][j]].head
                
                if head not in output.label_matrix:
                    output.label_matrix[head] = graph.label_matrix[i]
                else:
                    output.label_matrix[head] += graph.label_matrix[i]
                    
    prod_list = []
    for i in cfgrammar.productions:
        if len(i.body) == 2:
            prod_list.append(i)
            
    is_Done = False
    while not is_Done:  
        is_Done = True
        for p in prod_list:
            if (p.head in output.label_matrix) and (list(p.body)[0] in output.label_matrix) and \
                (list(p.body)[1] in output.label_matrix):
                
                nvals = output.label_matrix[p.head].nvals
                with semiring.LOR_LAND_BOOL:
                    output.label_matrix[p.head] += output.label_matrix[list(p.body)[0]] @ \
                                                  output.label_matrix[list(p.body)[1]]
                if output.label_matrix[p.head].nvals != nvals:
                    is_Done = False
                    
    return output.label_matrix[cfgrammar.start_symbol]




def hellings(cfgrammar, graph):
    
    vert_list = []
    if graph.num == 0:
        return False
    
    if cfgrammar.generate_epsilon():
        for i in range(graph.num):
            vert_list += [[cfgrammar.start_symbol, i, i]]
         
    term = defaultdict(list)
    for i, s in enumerate(list(map(check_eps, cfgrammar.productions))):
        term[s].append(i)
    term.pop(None)
    
    
    for label in graph.label_matrix:
        terminal = Terminal(label)
        if terminal in term:
            for k in range(len(term[terminal])):
                h = list(cfgrammar.productions)[term[terminal][k]].head
                for i in range(graph.num):
                    for j in range(graph.num):
                        if (i, j) in graph.label_matrix[label]:
                            vert_list.append([h, i, j])
                            
    prod_list = []
    for i in cfgrammar.productions:
        if len(i.body) == 2:
            prod_list.append(i)

    vert_list_copy = vert_list.copy()
    while vert_list_copy:
        variable_copy, i, j = vert_list_copy.pop()
        for variable, l, k in vert_list:
            if i == k:
                for p in prod_list:
                    if (p.head, l, j) not in vert_list and list(p.body) == [variable, variable_copy]:
                        vert_list_copy.append((p.head, l, j))
                        vert_list.append((p.head, l, j))
            elif j == l:
                for p in prod_list:
                    if (p.head, i, l) not in vert_list and list(p.body) == [variable_copy, variable]:
                        vert_list_copy.append((p.head, i, l))
                        vert_list.append((p.head, i, l))
    
    output = Matrix.sparse(BOOL, graph.num, graph.num)
    for variable, i, j in vert_list:
        if variable == cfgrammar.start_symbol:
            output[i, j] = 1
            
    return output
