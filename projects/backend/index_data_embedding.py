import json
import torch

from tqdm import tqdm
from typing import List
from utils import get_es_client
from elasticsearch import Elasticsearch
from config import INDEX_NAME_EMBEDDING

from sentence_transformers import SentenceTransformer

def index_data(documents: List[dict], model: SentenceTransformer) -> None:
    es = get_es_client(max_retries=1, sleep_time=0)
    _create_index(es=es)
    _insert_document(es=es, documents=documents, model=model)


def _create_index(es: Elasticsearch) -> dict:
    settings = {
        "index": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }
    }

    mappings = {
        "properties": {
            "embedding": {
                "type": "dense_vector",
                "dims": 384
            }
        }
    }
    es.indices.delete(index=INDEX_NAME_EMBEDDING, ignore_unavailable=True)
    return es.indices.create(index=INDEX_NAME_EMBEDDING,  mappings=mappings, settings=settings)


def _insert_document(es: Elasticsearch, documents: List[dict], model:SentenceTransformer):
    operations = []
    for document in tqdm(documents, total=len(documents), desc="Indexing documents"):
        operations.append({"index": { "_index": INDEX_NAME_EMBEDDING }})
        operations.append({
            **document,
            "embedding": model.encode(document["explanation"])
        })
    return es.bulk(operations=operations)



if __name__ == "__main__":
    with open("../../data/apod.json") as file:
        documents = json.load(file)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = SentenceTransformer("all-MiniLM-L6-v2").to(device)
    index_data(documents=documents, model=model)
