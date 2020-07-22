CWD     = $(CURDIR)
MODULE  = metaL
OS     ?= $(shell uname -s)

NOW = $(shell date +%d%m%y)
REL = $(shell git rev-parse --short=4 HEAD)

WGET = wget -c --no-check-certificate

PIP = $(shell which pip3)
PY  = $(shell which python3)


OBJ = tmp/empty.o tmp/hello


.PHONY: all
all: $(PY) $(MODULE).py $(MODULE).ini $(OBJ)
	echo $^

tmp/%.o: src/%.c
	tcc/bin/tcc -c -o $@ $<
tmp/%: src/%.c
	tcc/bin/tcc    -o $@ $< && $@



.PHONY: install update
install: $(OS)_install backend
	poetry install
update: $(OS)_update
	poetry update

.PHONY: Linux_install Linux_update
Linux_install Linux_update:
#	sudo apt update
#	sudo apt install -u `cat apt.txt`



TMP = $(CWD)/tmp

TCC_VER = 0.9.27
TCC     = tcc-$(TCC_VER)
TCC_GZ  = $(TCC).tar.bz2

.PHONY: backend
backend: $(CWD)/tcc/bin/tcc

TCC_CFG = --prefix=$(CWD)/tcc --disable-static --extra-cflags="-O2 -mtune=native"

$(CWD)/tcc/bin/tcc:
	$(MAKE) $(TMP)/$(TCC)/README
	cd $(TMP)/$(TCC) ; ./configure $(TCC_CFG) &&\
	$(MAKE) && $(MAKE) install &&\
	rm -rf $(TMP)/$(TCC)

$(TMP)/$(TCC)/README: $(TMP)/$(TCC_GZ)
	cd $(TMP) ; bzcat $< | tar -x && touch $@

$(TMP)/$(TCC_GZ):
	$(WGET) -O $@ http://download.savannah.gnu.org/releases/tinycc/$(TCC_GZ)
