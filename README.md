# MSDS434_project
MSDS 434 final project

## Run on cloud shell
gcloud builds submit --tag gcr.io/msds434-2022-sa/mobile-app --project=msds434-2022-sa
gcloud run deploy mobile-app --image gcr.io/msds434-2022-sa/mobile-app --platform managed --project=msds434-2022-sa --allow-unauthenticated --region us-west2
