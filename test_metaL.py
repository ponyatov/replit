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
