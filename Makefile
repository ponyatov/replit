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

SRC = $(shell find $(CWD) -maxdepth 1 -type f -regex .+.py$$)

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
	echo $(SRC) | xargs -n1 -P0 $(PEP) -i

.PHONY: web
web: $(PY) webook.py
	$^ $(SRC)

tmp/%.o: src/%.c
	tcc/bin/tcc -c -o $@ $<
tmp/%: src/%.c
	tcc/bin/tcc    -o $@ $< && $@



.PHONY: install update

install: $(PIP) backend js
	-$(MAKE) $(OS)_install
	$(PIP)   install    -r requirements.txt
#	poetry install
update: $(PIP)
	-$(MAKE) $(OS)_update
	$(PIP)   install -U    pip
	$(PIP)   install -U -r requirements.txt
	$(MAKE)  requirements.txt
#	poetry update

$(PIP) $(PY) $(PEP):
	python3 -m venv .
	$(PIP) install -U pip pylint autopep8
	$(MAKE) requirements.txt
$(PYT):
	$(PIP) install -U pytest
	$(MAKE) requirements.txt

.PHONY: Linux_install Linux_update
Linux_install Linux_update:
	sudo apt update
	sudo apt install -u `cat apt.txt`

.PHONY: venv
venv:
	python3 -m venv .
	$(PIP) install -U pip autopep8 pytest
	$(PIP) install -U -r requirements.txt
	$(MAKE) requirements.txt
.PHONY: requirements.txt
requirements.txt: $(PIP)
	$< freeze | grep -v 0.0.0 > $@

.PHONY: js
js: static/jquery.js static/bootstrap.css static/bootstrap.js

JQUERY_VER = 3.5.1
static/jquery.js:
	$(WGET) -O $@ https://code.jquery.com/jquery-$(JQUERY_VER).min.js

BOOTSTRAP_VER = 3.4.1
BOOTSTRAP_URL = https://stackpath.bootstrapcdn.com/bootstrap/$(BOOTSTRAP_VER)/
static/bootstrap.css:
	$(WGET) -O $@ https://bootswatch.com/3/darkly/bootstrap.min.css
static/bootstrap.js:
	$(WGET) -O $@ $(BOOTSTRAP_URL)/js/bootstrap.min.js



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



.PHONY: master shadow release

MERGE  = Makefile README.md .vscode apt.txt requirements.txt
MERGE += $(MODULE).py $(MODULE).ini test_$(MODULE).py
MERGE += webook.py static templates

master:
	git checkout $@
	git pull -v
	git checkout shadow -- $(MERGE)
	$(MAKE) doxy

shadow:
	git checkout $@
	git pull -v

release:
	git tag $(NOW)-$(REL)
	git push -v && git push -v --tags
	$(MAKE) shadow
