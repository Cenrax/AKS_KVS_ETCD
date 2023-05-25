## How did I created the kubernetes cluster

- Created a Kubernetes cluster in Azure
    ```
    az aks create --resource-group <resource_group_name> --name <cluster_name> --location "Central India" --node-count <node_count> --node-vm-size <vm_size> --enable-addons monitoring 
    ```
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
kubectl apply -f create_pvc.yaml (using azure file managed service for faster processing we can use the premium services too)
kubectl apply -f create_deployment.yaml
kubectl get deployments
```

Now we need to create the service
```
kubectl apply -f create_service.yaml
kubectl get svc 
```
Please note the external IP

Now in a browser put http://<<external-ip>>:80/docs
    
We will be able to see the documentation
<img width="909" alt="image" src="https://github.com/Cenrax/AKS_KVS_ETCD/assets/43017632/803612b4-6352-4323-87f8-57b2c448d129">



## Setup of the local development environment
    ```
    docker pull quay.io/coreos/etcd
    
    docker run -d --name my-etcd -p 2379:2379 -p 2380:2380 quay.io/coreos/etcd:latest /usr/local/bin/etcd --advertise-client-urls http://0.0.0.0:2379 --listen-client-urls http://0.0.0.0:2379 --initial-advertise-peer-urls http://0.0.0.0:2380 --listen-peer-urls http://0.0.0.0:2380 --initial-cluster-token etcd-cluster-1 --initial-cluster my-etcd=http://0.0.0.0:2380 --initial-cluster-state new

    docker run -d --name my-etcd -p 2379:2379 -p 2380:2380 -e ETCD_ADVERTISE_CLIENT_URLS=http://localhost:2379 -e ETCD_ROOT_PASSWORD=<your_password> bitnami/etcd:latest
    ```

### Locally check if the setup is successfull
```
etcdctl --endpoints=localhost:2379 --user root --password <your_password> endpoint health
```
    
### In the main.py file replace this 

```
username = os.getenv('ETCD_USERNAME')
password = os.getenv('ETCD_PASSWORD')
etcd_client = Etcd3Client(host='my-etcd.default.svc.cluster.local', port=2379, user=username, password=password)
    
```
with
```
etcd_client = Etcd3Client(host='127.0.0.1', port=2379, user='root', password=<your-password>)
    
    
