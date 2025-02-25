import json

from tqdm import tqdm
from typing import List
from utils import get_es_client
from elasticsearch import Elasticsearch
from config import INDEX_NAME_DEFAULT, INDEX_NAME_N_GRAM


def index_data(documents: List[dict], use_n_gram_tokenizer: bool):
    es = get_es_client(max_retries=5)
    _create_index(es=es, use_n_gram_tokenizer=use_n_gram_tokenizer)
    _insert_document(es=es, documents=documents, use_n_gram_tokenizer=use_n_gram_tokenizer)

    index_name = INDEX_NAME_N_GRAM if use_n_gram_tokenizer else INDEX_NAME_DEFAULT
    print(f"Indexed {len(documents)} documents into elasticsearch index {index_name}")


def _create_index(es: Elasticsearch, use_n_gram_tokenizer: bool) -> dict:
    tokenizer = "n_gram_tokenizer" if use_n_gram_tokenizer else "standard"
    index_name = INDEX_NAME_N_GRAM if use_n_gram_tokenizer else INDEX_NAME_DEFAULT

    body = {
        "settings": {
            "analysis": {
                "analyzer": {
                    "default": {
                        "type": "custom",
                        "tokenizer": tokenizer
                    }
                },
                "tokenizer": {
                    "n_gram_tokenizer": {
                        "type": "edge_ngram",
                        "min_gram": 1,
                        "max_ngram": 30,
                        "token_chars": ["letter", "digit"]
                    }
                }
            },
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            }
        }
    }

    es.indices.delete(index=index_name, ignore_unavailable=True)
    return es.indices.create(index=index_name,body=body)


def _insert_document(es: Elasticsearch, documents: List[dict], use_n_gram_tokenizer: bool) -> dict:
    operations = []
    index_name = INDEX_NAME_N_GRAM if use_n_gram_tokenizer else INDEX_NAME_DEFAULT
    for document in tqdm(documents, total=len(documents), desc="Indexing documents"):
        operations.append({"index": {"_index": index_name}})
        operations.append(document)
    return es.bulk(operations=operations)

if __name__ == "__main__":
    documents = json.load(open("../../data/apod.json"))
    index_data(documents=documents, use_n_gram_tokenizer=True)