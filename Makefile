setup:
	python3 -m venv ~/.MSDS434_project

install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest -vv -- tests/*.py

lint:
	pylint --disable=R,C myrepolib cli web

all: install lint test
