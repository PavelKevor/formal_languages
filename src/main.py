from pyformlang.cfg import Terminal, CFG, Epsilon, Variable, Production
from pyformlang.regular_expression import Regex
from pygraphblas import *
from collections import *
from Graph import Graph



def read_cfgrammar(name):
    file = open(name, 'r')

    s = ''
    cfg_from_regex = []
    for line in file:
        if 'regexp'  in line:
            line = line.replace('regexp', "")
            head = line.split(" -> ")[0]
            regex = Regex(line.split(" -> ")[1][:-1])
            cfg_from_regex.append(regex.to_cfg(starting_symbol=head))           
        else:
            s += line
            
    file.close()
    cfg = CFG.from_text(s)

    for c in cfg_from_regex:
        cfg = CFG(cfg.variables.union(c.variables), cfg.terminals.union(c.terminals), cfg.start_symbol, cfg.productions.union(c.productions))

    
    return cfg



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
        


def check_eps(p):
    if p.body:
        if len(p.body) == 1:
            return list(p.body)[0]
    else:
        return Epsilon()
        

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

