# MSDS434_project
MSDS 434 final project

## Google App Engine

set project id <br>
gcloud config set project 'msds434-2022-sa' <br>

activate virtual environment <br>
virtualenv ~/.venv <br>
source ~/.venv/bin/activate

cd into the MSDS folder <br>
git pull to get the most recent update <br>
gcloud app update <br>
gcloud app deploy <br>
gcloud app browse <br>

## Run on cloud shell
gcloud builds submit --tag gcr.io/msds434-2022-sa/mobile-app --project=msds434-2022-sa <br>
gcloud run deploy mobile-app --image gcr.io/msds434-2022-sa/mobile-app --platform managed --project=msds434-2022-sa --allow-unauthenticated --region us-west1 <br>
