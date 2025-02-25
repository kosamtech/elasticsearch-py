import time

from elasticsearch import Elasticsearch


def get_es_client(max_retries: int = 1, sleep_time: int = 5) -> Elasticsearch:
    i = 0
    while i < max_retries:
        try:
            es = Elasticsearch(hosts="http://localhost:9200")
            print("Connected to Elasticseach!")
            return es
        except Exception:
            print("Could not connect to Elasticsearch, retrying...")
            time.sleep(sleep_time)
            i += 1
    raise ConnectionError(f"Failed to connect to Elasticsearch after {i + 1} attemps")
