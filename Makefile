setup:
	sudo apt -y install python3.8-venv
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
	
flask: 
	python3 main.py

gcloud: 
	echo "deb https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
	curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
	sudo apt-get update && sudo apt-get install google-cloud-sdk
	
deploy: 
	gcloud app deploy --project=msds434-2022-sa --version=production --quiet

run: 
	python3 main.py

all: install lint test
