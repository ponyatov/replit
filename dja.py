## @file
## @brief Django templates

## @defgroup dj Dja
## @brief Meta-level web development patterns for Django
##
## @{

from metaL import *

MODULE = Module('dja')
vm['dja'] = MODULE
MODULE['MODULE'] = MODULE

TITLE = Title('Meta-level web development patterns for Django')
MODULE['TITLE'] = TITLE
MODULE['ABOUT'] = String('''
''')

filedir = Dir(MODULE)
MODULE << filedir

mk = File('Makefile')
filedir // mk
mk // ('''
CWD    = $(CURDIR)
MODULE = %s
OS     = $(shell uname -s)''' % MODULE.val)
mk // ('''
NOW = $(shell date +%d%m%y)
REL = $(shell git rev-parse --short=4 HEAD)''')
mk // ('''
.PHONY: all
all:''')

MODULE

## @}
