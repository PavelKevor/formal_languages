from statistics import fmean, variance
from pygraphblas import *
from pyformlang import *
from pyformlang.regular_expression import Regex
import timeit
import argparse
import os
from main import *
from Graph import Graph


parser = argparse.ArgumentParser()
parser.add_argument(
    '--type', nargs=1,
    choices=['graph', 'grammar'], required=False)
parser.add_argument(
    'files', nargs='+')
args = parser.parse_args()

graph = Graph()

graph.read_triples(args.files[0])
cfg = read_cfgrammar(args.files[1])


f = open("result_cfpq.txt", 'a')

print(str(args.files[0]) + "+" + args.files[1] + "\n")
f.write(str(args.files[0]) + "+" + args.files[1] + "\n", )

time_m = timeit.timeit("cfpq_tensor(graph, cfg)", setup="from __main__ import Graph, graph, cfg, cfpq_tensor", number=5)
if time_m > 1000:
    time_m = ''
else:
    time_m = str(round(time_m, 5))
f.write("tensor: " + time_m + "\n")


crf = cfg.to_normal_form()

time_m = timeit.timeit("cfpq_tensor(graph, crf)", setup="from __main__ import Graph, graph, crf, cfpq_tensor", number=5)
if time_m > 1000:
    time_m = ''
else:
    time_m = str(round(time_m, 5))
f.write("tensor+crf:" + time_m + "\n")


time_m = timeit.timeit("cfpq_hellings(graph, crf)", setup="from __main__ import Graph, graph, crf, cfpq_hellings",  number=5)
if time_m > 1000:
    time_m = ''
else:
    time_m = str(round(time_m, 5))
f.write("hellings: " + time_m + "\n")


time_m = timeit.timeit("cfpq_MxM(graph, crf)", setup="from __main__ import Graph, graph, crf, cfpq_MxM",  number=5)
if time_m > 1000:
    time_m = ''
else:
    time_m = str(round(time_m, 5))
f.write("MxM: " + time_m + "\n" + "\n")




f.close()
