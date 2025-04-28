from langchain_voyageai import VoyageAIEmbeddings
import os
from dotenv import load_dotenv
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility


def create_collection(dim: int):
    collection_name = "vectorized_articles_collection"
    connections.connect("default", host="localhost", port="19530")
    if utility.has_collection(collection_name):
        utility.drop_collection(collection_name)

    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="postgres_id", dtype=DataType.INT64),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=dim),
        FieldSchema(name="embedding_type", dtype=DataType.VARCHAR, max_length=255)
    ]

    schema = CollectionSchema(fields, description="vectorized_articles_collection")
    collection = Collection(name=collection_name, schema=schema)

    index_params = {
        "metric_type": "COSINE",
        "index_type": "IVF_FLAT",
        "params": {"nlist": 512}
    }

    collection.create_index(field_name="embedding", index_params=index_params)

    collection.flush()
    collection.load()

    return collection


if __name__ == '__main__':
    create_collection(dim=512)
