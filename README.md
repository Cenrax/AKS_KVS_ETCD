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
- Created an Azure Container Registry and pushed the image
    ```
    cd src
    docker build -t my-fastapi-app:<version-no> .
    docker tag my-fastapi-app:<version-no> <acr-name>.azurecr.io/my-fastapi-app:<version-name>
    docker push <acr-name>.azurecr.io/my-fastapi-app:<version-name>
    ```
- Connect to the ACR
    ```
    az acr login --name <acr-name>
    ```
- Connect the cluster with the ACR
    ```
    az aks update -n <cluster-name> -g <resource-group-name> --attach-acr <acr-name>
    ```

The cluster is setup now we need to deploy the deployments and the service (so it can be accessed outside the cluster)

Note : We need to have kubectl installed in the local-machine
```
cd scripts
kubectl apply -f create_deployment.yaml
kubectl get deployments
```




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
