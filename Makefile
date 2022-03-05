setup:
	python3 -m venv ~/.MSDS434_project

install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest -vv test1.py
	
format:
	black *.py

lint:
	pylint --disable=R,C *.py
	
run: 
	python main.py

all: install lint test run
