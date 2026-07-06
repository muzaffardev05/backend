import os
import torch
from sentence_transformers import SentenceTransformer


class EmbeddingService:

    def __init__(self):

        cpu_count = os.cpu_count()

        torch.set_num_threads(cpu_count)
        torch.set_num_interop_threads(cpu_count)

        print(f"Using {cpu_count} CPU threads")

        self.model = SentenceTransformer(
            "BAAI/bge-small-en-v1.5",
            device="cpu"
        )

    def generate_embeddings(self, texts):

        return self.model.encode(
            texts,
            batch_size=512,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False
        )