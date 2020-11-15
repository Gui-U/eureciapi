SHELL := /bin/bash

test: venv/bin/activate
	source venv/bin/activate && ./main.py

venv/bin/activate:
	python3 -m venv venv && source venv/bin/activate && pip install -U pip setuptools && pip install -r requirements.txt

clean:
	rm -rf venv Fiche_de_paie_* payslip* calen*
