from langchain_text_splitters import RecursiveCharacterTextSplitter

class ChunkService:

    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )

    def chunk_documents(self, documents):

        chunks = []

        for document in documents:

            texts = self.splitter.split_text(document["text"])

            for index, text in enumerate(texts):
                chunks.append({
                    "tender_id": document["tender_id"],
                    "chunk_index": index,
                    "text": text
                })

        return chunks