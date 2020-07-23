CWD     = $(CURDIR)
MODULE  = metaL
OS     ?= $(shell uname -s)

NOW = $(shell date +%d%m%y)
REL = $(shell git rev-parse --short=4 HEAD)

WGET = wget -c --no-check-certificate

PIP = $(CWD)/bin/pip3
PY  = $(CWD)/bin/python3
PYT = $(CWD)/bin/pytest
PEP = $(CWD)/bin/autopep8 --ignore=E26,E302,E401,E402

OBJ = tmp/empty.o tmp/hello


.PHONY: all
all: $(PY) $(MODULE).py $(MODULE).ini $(OBJ)
	$(MAKE) pep
	$(PY)   -i $(MODULE).py $(MODULE).ini
.PHONY: test
test:
	$(MAKE) pep
	$(PYT)  test_$(MODULE).py
.PHONY: pep
pep:	
	$(PEP) -i      $(MODULE).py
	$(PEP) -i test_$(MODULE).py

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

.PHONY: venv
venv:
	python3 -m venv .
	$(PIP) install -U pip autopep8 pytest
	$(PIP) install -U -r requirements.txt
	$(MAKE) requirements.txt
.PHONY: requirements.txt
requirements.txt: $(PIP)
	$< freeze | grep -v 0.0.0 > $@



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



.PHONY: doxy
doxy:
	doxygen doxy.gen 1>/dev/null
