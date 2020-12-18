from statistics import fmean, variance
from pygraphblas import *
from pyformlang import *
from pyformlang.regular_expression import Regex
import timeit
import argparse
import os
from Graph import Graph


parser = argparse.ArgumentParser()
parser.add_argument(
    '--type', nargs=1,
    choices=['graph', 'regexp'], required=False)
parser.add_argument(
    'files', nargs='+')
args = parser.parse_args()

graph = Graph()
DFA = Graph()
inter = Graph()
closure = Graph()
    
graph.read_triples(args.files[0])
DFA.read_regexp(args.files[1])
inter.intersection(graph, DFA)
        
        

f = open("result.txt", 'a')
    
f.write(str(args.files[1]) + "+" + args.files[0] + "\n", )
time_am = timeit.repeat("inter.intersection(graph, DFA).tc_with_adjacency_matrix()", setup="from __main__ import Graph, inter, graph, DFA", repeat=5, number=1)
    
closure = inter.tc_with_adjacency_matrix()
print(str(args.files[1]),"+", args.files[0],"-", closure.nvals)
medium = round(fmean(time_am), 6)
D = round(variance(time_am, 6))
time_am = [round(t, 6) for t in time_am]
f.write("transitive_closure_with_adjacency_matrix: " + str(time_am) + " " +
            "medium:" +
            str(medium) + " " +
            str(D) + "\n")

time_s = timeit.repeat("inter.intersection(graph, DFA).tc_with_sqr()", setup="from __main__ import Graph, inter, graph, DFA", repeat=5, number=1)
              
closure = inter.tc_with_sqr()
print(closure.nvals)
medium = round(fmean(time_s), 6)
D = round(variance(time_s), 6)
time_s = [round(t, 6) for t in time_s]
f.write("transitive_closure_with_squaring: " + str(time_s) + " " +
            "medium:" +
            str(medium) + " " +
            str(D) + "\n\n")
f.close()
