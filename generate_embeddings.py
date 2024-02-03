import os

os.environ["OPENAI_API_KEY"] = "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"

from llama_index import VectorStoreIndex, SimpleDirectoryReader,  StorageContext, load_index_from_storage

def meeting_vector_index(dir_name):
    PERSIST_DIR = "./storage/"+dir_name
    if not os.path.exists(PERSIST_DIR):
        # load the documents and create the index
        documents = SimpleDirectoryReader(dir_name).load_data()
        index = VectorStoreIndex.from_documents(documents)
        # store it for later
        index.storage_context.persist(persist_dir=PERSIST_DIR)
    else:
        # load the existing index
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context)

    return index

