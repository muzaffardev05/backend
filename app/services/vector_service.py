import os
import pickle
import faiss
import numpy as np


class VectorService:

    def __init__(self):

        self.dimension = 384           # BAAI/bge-small-en-v1.5

        self.index_path = "storage/tender.index"
        self.metadata_path = "storage/metadata.pkl"

        os.makedirs("storage", exist_ok=True)

        if os.path.exists(self.index_path):

            self.index = faiss.read_index(self.index_path)

            with open(self.metadata_path, "rb") as f:
                self.metadata = pickle.load(f)

        else:

            self.index = faiss.IndexFlatIP(self.dimension)

            self.metadata = []

    def add_vectors(self, chunks, embeddings):

        vectors = np.array(embeddings).astype("float32")

        self.index.add(vectors)

        for chunk in chunks:

            self.metadata.append({
                "tender_id": chunk["tender_id"],
                "chunk_index": chunk["chunk_index"],
                "text": chunk["chunk_text"]
            })

        self.save() 



    def save(self):

        faiss.write_index(self.index, self.index_path)

        with open(self.metadata_path, "wb") as f:
            pickle.dump(self.metadata, f)

    def search(self, query_embedding, top_k=5):

        query = np.array([query_embedding]).astype("float32")

        scores, indexes = self.index.search(query, top_k)

        results = []

        for score, idx in zip(scores[0], indexes[0]):

            if idx == -1:
                continue

            results.append({
                "score": float(score),
                **self.metadata[idx]
            })

        return results        
    

