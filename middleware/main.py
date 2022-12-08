from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from PIL import Image
import numpy as np
from elasticsearch import Elasticsearch
from feature_extractor import FeatureExtractor
import io
import uvicorn
import pickle as pk

es = Elasticsearch([{'host': "localhost", 'port': 9200, 'scheme': "http"}])
index = "image_se"
fe = FeatureExtractor()
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def root():
    return "Hello World"

@app.post('/vgg_query')
def vgg_query(image: UploadFile = File([]), size: Optional[int] = 10):
    pca = pk.load(open("C:/Users/med_g/OneDrive/Desktop/SUPCOM/DB Indexing & geospacial applications/elasticsearch/img_engine/search_engine/middleware/utils/pca.pkl", 'rb')) #"./utils/pca.pkl",'rb'))
    image = Image.open(io.BytesIO(image.file.read()))
    features = fe.extract(image)
    reducedFeatures = pca.transform([features])
    reducedFeatures = list(reducedFeatures[0])
    body = {
        "query": {
            "elastiknn_nearest_neighbors": {
                "vec": reducedFeatures,
                "field": "feature_vector",
                "similarity": "l2",
                "model": "exact",
            }
        }
    }
    res = es.search(index=index, body=body, size = size)
    return res['hits']['hits']

if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='localhost')