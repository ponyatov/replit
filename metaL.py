MODULE = 'metaL'
TITLE = '[meta]programming [L]anguage'
ABOUT = 'homoiconic metaprogramming system'
AUTHOR = 'Dmitry Ponyatov'
EMAIL = 'dponyatov@gmail.com'
YEAR = 2020
LICENSE = 'MIT'

import os, sys

from xxhash import xxh32

class Object:

  def __init__(self, V):
    # name / scalar value
    self.val = V
    # attributes = dict = env
    self.slot = {}
    # nested AST = vector = stack = queue
    self.nest = []

  ## dump

  def __repr__(self): return self.dump()

  def test(self): return self.dump(test=True)

  def dump(self, cycle=None, depth=0, prefix='', test=False):
    # header
    tree = self._pad(depth, tab) + self.head(prefix, test)
    # subtree
    return tree

  def _pad(self,depth): return '\n' + '\t'*depth

  def head(self, prefix='', test=False):
    hdr = '%s<%s:%s>' %(prefix,self._type(),self._val())
    if not test:
      hdr += '@%x'%id(self)
    return hdr
    