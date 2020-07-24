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
        if isinstance(V, Object):
            V = V.val
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

    ## @name operator
    ## @{

    ## `A[key] ~> A.slot[key:str] | A.nest[key:int] `
    def __getitem__(self, key):
        if isinstance(key, int):
            return self.nest[key]
        elif isinstance(key, str):
            return self.slot[key]
        else:
            raise TypeError(that)

    ## `A[key] = B`
    def __setitem__(self, key, that):
        if isinstance(that, str):
            that = String(that)
        self.slot[key] = that
        return self

    ## `A << B ~> A[B.type] = B`
    def __lshift__(self, that):
        return self.__setitem__(that._type(), that)

    ## `A >> B ~> A[B.val] = B`
    def __rshift__(self, that):
        return self.__setitem__(that.val, that)

    ## `A // B -> A.push(B)`
    def __floordiv__(self, that):
        if isinstance(that, str):
            that = String(that)
        self.nest.append(that)
        return self

    ## @}

    ## @name evaluation
    ## @{

    ## evaluate in context
    ## @param[in] ctx context
    def eval(self, ctx): raise Error((self))

    ## @}

    ## @name html
    ## @{
    def html(self, ctx): return '<pre id=dump>%s</pre>' % self.dump()
    ## @}

## @defgroup error Error
## @ingroup object

## @ingroup error
class Error(Object, BaseException):
    pass

## @ingroup error
## undefined variable (forward assignment)
class Undef(Object):
    pass

## @defgroup prim Primitive
## @ingroup object

## @ingroup prim
class Primitive(Object):
    ## primitives evaluates to itself
    def eval(self, ctx): return self

## @ingroup prim
class Symbol(Primitive):
    pass

## @ingroup prim
class String(Primitive):
    def html(self, ctx): return self.val

## @ingroup prim
## floating point
class Number(Primitive):
    def __init__(self, V):
        Primitive.__init__(self, float(V))

    ## `-A`
    def minus(self, ctx):
        return self.__class__(-self.val)

    ## `+A`
    def plus(self, ctx):
        return self.__class__(+self.val)

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


## @defgroup active Active
## @ingroup object

## @ingroup active
## executable data elements
class Active(Object):
    pass

## @ingroup active
## operator
class Op(Active):
    def eval(self, ctx):
        # greedy computation for all subtrees
        greedy = list(map(lambda i: i.eval(ctx), self.nest))
        # unary
        if len(greedy) == 1:
            if self.val == '+':
                return greedy[0].plus(ctx)
            if self.val == '-':
                return greedy[0].minus(ctx)
        # unknown
        raise Error((self))

## @ingroup active
## Virtual Machine (environment + stack + message queue)
class VM(Active):
    pass


## @ingroup active
## global system VM
vm = VM(MODULE)
vm << vm


## @defgroup meta Meta
## @ingroup object

## @ingroup meta
class Meta(Object):
    pass

## @ingroup meta
class Module(Meta):
    ## @name html
    def html(self, ctx): return '<pre>%s</pre>' % self.val


vm['MODULE'] = Module(MODULE)


## @defgroup io IO
## @brief base file output

## @ingroup io
class IO(Object):
    pass

## @ingroup io
class File(IO):
    pass

## @defgroup game Game
## @brief `pygame` interface


import pygame

## @ingroup game
class Game(Object):
    def __init__(self, V):
        Object.__init__(self, V)
        pygame.init()

## @ingroup game
class Display(Game):

    ## @param[in] W width in pixels
    ## @param[in] H height in pixels
    def __init__(self, V, W=320, H=240):
        Game.__init__(self, V)
        self['W'] = Integer(W)
        self['H'] = Integer(H)

    ## show game window on execution
    def eval(self, ctx):
        W = self['W'].val
        H = self['H'].val
        self.display = pygame.display.set_mode((W, H))
        return self


vm['game'] = Game(MODULE) << Display(MODULE)


## @defgroup lexer lexer
## @ingroup parser
import ply.lex as lex

## @ingroup lexer
## token types
tokens = ['symbol',
          'number', 'integer', 'hex', 'bin',
          'add', 'sub', 'mul', 'div', 'pow']

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

## @name operator
## @{

## @ingroup lexer
##    r'\+'
def t_add(t):
    r'\+'
    t.value = Op(t.value)
    return t
## @ingroup lexer
##    r'\-'
def t_sub(t):
    r'\-'
    t.value = Op(t.value)
    return t
## @ingroup lexer
##    r'\*'
def t_mul(t):
    r'\*'
    t.value = Op(t.value)
    return t
## @ingroup lexer
##    r'\/'
def t_div(t):
    r'\/'
    t.value = Op(t.value)
    return t
## @ingroup lexer
##    r'\^'
def t_pow(t):
    r'\^'
    t.value = Op(t.value)
    return t

## @}

## @name lexeme
## @{

## @ingroup lexer
##    r`[0-9]+\.[0-9]*([eE][+\-]?[0-9]+)?`
def t_number(t):
    r'[0-9]+\.[0-9]*([eE][+\-]?[0-9]+)?'
    t.value = Number(t.value)
    t.type = 'number'
    return t

## @ingroup lexer
##    r`[0-9]+[eE][+\-]?[0-9]+`
def t_number_exp(t):
    r'[0-9]+[eE][+\-]?[0-9]+'
    t.value = Number(t.value)
    t.type = 'number'
    return t

## @ingroup lexer
##    r`0x[0-9a-fA-F]+`
def t_hex(t):
    r'0x[0-9a-fA-F]+'
    t.value = Hex(t.value)
    return t

## @ingroup lexer
##    r`0b[01]+`
def t_bin(t):
    r'0b[01]+'
    t.value = Bin(t.value)
    return t

## @ingroup lexer
##    r`[0-9]+`
def t_integer(t):
    r'[0-9]+'
    t.value = Integer(t.value)
    return t

## @ingroup lexer
##    r`[^ \t\r\n\#\+\-\*\/\^]+`
def t_symbol(t):
    r'[^ \t\r\n\#\+\-\*\/\^]+'
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
    ## AST evaluates to new AST with each subelement evaluated
    def eval(self, ctx):
        res = AST(self.val)
        for i in self.nest:
            res // i.eval(ctx)
        return res

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

## @name operator
## @{


## @ingroup parser
precedence = (
    ('left', 'add', 'sub'),
    ('left', 'mul', 'div'),
    ('left', 'pow', ),
    ('left', 'pfx', ),
)

## @ingroup parser
##    ' ex : add ex %prec pfx ' `+A`
def p_ex_plus(p):
    ' ex : add ex %prec pfx '
    p[0] = p[1] // p[2]
## @ingroup parser
##    ' ex : sub ex %prec pfx ' `-A`
def p_ex_minus(p):
    ' ex : sub ex %prec pfx '
    p[0] = p[1] // p[2]

## @}

## @name number
## @{

## @ingroup parser
##    r' ex : number '
def p_ex_number(p):
    r' ex : number '
    p[0] = p[1]
## @ingroup parser
##    r' ex : integer '
def p_ex_integer(p):
    r' ex : integer '
    p[0] = p[1]
## @ingroup parser
##    r' ex : hex '
def p_ex_hex(p):
    r' ex : hex '
    p[0] = p[1]
## @ingroup parser
##    r' ex : bin '
def p_ex_bin(p):
    r' ex : bin '
    p[0] = p[1]

## @}

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
            for ast in parser.parse(src.read()):
                print(ast)
                print(ast.eval(vm))
                print('-' * 66)


if __name__ == '__main__':
    init()
    print(vm)
