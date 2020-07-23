#  ![logo](doc/hedge64x64.png) `metaL`
## version for Repl.it Language Jam contest

https://repl.it/@DmitryPonyatov/replit

doxygen manual: https://ponyatov.github.io/replit/modules.html

* https://blog.repl.it/langjam
* https://repl.it/talk/share/metaL-for-replit-Language-Jam-contest/46470

(c) Dmitry Ponyatov <<dponyatov@gmail.com>> 2020 MIT

github: https://github.com/ponyatov/replit

## Language Ideas Promo

* take Lisp homoiconic nature and port it to CPython3 stack (VM & libs)
* provide a light environment for **metaprogramming by code generation**
  * `metaL` is a special language for writing programs that write other programs (in C & Python)
* protect people from the parens soup by using infix syntax
  and AST-friendly data structure in place of classic lists
* integrate best features from Python, Lisp/Clojure, and Smalltalk
* targets on IoT programming:
  * ANSI C code generation is required by design
    * uses amazing [TCC](https://bellard.org/tcc/) host compiler backend for fast debug
  * cross-compiling to many embedded devices including
    AVR8, Cortex-M, and MSP430 microcontrollers
    * uses GCC cross-compiler for portability

### Concept Programming

CP here is a programming model described in the works of Enn Heraldovich Tyugu
about model-based software development. It is not mean the term by Alexsandr
Stepanov here. The common idea is about making domain models describe the
problem in a wide in the form of relation networks, and automatic program (code)
synthesis from specifications to solve concrete tasks. This synthesis works over
these networks using them as *generic knowledge representation*.

* http://www.cs.ioc.ee/~tyugu/
* J. Symbolic Computation (1988) 5, 359-375\ The Programming System PRIZ [sym88]

## Base Node Class

The core of the **graph interpreter system** is a homoiconic model uses a
directed graph of objects as both program and data representation. The idea was
taken from [minsky] and extended with the ability to store not only slots
(attributes) but also hold any knowledge frames in an ordered container.

https://www.youtube.com/watch?v=nXJ_2uGWM-M

Frames originated as a technology used for knowledge representation in
artificial intelligence. They are very close to objects and class hierarchies in
object-oriented languages although their fundamental design goals are different.
Frames are focused on the explicit and intuitive representation of knowledge
whereas objects focus on encapsulation and binding data with processing
procedures. Original Marvin Minsky's concept *lacks some principal features for
software design*, so it must be extended with the ability to *store sequential
collections*.

In practice, the techniques and capabilities of the frame model and
object-oriented languages overlap significantly so much as we can treat frames
not only a native superset of OOP but they drastically extend object design
concepts wider: we can represent any knowledge in frames, and use any
programming paradigms as we desire.

```py
class Frame:
    def __init__(self, V):
        # scalar data value
        # mostly names the frame, but also can store things like numbers and strings
        self.val = V
        # named slots = attributes = string-keyed associative array
        self.slot = {}
        # ordered storage = program AST nested elemens = vector = stack
        self.nest = []
        # unique storage id (Redis,RDBMS,..)
        self.sid = '@%x' % id(self)
```

This data node structure which combines named slots with the ordered collection
is definitively required for representing any program source code, as this is
very close to classical AST and attribute grammar but uses graph in place of the
attributed tree. The object graph (frame) representation of a program as a
primary form is effective and *native for any work involved with source code
transformations*: synthesis, modifications, analysis, cross-language
translation, etc.

Factically, **we don't require any text programming language at all**, as this
*Executable Data Structure* can

* hold any program statically (as storage),
* be executed by the EDS-interpreter, so it is *active* data
* can be translated into any mainstream programming language or
* [cross-]compiled into machine code via LLVM.

### Homoiconic programming model

**Homoiconicity** is a property of a programming language in which any program
is *simultaneously*

* an easy to modify *data structure*, and
* an *executable program representation* (program source code).

In a homoiconic language, a programmer does not just have access to the source
code, but the language itself specifically provides tools and easy to use
methods for convenient work with parts of programs (represented as generic data)
in runtime.

* Say, if you include source code of your program in C++ into the distribution
  package, you can work with the program code as data, but only at the level of
  text files, or using third-party analysis libraries. In the C++ language
  itself, there are no dedicated tools for reading, modifying, or generating
  source code.
* Conversely, in the Lisp language, all programs are represented in the form of
  executable lists -- these lists are simultaneously a program and the usual
  universal data structure for working with which the language was specially
  created.

### EDS Interpreter

In order to use the advantages of homoiconicity in your programs written in any
conventional languages (C++, Java,..), you need to integrate an
**EDS-interpreter** into your programs that will

* *execute some data structure as a program*, and additionally
* provides high-level tools for modifying program/data graph in runtime.

It is not necessary that this interpreter should include a parser of some
scripting language, as *graph structure can be generated directly by code in the
implementation language*, and by structure self-transformation. To create a
program in such a system, you only need to have any way to create an *executable
data structure* in memory: it can be GUI-based drawing, text format parser,
external graph database, or some C++ code that forces the compiler to include
such a structure in the executable file statically.

### `metaL` is no-syntax language

In a long long time, CLI (command-line interface) and scripting show itself very
effective from the first days of computing and don't go to become obsolete. So,
it is handy to have some lite DDL/DML script language in front of your
metaL-based system just to be able to use it for initialization files, and
making some interactive queries to the running system. *This DDL/DML is not the
`metaL` itself*, its just a way to host system snapshot in git-friendly text
files and provide very light CLI. But, `metaL` is the language of live data
structures in running computer memory. It specifies common ides
* how these structures are presented (unified storage),
* methods of computation (some sort of expression evaluation, close to AST
  interpretation), and
* set of node types described in the language core, which you can expand next as
  you want.

### Metaprogramming

Metaprogramming -- when one program modifies (generates) another program,
including itself.

Metaprogramming is a method of boosting your efficiency as a programmer by
expanding the language you use. If you write very similar code every day, in
languages ​​that can do meta (Lisp, Nim), you can write small macro programs
that will run during the compilation stage, and generate new code by a template,
or modify an existing code the way as you need it. Factically, you can add to
the language those features that are needed for a narrow set of your specific
tasks.

In order to be able to use metaprogramming in a full scale, the language or
programming system you are using must be homoiconic. If you want to use this
method with industrial programming languages, the use of an EDS interpreter will
allow you to quickly and conveniently solve your problems, paying for it with
some losses in the speed of programs and memory usage (see a comparison of
interpreters vs the compilers into machine code).

## Links

[SICP] [Structure and Interpretation of Computer Programs](https://mitpress.mit.edu/sites/default/files/sicp/full-text/book/book-Z-H-4.html#%_toc_start)
       Harold Abelson, Gerald Jay Sussman, Julie Sussman // MIT Press, 1996, ISBN	0-262-51087-1
       

[minsky] Marvin Minsky [Frames for data representation](https://web.media.mit.edu/~minsky/papers/Frames/frames.html)

[tyugu] **Knowledge-Based Programming** Enn Tyugu 1988 // Addison-Wesley Longman Publishing Co., Inc.

[tyuguru] Э.Х.Тыугу **Концептуальное программирование**. М.: Наука, 1984. 255 с

[sym88] J. Symbolic Computation (1988) 5, 359-375\ **The Programming System PRIZ**
\ G.Mints, E.Tyugu, Institute of Cybernetics, Estonian Academy of
Sciences,Tallinn 200108, USSR \
[pdf](https://www.academia.edu/18315153/The_programming_system_PRIZ?auto=download)

[priz] **Инструментальная система программирования ЕС ЭВМ (ПРИЗ)** / М.И. Кахро,
А.П. Калья, Энн Харальдович Тыугу . – Изд. 2-е – Москва : Финансы и статистика,
1988 . – 181 с ISBN 5-279-00111-2
