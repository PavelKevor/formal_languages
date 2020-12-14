from main import *
from Graph import *

keywords = [
    'connect', 'select', 'from',
    '{', '}', 'alt', 'option',
    'plus', 'star', '(', ')']


def check_syntax_with_cyk(script):
    grammar = read_cfgrammar('language_grammar.txt')
    converted_script = []
    for i in script.split():
        if i in keywords:
            converted_script.append(w)
        else:
            converted_script.extend(w)

    return cyk(grammar, converted_script)

def test_check_syntax():
    
    script = "connect '/home/fl/graphs'"
    assert check_syntax_with_cyk(script)

    script = "select count from 'graph1'"
    assert check_syntax_with_cyk(script)

    script = "select count from 'graph' intersect {'a' plus conc 'b'}"
    assert check_syntax_with_cyk(script)

    select = "select count from 'graph' intersect {'a' option conc 'b' conc 'c' plus}"
    assert check_syntax_with_cyk(script)

    script = "select edges from 'graph' intersect {('a' alt 'b') star conc 'c' plus conc 'd' option}'"
    assert check_syntax_with_cyk(script)

    script = "select edges from 'graph1' intersect 'graph2'"
    assert check_syntax_with_cyk(script)

    script = "count select from 'graph'"
    assert not check_syntax_with_cyk(script)

    script = "select chount from 'graph'"
    assert not check_syntax_with_cyk(script)

    script = "connect connect '/home/fl/graphs' "
    assert not check_syntax_with_cyk(script)

