CWD     = $(CURDIR)
MODULE  = metaL
OS     ?= $(shell uname -s)

NOW = $(shell date +%d%m%y)
REL = $(shell git rev-parse --short=4 HEAD)

WGET = wget -c --no-check-certificate

PIP = $(shell which pip3)
PY  = $(shell which python3)

.PHONY: all
all: $(PY) $(MODULE).py $(MODULE).ini
	echo $^



TMP = $(CWD)/tmp

TCC_VER = 0.9.27
TCC     = tcc-$(TCC_VER)
TCC_GZ  = $(TCC).tar.bz2

.PHONY: tcc
tcc: $(TMP)/$(TCC_GZ)
	echo $<

$(CWD)/tcc/bin/tcc: $(TMP)/$(TCC_GZ)

$(TMP)/$(TCC_GZ):
	$(WGET) -O $@ http://download.savannah.gnu.org/releases/tinycc/$(TCC_GZ)

