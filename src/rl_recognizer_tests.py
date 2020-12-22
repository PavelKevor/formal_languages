from regular_language_recognizer import *


def check_word_test:
    assert check_word('a*|a*.b', 'ab')

    assert check_word('a*|a*.b', 'aaaaaaaaab')

    assert check_word('a*|a*.b', 'aaaaaaaaaa')

    assert not check_word('a*|a*.b', 'aaabbb')

    assert not check_word('a*|a*.b', 'bbbbb')

    assert not check_word('a*|a*.b', 'abababab')

    assert check_word('a.b*.c*|d*', 'ddddddddddddddddddd')

    assert check_word('a*.b*.c.d|d*.c*.b.a', 'aaabbbcd')

    assert check_word('a*.b*.c.d|d*.c*.b.a', 'ddddccccba')

    assert not check_word('a*.b*.c.d|d*.c*.b.a', 'dcbbbbaaaa')

    assert not check_word('a*.b*.c.d|d*.c*.b.a', 'abcdd')

    assert check_word('a*.b*.c*.d*.k*.n*.a.b.c.d|a|d|f|h|s|g|s|j|m', 'aaaaaaabbbbbbccccccdddddddddddddddddkkkkkkkkkknnnnnnnnnabcd')

    assert check_word('a*.b*.c*.d*.k*.n*.a.b.c.d|a|d|f|h|s|g|s|j|m', 'f')

    assert not check_word('a*.b*.c*.d*.k*.n*.a.b.c.d|a|d|f|h|s|g|s|j|m', 'aaaaaaabbbbbbccccccdddddddddddddddddkkkkkkkkkknnnnnnnnnabc')

    assert check_word('test1*|test1*.test2', 'test1test1test1test2')
