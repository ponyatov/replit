import pytest

from metaL import *

class TestObject:

  def test_empty(self):
    assert 1==1

  def hello(self): return Object('Hello')

  def test_hello(self):
    assert self.hello().test ==\
    ''
