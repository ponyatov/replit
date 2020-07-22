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
            '\n<object:Hello>'
