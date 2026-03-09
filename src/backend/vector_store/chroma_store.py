import chromadb

client = chromadb.Client()

collection = client.get_or_create_collection(name="debate_memory")


def store_message(agent, text):
    collection.add(
        documents=[text], metadatas=[{"agent": agent}], ids=[str(hash(text))]
    )


def retrieve_context(query):
    results = collection.query(query_texts=[query], n_results=3)

    return results["documents"]
