import voyageai
import os
from dotenv import load_dotenv
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility


EMBEDDING_DIM = 1024


def create_collection(dim: int = EMBEDDING_DIM):
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


def retrieve_collection(host="localhost", port="19530", collection_name='vectorized_articles_collection'):
    connections.connect("default", host=host, port=port)
    if not utility.has_collection(collection_name):
        print('No collection found')
        return None
    collection = Collection(name=collection_name)
    collection.load()
    return collection


def similarity_search(embeddings, embedding_type: str, top_k: int = 5, threshold: float = 0.5):
    load_dotenv()

    collection = retrieve_collection()
    search_params = {
        "metric_type": "COSINE",
        "index_type": "IVF_FLAT",
        "params": {"nlist": 128}
    }
    expr = f"embedding_type == '{embedding_type}'"

    results = collection.search(
        data=embeddings,
        anns_field='embedding',
        param=search_params,
        limit=top_k,
        expr=expr,
        output_fields=['postgres_id', 'embedding', 'embedding_type'],
    )

    similar_entries = []
    for hits in results:
        for hit in hits:
            if hit.distance > threshold:
                similar_entries.append({
                    'id': hit.id,
                    'postgres_id': hit.postgres_id,
                    'similarity_score': hit.distance,
                    'embedding_type': hit.embedding_type,
                })
    return similar_entries


def insert_article(postgres_id: int, embedding: list, embedding_type: str):
    collection = retrieve_collection()
    data = [
        [postgres_id],
        [embedding],
        [embedding_type]
    ]
    field_names = ['postgres_id', 'embedding', 'embedding_type']
    collection.insert(data, field_names=field_names)
    collection.flush()


if __name__ == '__main__':
    create_collection()
