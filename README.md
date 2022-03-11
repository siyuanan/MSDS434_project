# MSDS434_project
MSDS 434 final project

## Google App Engine

set project id
gcloud config set project 'msds434-2022-sa'

activate virtual environment
virtualenv ~/.venv
source ~/.venv/bin/activate

cd into the MSDS folder
git pull to get the most recent update
gcloud app update
gcloud app deploy
gcloud app browse

## Run on cloud shell
gcloud builds submit --tag gcr.io/msds434-2022-sa/mobile-app --project=msds434-2022-sa
gcloud run deploy mobile-app --image gcr.io/msds434-2022-sa/mobile-app --platform managed --project=msds434-2022-sa --allow-unauthenticated --region us-west2
