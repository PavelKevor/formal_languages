[![Build Status](https://travis-ci.org/PavelKevor/formal_languages.svg?branch=task1)](https://travis-ci.org/PavelKevor/formal_languages)
# formal_languages
## Task1
Simple tests for pygraphblas and pyformlang.
### Here you can see how to install these packages:
 - [pygraphblas](https://github.com/michelp/pygraphblas)
 - [pyformlang](https://pypi.org/project/pyformlang/)
 - [pytest](https://docs.pytest.org/en/stable/getting-started.html#install-pytest)
### To run tests:
 - pytest -s src/tests.py

## Task3
Time measurements of two implementations of transitive closure.
### To download data:
 - gdown https://drive.google.com/uc?id=158g01o2rpdq5eL3Ari8e5SPbbeZTJspr
### To run benchmark:
 - bash benchmark1_rpq.sh
### To see histograms in your browser:
 - python3 histograms.py
 
 ## Task7 Graph_database query language syntax.
 - [Language grammar](https://github.com/PavelKevor/formal_languages/blob/task-7/src/graph_db/language_grammar)
 
 - [Documentation](https://github.com/PavelKevor/formal_languages/blob/task-7/src/graph_db/readme.md)
 
 ## Additional_task1 Regular language recognizer using derivatives.
 You can use function check_word(regex, word) from regular_language_recognizer.py to check if word 
 belongs to regular expression using derivatives.
 
  Regular expression format:
 
    1) Alphbet - any symbols exept . , |, *
    2) . - concatenation, | - alternative plus, * - operator *
    3) You can use chains of symbols like symbols of alphabet
  Examples:
```sh
check_word('a*|a*.b', 'aaaaaaaaab')
check_word('a*.b*.c.d|d*.c*.b.a', 'aaabbbcd')
assert check_word('test1*|test1*.test2', 'test1test1test1test2')
```
