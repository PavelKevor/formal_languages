from pyformlang.cfg import Terminal, CFG, Epsilon, Variable, Production
from pygraphblas import *
from collections import *
from Graph import Graph


def read_cfgrammar(name):
    file = open(name, 'r')
    p = []
    for line in file:
        p += [line.split()[0] + " -> " + " ".join(line.split()[1:])]
    file.close()

    return CFG.from_text("\n".join(p))
    


def cnf(cfgrammar):
    if not cfgrammar.generate_epsilon():
        return cfgrammar.to_normal_form()
    
    else:
        cfgrammar = cfgrammar.to_normal_form()
        new_symbol = Variable(cfgrammar.start_symbol.value + "'")
        cfgrammar.productions.add(Production(new_symbol, []))
        
        output = CFG(variables=cfgrammar.variables,
                  start_symbol=new_symbol,
                     terminals=cfgrammar.terminals)
        
        output.variables.add(new_symbol)
        
        for i in cfgrammar.productions:
            if cfgrammar.start_symbol == i.head :
                output.productions.add(Production(new_symbol, i.body))
            output.productions.add(i)
            
        return output
        




def sup(p):
    if not p.body:
        return Epsilon()
    else:
        return list(p.body)[0]
        


def cyk(cfgrammar, w):
    w = w.split()
    length = len(w)
    if length != 0:
        number = len(cfgrammar.variables)
        matrix = [[[0 for _ in range(length)] for _ in range(length)] for _ in range(number)]
        variables = dict(zip(cfgrammar.variables, range(number)))
        
        symbols = defaultdict(list)
        for i, s in enumerate(w):
            symbols[s].append(i)

        
        bodies = defaultdict(list)
        for i, s in enumerate(list(map(sup, cfgrammar.productions))):
            bodies[s].append(i)
       
                              
        for s in w:
            if s == ' ':
                term = Epsilon()
            else:
                term = Terminal(s)
            
            if term in bodies:
                for i in symbols[s]:
                    for j in bodies[term]:
                        matrix[variables[list(cfgrammar.productions)[j].head]][i][i] = 1
        for m in range(1, length):
            for i in range(length - m):
                j = i + m
                for n in range(number):
                    for p in cfgrammar.productions:
                        for k in range(i, j):
                            for key, value in variables.items():
                                if n == value:
                                    h = key
                                    
                            if p.head == h and len(p.body) == 2:
                                matrix[n][i][j] += matrix[variables[list(p.body)[0]]][i][k] * matrix[variables[list(p.body)[1]]][k + 1][j]
                                if matrix[n][i][j]:
                                    break
                        if matrix[n][i][j]:
                            break

    else:
        return cfgrammar.generate_epsilon()
        
    
    return bool(matrix[variables[cfgrammar.start_symbol]][0][length - 1])



def hellings_algo(graph, cfgrammar):
    if graph.num != 0:

        vertices_list = list()
        if cfgrammar.generate_epsilon():
            for i in range(graph.num):
                vertices_list.append([cfgrammar.start_symbol, i, i])

        body = defaultdict(list)
        for i, s in enumerate(list(map(sup, cfgrammar.productions))):
            body[s].append(i)
        
        for label in graph.label_matrix:
            term = Terminal(label)
            if term in body:
                for k in range(len(body[term])):
                    var = list(cfgrammar.productions)[body[term][k]].head
                    for i in range(graph.num):
                        for j in range(graph.num):
                            if graph.label_matrix[label][i, j]:
                                vertices_list.append([var, i, j])
        vertices_list_copy = vertices_list.copy()
        while vertices_list_copy:
            var1, v1, v2 = vertices_list_copy.pop()
            for var2, u1, u2 in vertices_list:
                if u2 == v1:
                    for production in cfgrammar.productions:
                        if list(production.body) == {var2, var1} and (production.head, u1, v2) not in vertices_list:
                            vertices_list_copy.append((production.head, u1, v2))
                            vertices_list.append((production.head, u1, v2))
                elif u1 == v2:
                    for p in cfgrammar.productions:
                        if list(p.body) == {var1, var2} and (p.head, v1, u1) not in vertices_list:
                            vertices_list_copy.append((p.head, v1, u1))
                            
                            vertices_list.append((p.head, v1, u1))
        reach_matrix = Matrix.sparse(BOOL, graph.num, graph.num).full(0)
        for v, i, j in vertices_list:
            if v == cfgrammar.start_symbol:
                reach_matrix[i, j] = 1
        return reach_matrix

    else:
        return False
        
