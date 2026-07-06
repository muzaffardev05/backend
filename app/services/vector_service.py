import os
import pickle

import faiss
import numpy as np


class VectorService:

    def __init__(self):

        self.dimension = 384

        self.index_path = "app/storage/tender.index"
        self.metadata_path = "app/storage/metadata.pkl"

        os.makedirs("app/storage", exist_ok=True)

        self.load()

    def load(self):

        if os.path.exists(self.index_path):

            self.index = faiss.read_index(self.index_path)

            with open(self.metadata_path, "rb") as f:
                self.metadata = pickle.load(f)

        else:

            self._create_new_index()

    def _create_new_index(self):

        M = 32

        self.index = faiss.IndexHNSWFlat(
            self.dimension,
            M,
            faiss.METRIC_INNER_PRODUCT
        )

        self.index.hnsw.efConstruction = 200
        self.index.hnsw.efSearch = 128

        self.metadata = []

    def reset(self):
        """
        Create a brand new empty index.
        Useful when rebuilding all embeddings.
        """
        self._create_new_index()

    def add_vectors(self, tenders, embeddings):

        vectors = np.asarray(
            embeddings,
            dtype=np.float32
        )

        if vectors.ndim == 1:
            vectors = vectors.reshape(1, -1)

        if vectors.shape[1] != self.dimension:
            raise ValueError(
                f"Expected {self.dimension} dimensions, got {vectors.shape[1]}"
            )

        # Normalize for cosine similarity
        faiss.normalize_L2(vectors)

        self.index.add(vectors)

        self.metadata.extend([
            {
                "tender_id": tender["tender_id"],
                "title": tender["title"],
                "organization": tender["organization"],
                "publish_date": tender["publish_date"],
                "closing_date": tender["closing_date"],
                "location": tender["location"],
                "status": tender["status"],
                "category": tender["category"],

            }
            for tender in tenders
        ])

    def save(self):

        faiss.write_index(
            self.index,
            self.index_path
        )

        with open(
            self.metadata_path,
            "wb"
        ) as f:

            pickle.dump(
                self.metadata,
                f,
                protocol=pickle.HIGHEST_PROTOCOL
            )

    def search(
        self,
        query_embedding,
        top_k=5
    ):

        query = np.asarray(
            query_embedding,
            dtype=np.float32
        ).reshape(1, -1)

        faiss.normalize_L2(query)

        scores, indexes = self.index.search(
            query,
            top_k
        )

        results = []

        for score, idx in zip(
            scores[0],
            indexes[0]
        ):

            if idx == -1:
                continue

            results.append({
                "score": float(score),
                **self.metadata[idx]
            })

        return results

    @property
    def total_vectors(self):

        return self.index.ntotal