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
CC      = %s
AS      = %s
LD      = %s
OBJDUMP = objdump''' % tuple(['tcc -m32'] * 3))
mk // ('''
.PHONY: all''')
mk // ('''
all: $(MODULE).kernel
\tqemu-system-i386 -kernel $<''')
mk // ('''
OBJ += multiboot.o kernel.o''')
mk // ('''
$(MODULE).kernel: $(OBJ)
\t$(LD) -o $@ $^''')
build_short = '%%.o: %%.%s Makefile\n\t$(AS) -c -m32 -o $@ $< && $(OBJDUMP) -xdas $@ > $@.dump'
mk // (build_short % 's')
mk // (build_short % 'c')
mk // ('''
.PHONY: zip
zip:
\tgit archive --format zip --output $(MODULE)_src_$(NOW)_$(REL).zip HEAD''')

apt = File('apt.txt')
filedir // apt
apt // ('git make binutils tcc qemu-system-i386')

gitignore = File('.gitignore')
filedir // gitignore
gitignore // ('*~\n*.swp\n\n*.o\n*.dump\n%s.kernel\n\n%s_src_*.zip' %
              (MODULE.val, MODULE.val))

# https://www.gnu.org/software/grub/manual/multiboot/multiboot.html
# https://wiki.osdev.org/Multiboot

multibooh = File('multiboot.h')
filedir // multibooh
multibooh // '// http://git.savannah.gnu.org/cgit/grub.git/tree/doc/multiboot.h?h=multiboot'

multiboot = File('multiboot.s')
filedir // multiboot
multiboot // ('''
#include "multiboot.h"

     .section  .multiboot''')
multiboot // ('''
    multiboot:
     required:
        magic: .long 0x1BADB002  // multiboot v.1
        flags: .long (1<<0|1<<2) // align 4K | videoinit
     checksum: .long 0x1BADB002  //
       memory:
  header_addr: .long 0
    load_addr: .long 0
load_end_addr: .long 0
 bss_end_addr: .long 0
   entry_addr: .long 0
 askvideomode:
    mode_type: .long 0           // ask linear buffer
        width: .long 640
       height: .long 480
        depth: .long 24
''')

# https://wiki.osdev.org/TCC

kernel = File('kernel.c')
filedir // kernel
kernel // ('''

''')

## @}
