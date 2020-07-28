## @file
## metacircular implementation in metaL/Python

## @defgroup circ Metacircular
## @brief `implementation in metaL/Python`
## @{

from metaL import *

## global Virtual Machine (recreated)
vm = VM(MODULE)
vm << vm

## @name metainfo
## @brief constants reimported from the `metaL` module
## @{

MODULE = Module(MODULE)
vm['MODULE'] = MODULE

TITLE = Title(TITLE)
vm['TITLE'] = TITLE

ABOUT = String(ABOUT) // String('''

This source code in Python shows the usage of pure metaL without any parser as a
complex sample by implementing metaL in itself. If you want to design your own
language, factically it is not required to have source code in text files, you
can use executable data structures as a unified program/data representation, and
any host language you are friendly with to interpret and do the magic.

It is also the demo of using the DRY principle: Don't Repeat Yourself. There are
a lot of mainstream languages used in production, but we need yet another
highest-level language to describe concepts in software development and generate
code into many dependent files. It's metaprogramming in a wide.

''')
vm['ABOUT'] = ABOUT

AUTHOR = Author(AUTHOR)
vm['AUTHOR'] = AUTHOR

EMAIL = Email(EMAIL)
vm['EMAIL'] = EMAIL

AUTHOR << EMAIL

YEAR = YEAR
vm['YEAR'] = YEAR

LICENSE = License(LICENSE)
vm['LICENSE'] = LICENSE

GITHUB = Url(GITHUB)
vm['GITHUB'] = GITHUB

LOGO = PNG(LOGO)
vm['LOGO'] = LOGO

## @}

## documentation is also first-class objects
doc = Doc(MODULE)
vm << doc

print(vm)

## @}
