## @file
## Demo OS in metaL/Python

## @defgroup demos DemoOS
## @brief `unikernel` in metaL/Python
##
## It's an operating system model treated as a demo of writing a language-powered
## OS in Python, which was mentioned in https://t.me/osdev channel a few weeks ago.
## It is not something more than just a fun toy, not targets for any practical use
## or Linux killer.
##
## On the other side, I don't see a lot of projects on implementing hobby OS based
## on some language interpreter, compiler embedded into the OS kernel, or
## standalone interactive development system, as it was popular in the 80th.
##
## So, in this demo, I'm going to mix a bytecode interpreter, a few bare-metal
## drivers written in C and assembly, and the method of concept programming in
## Python. Also, it should run in a *guest OS* mode as generic application over
## mainstream OS such as Linux.
## @{

from metaL import *

MODULE = Module('demos')
vm['MODULE'] = MODULE

TITLE = Title('Demo OS in metaL/Python')
vm['TITLE'] = TITLE

ABOUT = String('''
It's an operating system model treated as a demo of writing a language-powered
OS in Python, which was mentioned in https://t.me/osdev channel a few weeks ago.
It is not something more than just a fun toy, not targets for any practical use
or Linux killer.
''')
vm['ABOUT'] = ABOUT

## directory for generated files
filedir = Dir(MODULE)
vm['dir'] = filedir

README = File('README.md')
filedir // README

README // ('#  `%s`' % MODULE.val)
README // ('## %s' % TITLE.val)
README // (ABOUT)
README // ('(c) %s <<%s>> %s %s' %
           (AUTHOR.val, EMAIL.val, YEAR.val, LICENSE.val))
README // ('')
README // ('github: %s/%s' %
           (GITHUB.val, 'replit/blob/master/%s.py' % MODULE.val))

## @}
