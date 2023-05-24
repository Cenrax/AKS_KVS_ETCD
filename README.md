## Run the server
```
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Process to run the app

- docker build -t my-fastapi-app:latest .
- docker tag my-fastapi-app:latest sketcd.azurecr.io/my-fastapi-app:latest
- docker push sketcd.azurecr.io/my-fastapi-app:latest


## Login to ACR
- az acr login --name sketcd


## Get the logs
- kubectl logs -f deployment/fastapi-app

## Locally check the health
```
etcdctl --endpoints=localhost:2379 --user root --password sk123 endpoint health
```