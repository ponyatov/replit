MODULE = 'metaL'
TITLE = '[meta]programming [L]anguage'
ABOUT = 'homoiconic metaprogramming system'
AUTHOR = 'Dmitry Ponyatov'
EMAIL = 'dponyatov@gmail.com'
YEAR = 2020
LICENSE = 'MIT'


## base object graph node

class Object:

    def __init__(self, V):
        # name / scalar value
        self.val = V
        # attributes = dict = env
        self.slot = {}
        # nested AST = vector = stack = queue
        self.nest = []

    # dump

    def __repr__(self): return self.dump()

    def test(self): return self.dump(test=True)

    def dump(self, cycle=None, depth=0, prefix='', test=False):
        # header
        tree = self._pad(depth) + self.head(prefix, test)
        # cycles
        if not depth:
            cycle = []
        if self in cycle:
            return tree + ' _/'
        else:
            cycle.append(self)
        # slot{}s
        for i in sorted(self.slot.keys()):
            tree += self.slot[i].dump(cycle, depth + 1, '%s = ' % i, test)
        # nest[]ed
        idx = 0
        for j in self.nest:
            tree += j.dump(cycle, depth + 1, '%s: ' % idx, test)
            idx += 1
        # subtree
        return tree

    def _pad(self, depth): return '\n' + '\t' * depth

    def head(self, prefix='', test=False):
        hdr = '%s<%s:%s>' % (prefix, self._type(), self._val())
        if not test:
            hdr += ' @%x' % id(self)
        return hdr

    def _type(self): return self.__class__.__name__.lower()

    def _val(self): return '%s' % self.val

    ## operator

    def __getitem__(self, key):
        return self.nest[key]

    def __setitem__(self, key, that):
        self.slot[key] = that
        return self

    def __lshift__(self, that):
        return self.__setitem__(that._type(), that)

    def __rshift__(self, that):
        return self.__setitem__(that.val, that)

    def __floordiv__(self, that):
        self.nest.append(that)
        return self


class Primitive(Object):
    pass

class Symbol(Primitive):
    pass

class String(Primitive):
    pass

class Number(Primitive):
    def __init__(self, V):
        Primitive.__init__(self, float(V))

class Integer(Number):
    def __init__(self, V):
        Primitive.__init__(self, int(V))

class Hex(Integer):
    def __init__(self, V):
        Primitive.__init__(self, int(V[2:], 0x10))

    def _val(self):
        return hex(self.val)

class Bin(Integer):
    def __init__(self, V):
        Primitive.__init__(self, int(V[2:], 0x02))

    def _val(self):
        return bin(self.val)
