from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.finite_automaton import State, Symbol
from pygraphblas import *
import main


def test_intersection_of_graphs():
    graph = main.Graph()
    DFA = main.Graph()

    graph.read_triples("tests/graph_test1.txt")
    automaton.read_regexp("tests/DFA_test1.txt")
    intersection = DFA.intersection(graph)
    
    assert graph.label_matrix["x"] == intersection.label_matrix["x"]

    graph.read_triples("tests/graph_test1.txt")
    DFA.read_regexp("tests/DFA_test2.txt")
    intersection = DFA.intersection(graph)
    
    assert not intersection.label_matrix
    
    graph.read_triples("tests/graph_test2.txt")
    automaton.read_regexp("tests/DFA_test2.txt")
    intersection = DFA.intersection(graph)
    
    assert intersection.num == 14
    
def test_intersection():

    automaton1 = DeterministicFiniteAutomaton()
    automaton2 = DeterministicFiniteAutomaton()
    intersection = DeterministicFiniteAutomaton()

    state0 = State(0)
    state1 = State(1)
    state2 = State(2)

    automaton1.add_start_state(state0)
    automaton2.add_start_state(state0)

    automaton1.add_final_state(state2)
    automaton2.add_final_state(state2)

    symbol0 = Symbol("0")
    symbol1 = Symbol("1")

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