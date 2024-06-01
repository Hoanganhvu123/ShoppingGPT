import os
import json
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS

os.environ["GOOGLE_API_KEY"] = "AIzaSyClbPvcvemX2qE4cWuizhc5sgnxTIbIwkk"

class SearchModule:
    def __init__(self, verbose=False):
        index_name = "guides_faiss_index"
        model_name = "sentence-transformers/all-mpnet-base-v2"
        embeddings = HuggingFaceEmbeddings(model_name=model_name)

        if os.path.isdir(index_name):
            print("load local faiss index")
            self.db = FAISS.load_local(index_name, embeddings)
        else:
            file_path = 'data/guides.json'
            guides = {}
            with open(file_path, 'r') as f:
                guides = json.load(f)
            print(f"Loaded {len(guides)} buying guides")

            text_splitter = CharacterTextSplitter(separator="\n")
            docs = []
            for name, guide in guides.items():
                text = text_splitter.split_text(guide)
                docs.extend([Document(page_content=t) for t in text])
            print(f"Processed {len(docs)} docs")

            self.db = FAISS.from_documents(docs, embeddings)
            self.db.save_local(index_name)
        print("Loaded knowledge db")

    def top_docs(self, query: str, k: int = 4):
        top_documents = self.db.similarity_search(query, k=k)
        return top_documents