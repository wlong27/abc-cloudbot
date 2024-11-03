from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client.http import models
import json

embedding_model = None
qdrant_client = None
collection_name = "first_collection"
try:
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    qdrant_client = QdrantClient(":memory:")
    qdrant_client.recreate_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=384,
            distance=models.Distance.COSINE
        )
    )
  
except Exception as e:
    print(f'Failed initialization of Qdrant {e}')

def embed_documents(documents):
    embeddings = [embedding_model.embed_query(doc) for doc in documents]
    qdrant_client.upsert(
        collection_name=collection_name,
        points=[PointStruct(id=i, vector=embedding, payload={"content": documents[i]}) for i, embedding in enumerate(embeddings)]
    )
    
def embed_json_chunks(json_list, metadata=None):
    points = []
    for chunk in json_list:
        if isinstance(chunk, dict):
            chunk_str = json.dumps(chunk)
        else:
            chunk_str = chunk
        
        embedding = embedding_model.embed_query(chunk_str)
        chunk_metadata = { "original_json": chunk_str }       
        if metadata:
            chunk_metadata.update(metadata)
            
        point = models.PointStruct(
            id=qdrant_client.count(collection_name).count,
            vector=embedding,
            payload=chunk_metadata
        )
        points.append(point)
    qdrant_client.upsert(collection_name=collection_name, points=points)        

def embed_json(json_list, json_key=None, metadata=None):
    points = []
    id_key = qdrant_client.count(collection_name).count
            
    for json_obj in json_list:        
        if json_key:
            embedded_content = json_obj[json_key]          
        else:
            embedded_content = json_obj['content'] 
        
        embeddings = embedding_model.embed_query(embedded_content)
        if metadata:
            json_obj.update(metadata)

        point = models.PointStruct(
            id=id_key,
            vector=embeddings,
            payload=json_obj
        )
        points.append(point)
        id_key += 1        
    qdrant_client.upsert(collection_name=collection_name, points=points)        

def search_qdrant(query):
    query_embedding = embedding_model.embed_query(query)
    search_results = qdrant_client.search(
        collection_name= collection_name,
        query_vector = query_embedding,
        limit = 5
    )
    
    retrieved_docs = [hit.payload for hit in search_results]
    return retrieved_docs


def retrieve_context(user_query):
    retrieved_docs = search_qdrant(user_query)
    return retrieved_docs
    # if isinstance(retrieved_docs, list) and all(isinstance(item, str) for item in retrieved_docs):
    #     context = "\n".join(retrieved_docs)
    # elif isinstance(retrieved_docs, list) and all(isinstance(item, dict) for item in retrieved_docs):
    #     context = retrieved_docs