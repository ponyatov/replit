
CWD    = $(CURDIR)
MODULE = demos
OS     = $(shell uname -s)

NOW = $(shell date +%d%m%y)
REL = $(shell git rev-parse --short=4 HEAD)

CC      = tcc -m32
AS      = tcc -m32
LD      = tcc -m32
OBJDUMP = objdump

.PHONY: all

all: $(MODULE).kernel
	qemu-system-i386 -kernel $<

OBJ += multiboot.o kernel.o

$(MODULE).kernel: $(OBJ)
	$(LD) -o $@ $^
%.o: %.s Makefile
	$(AS) -c -m32 -o $@ $< && $(OBJDUMP) -xdas $@ > $@.dump
%.o: %.c Makefile
	$(AS) -c -m32 -o $@ $< && $(OBJDUMP) -xdas $@ > $@.dump

.PHONY: zip
zip:
	git archive --format zip --output $(MODULE)_src_$(NOW)_$(REL).zip HEAD
