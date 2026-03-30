from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


EMBED_MODEL = "nomic-embed-text"


def build_vector_db(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(docs)

    embeddings = OllamaEmbeddings(model=EMBED_MODEL)

    vector_db = FAISS.from_documents(chunks, embeddings)
    return vector_db


def save_vector_db(vector_db, db_path):
    vector_db.save_local(db_path)


def load_vector_db(db_path):
    embeddings = OllamaEmbeddings(model=EMBED_MODEL)
    vector_db = FAISS.load_local(
        db_path,
        embeddings,
        allow_dangerous_deserialization=True
    )
    return vector_db