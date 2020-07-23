import pytest

from metaL import *


class TestObject:

    def hello(self): return Object('Hello')
    def world(self): return Object('World')

    def test_hello(self):
        assert self.hello().test() ==\
            '\n<object:Hello>'

    def test_world(self):
        assert (self.hello() // self.world()).test() ==\
            '\n<object:Hello>' +\
            '\n\t0: <object:World>'

    def test_leftright(self):
        hello = self.hello()
        world = self.world()
        left = Object('left')
        right = Object('right')
        assert (hello // world << left >> right).test() ==\
            '\n<object:Hello>' +\
            '\n\tobject = <object:left>' +\
            '\n\tright = <object:right>' +\
            '\n\t0: <object:World>'


class TestPrimitive:

    def test_number(self):
        assert Number(486).test() ==\
            '\n<number:486.0>'

    def test_integer(self):
        assert Integer('-01').test() ==\
            '\n<integer:-1>'

    def test_number_dot(self):
        assert Number('+02.30').test() ==\
            '\n<number:2.3>'

    def test_hex(self):
        x = Hex('0xDeadBeef')
        assert x.test() == '\n<hex:0xdeadbeef>'
        assert x.val == 3735928559

    def test_bin(self):
        x = Bin('0b1101')
        assert x.test() == '\n<bin:0b1101>'
        assert x.val == 13


class TestLexer:

    def test_none(self):
        lexer.input('')
        assert lexer.token() == None

    def test_comment(self):
        lexer.input('# comment')
        assert lexer.token() == None

    def test_spaces(self):
        lexer.input(' \t\r\n')
        assert lexer.token() == None

    def test_symbol(self):
        lexer.input('symbol')
        token = lexer.token()
        assert token and token.value.test() ==\
            '\n<symbol:symbol>'


class TestParser:

    def test_none(self):
        assert parser.parse('').test() ==\
            '\n<ast:>'
