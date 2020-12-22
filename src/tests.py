from pyformlang import *
from pygraphblas import *
from Graph import Graph
from main import *



def test_hellings():
    graph = Graph()
    graph.read_triples("tests/graph_test2.txt")

    cfgrammar = read_cfgrammar("tests/grammar_test2.txt")
    cfgrammar = cfgrammar.to_normal_form()
    cfgrammar = cnf(cfgrammar)
    
    #empty graph
    graph.read_triples("tests/graph_test3.txt")
    assert not hellings(cfgrammar, graph)

    #graph with loop
    graph.read_triples("tests/graph_test4.txt")
    assert hellings(cfgrammar, graph).select("==", 1).nvals == 0

    graph.read_triples("tests/graph_test1.txt")
    assert hellings(cfgrammar, graph).select("==", 1).nvals == 0

def test_cyk():
    cfg = read_cfgrammar("tests/grammar_test1.txt")
    cfgrammar = cnf(cfg)
 
    assert cyk(cfgrammar_cnf, "0 0 0")
    assert not cyk(cfgrammar, "0 1 10 11")
    assert not cyk(cfgrammar, "0000000")
    assert not cyk(cfgrammar, "1 1 0")



    
    cfg = read_cfgrammar("tests/grammar_test2.txt")
    cfgrammar = cnf(cfg)
   
    assert cyk(cfgrammar, "1 1 1")
    assert not cyk(cfgrammar, "0 1 10 11")
    assert cyk(cfgrammar, "1 1 0")
    assert not cyk(cfgrammar, "11111111")





def test_intersection_of_graphs():
    graph = Graph()
    DFA = Graph()

    graph.read_triples("tests/graph_test1.txt")
    DFA.read_regexp("tests/DFA_test1.txt")
    intersection = Graph()
    intersection.intersection(DFA, graph)
    
    assert graph.label_matrix["test"] == intersection.label_matrix["test"]

    graph.read_triples("tests/graph_test1.txt")
    DFA.read_regexp("tests/DFA_test2.txt")
    intersection = Graph()
    intersection.intersection(DFA, graph)
    
    assert not intersection.label_matrix
    
    graph.read_triples("tests/graph_test2.txt")
    DFA.read_regexp("tests/DFA_test2.txt")
    intersection = Graph()
    intersection.intersection(DFA, graph)
    
    assert intersection.num == 28
    
    graph.read_triples("tests/graph_test3.txt")
    DFA.read_regexp("tests/DFA_test3.txt")
    intersection = Graph()
    intersection.intersection(DFA, graph)
    
    #empty graph
    graph.read_triples("tests/graph_test3.txt")
    DFA.read_regexp("tests/DFA_test2.txt")
    intersection = Graph()
    intersection.intersection(DFA, graph)
    
    assert intersection.label_matrix == {}
    
    #empty DFA
    graph.read_triples("tests/graph_test2.txt")
    DFA.read_regexp("tests/DFA_test3.txt")
    intersection = Graph()
    intersection.intersection(DFA, graph)
    
    assert intersection.label_matrix == {}
    
    graph.read_triples("tests/graph_test4.txt")
    DFA.read_regexp("tests/DFA_test1.txt")
    intersection = Graph()
    intersection.intersection(DFA, graph)
    
    assert graph.label_matrix["test"] == intersection.label_matrix["test"]

    
def test_intersection():

    automaton1 = finite_automaton.DeterministicFiniteAutomaton()
    automaton2 = finite_automaton.DeterministicFiniteAutomaton()
    intersection = finite_automaton.DeterministicFiniteAutomaton()

    state0 = finite_automaton.State(0)
    state1 = finite_automaton.State(1)
    state2 = finite_automaton.State(2)

    automaton1.add_start_state(state0)
    automaton2.add_start_state(state0)

    automaton1.add_final_state(state2)
    automaton2.add_final_state(state2)

    symbol0 = finite_automaton.Symbol("0")
    symbol1 = finite_automaton.Symbol("1")

    automaton1.add_transition(state0, symbol0, state1)
    automaton1.add_transition(state0, symbol1, state2)
    automaton1.add_transition(state1, symbol0, state0)
    automaton1.add_transition(state1, symbol1, state2)
    automaton1.add_transition(state2, symbol0, state1)
    automaton1.add_transition(state2, symbol1, state0)
    
    automaton2.add_transition(state0, symbol0, state1)
    automaton2.add_transition(state0, symbol1, state1)
    automaton2.add_transition(state1, symbol0, state0)
    automaton2.add_transition(state1, symbol1, state2)
    automaton2.add_transition(state2, symbol0, state0)
    automaton2.add_transition(state2, symbol1, state1)


    intersection = automaton1 & automaton2

    assert intersection.accepts("01")
    assert intersection.accepts("0001")
    assert intersection.accepts("000001")
    assert not intersection.accepts("1")
    assert not intersection.accepts("0101")
    assert not intersection.accepts("101")



def test_of_matrix_multiplication():
    matrix1 = Matrix.from_lists(
        [0, 0, 1, 1],
        [0, 1, 0, 1],
        [1, 2, 0, 3])
    
    matrix2 = Matrix.from_lists(
        [0, 0, 0, 1, 1, 1],
        [0, 1, 2, 0, 1, 2],
        [-5, -2, -3, 4, -1, 0])
    
    answer = Matrix.from_lists(
        [0, 0, 0, 1, 1, 1],
        [0, 1, 2, 0, 1, 2],
        [3, -4, -3, 12, -3, 0])

    res = matrix1 @ matrix2

    assert res.iseq(answer)


