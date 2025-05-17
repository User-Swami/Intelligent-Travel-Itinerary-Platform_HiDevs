import chromadb

client = chromadb.Client()
collection = client.get_or_create_collection(name="itinerary_queries")

def add_to_store(query, answer):
    collection.add(documents=[answer], ids=[query], metadatas=[{"query": query}])

def search_similar_queries(query):
    result = collection.query(query_texts=[query], n_results=1)
    if result['documents']:
        return result['documents'][0][0]
    return None