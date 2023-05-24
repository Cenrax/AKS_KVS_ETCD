## How did I created the kubernetes cluster

- Created a Kubernetes cluster in Azure
- Configured my localmachine with az cmd using
    ```
    az aks get-credentials --resource-group <resource-group-name> --name <cluster-name>
    ```
- Connected it with my cluster (Verified it using kubectl get nodes)
- Installed helm to deploy the etcd database in my cluster
    ```
    helm install my-etcd oci://registry-1.docker.io/bitnamicharts/etcd
    ```
- 



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
