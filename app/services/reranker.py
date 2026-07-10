# from sentence_transformers import CrossEncoder


# class Reranker:

#     def __init__(self):

#         self.model = CrossEncoder(
#             "BAAI/bge-reranker-v2-m3"
#         )

#     def rerank(
#         self,
#         query,
#         results
#     ):

#         pairs = []

#         for tender in results:

#             text = " ".join([
#                 tender.get("title", ""),
#                 tender.get("description", ""),
#                 tender.get("organization", ""),
#                 tender.get("location", "")
#             ])

#             pairs.append((query, text))

#         scores = self.model.predict(pairs)

#         for tender, score in zip(results, scores):

#             tender["rerank_score"] = float(score)

#         results.sort(
#             key=lambda x: x["rerank_score"],
#             reverse=True
#         )

#         return results