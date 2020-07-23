## @file
## @brief `metaL` core

MODULE = 'metaL'
TITLE = '[meta]programming [L]anguage'
ABOUT = 'homoiconic metaprogramming system'
AUTHOR = 'Dmitry Ponyatov'
EMAIL = 'dponyatov@gmail.com'
YEAR = 2020
LICENSE = 'MIT'


import os, sys

## @defgroup object Object

## @brief base object graph node
## @ingroup object
class Object:

    ## construct object
    ## @param[in] V given scalar value
    def __init__(self, V):
        ## name / scalar value
        self.val = V
        ## attributes = dict = env
        self.slot = {}
        ## nested AST = vector = stack = queue
        self.nest = []

    ## @name dump
    ## @{

    ## `print` callback
    def __repr__(self): return self.dump()

    ## dump for tests (no sid in headers)
    def test(self): return self.dump(test=True)

    ## dump in full text tree form
    ## @param[in] cycle already dumped objects (cycle prevention registry)
    ## @param[in] depth recursion depth
    ## @param[in] prefix optional prefix in `<T:V>` header
    ## @param[in] test test dump option @ref test
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

    ## paddig for @ref dump
    def _pad(self, depth): return '\n' + '\t' * depth

    ## short `<T:V>` header only
    ## @param[in] prefix optional prefix in `<T:V>` header
    ## @param[in] test test dump option @ref test
    def head(self, prefix='', test=False):
        hdr = '%s<%s:%s>' % (prefix, self._type(), self._val())
        if not test:
            hdr += ' @%x' % id(self)
        return hdr

    def _type(self): return self.__class__.__name__.lower()

    def _val(self): return '%s' % self.val

    ## @}

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


## @defgroup prim Primitive
## @ingroup object

## @ingroup prim
class Primitive(Object):
    pass

## @ingroup prim
class Symbol(Primitive):
    pass

## @ingroup prim
class String(Primitive):
    pass

## @ingroup prim
## floating point
class Number(Primitive):
    def __init__(self, V):
        Primitive.__init__(self, float(V))

## @ingroup prim
class Integer(Number):
    def __init__(self, V):
        Primitive.__init__(self, int(V))

## @ingroup prim
## hexadecimal machine number
class Hex(Integer):
    def __init__(self, V):
        Primitive.__init__(self, int(V[2:], 0x10))

    def _val(self):
        return hex(self.val)

## @ingroup prim
## bit string
class Bin(Integer):
    def __init__(self, V):
        Primitive.__init__(self, int(V[2:], 0x02))

    def _val(self):
        return bin(self.val)

## @defgroup cont Container
## @ingroup object

## @ingroup cont
## generic data container
class Container(Object):
    pass

## @ingroup cont
## var size array (Python list)
class Vector(Container):
    pass

## @ingroup cont
## FIFO stack
class Stack(Container):
    pass

## @ingroup cont
## associative array
class Dict(Container):
    pass


## @defgroup lexer lexer
## @ingroup parser

import ply.lex as lex

## @ingroup lexer
## token types
tokens = ['symbol']

## @ingroup lexer
## drop spaces
t_ignore = ' \t\r'

## @ingroup lexer
## line commens starts with `#`
t_ignore_comment = r'\#.*'

## @ingroup lexer
## increment line counter on every new line
def t_nl(t):
    r'\n'
    t.lexer.lineno += 1

## @name lexeme
## @{

## @ingroup lexer
def t_symbol(t):
    r'[^ \t\r\n\#]+'
    t.value = Symbol(t.value)
    return t

## @}

## @ingroup lexer
## lexer error callback
def t_ANY_error(t): raise SyntaxError(t)


## @ingroup lexer
## PLY lexer
lexer = lex.lex()


## @defgroup parser parser

import ply.yacc as yacc

## @ingroup parser
## Abstract Syntax Tree =~= any `metaL` graph
class AST(Object):
    pass

## @ingroup parser
##    ' REPL : '
## create empty AST on recursion start
def p_REPL_none(p):
    ' REPL : '
    p[0] = AST('')

## @ingroup parser
##    ' REPL : REPL ex '
## collect every parsed [ex]pression
def p_REPL_recursion(p):
    ' REPL : REPL ex '
    p[0] = p[1] // p[2]


## @ingroup parser
##    ' ex : symbol '
def p_ex_symbol(p):
    ' ex : symbol '
    p[0] = p[1]

## @ingroup parser
## syntax error callback
def p_error(p): raise SyntaxError(p)


## @ingroup parser
## PLY parser
parser = yacc.yacc(debug=False, write_tables=False)


## @defgroup init system init

## @ingroup init
## handle command-line arguments as filenames must be interpreted
def init():
    for init in sys.argv[1:]:
        with open(init) as src:
            print(parser.parse(src.read()))


if __name__ == '__main__':
    init()
