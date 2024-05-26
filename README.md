# Build and deploy

Command to build the application. PLease remeber to change the project name and application name
```
gcloud builds submit --tag gcr.io/ondc-424509/catalogue-indexing-engine  --project=ondc-424509
```

Command to deploy the application
```
gcloud run deploy --image gcr.io/ondc-424509/catalogue-indexing-engine --platform managed  --project=ondc-424509 --allow-unauthenticated
```