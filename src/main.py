from fastapi import FastAPI, HTTPException
from etcd3 import Etcd3Client
from pydantic import BaseModel
import os

app = FastAPI()

username = os.getenv('ETCD_USERNAME')
password = os.getenv('ETCD_PASSWORD')

# Create an etcd client
etcd_client = Etcd3Client(host='etcd-demo.default.svc.cluster.local', port=2379, user=username, password=password)

class Item(BaseModel):
    key: str
    value: str

@app.get("/get/{key}")
def get_value(key: str):
    try:
        result = etcd_client.get(key.encode())
        if result:
            value = result[0].decode()
            return {"key": key, "value": value}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error occurred during retrieval")
    raise HTTPException(status_code=404, detail="Key not found")

@app.post("/put")
def put_value(item: Item):
    try:
        etcd_client.put(item.key.encode(), item.value.encode())
        return {"key": item.key, "value": item.value}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error occurred during insertion")

@app.delete("/delete/{key}")
def delete_value(key: str):
    try:
        result = etcd_client.delete(key.encode())
        if result:
            return {"message": "Key deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error occurred during deletion")
    raise HTTPException(status_code=404, detail="Key not found")
