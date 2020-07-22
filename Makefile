CWD     = $(CURDIR)
MODULE  = metaL
OS     ?= $(shell uname -s)

NOW = $(shell date +%d%m%y)
REL = $(shell git rev-parse --short=4 HEAD)

PIP = $(shell which pip3)
PY  = $(shell which python3)

.PHONY: all
all: $(PY) $(MODULE).py $(MODULE).ini
	echo $^
