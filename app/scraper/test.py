import logging
import time

from app.scraper.ppra_scraper import PPRAScraper
from app.scraper.ppra_parser import PPRAParser

from app.services.database_service import DatabaseService
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

EMBEDDING_BATCH_SIZE = 512


def scrape_and_prepare_documents(
    scraper,
    parser,
    db,
    document_service
):
    """
    Scrape PPRA, save tenders, generate documents,
    and mark changed tenders for re-embedding.
    """

    rows = scraper.scrape()

    logger.info("Scraped %s tenders", len(rows))

    new_tenders = 0
    changed_documents = 0

    for row in rows:

        tender = parser.parse(row)

        document = document_service.build_document(tender)

        db_tender = db.save_tender(
            tender=tender,
            document=document
        )

        if db_tender.created_at == db_tender.updated_at:
            new_tenders += 1

        if db.tender_changed(db_tender.tender_no):
            changed_documents += 1

    logger.info("New tenders       : %s", new_tenders)
    logger.info("Changed documents : %s", changed_documents)


def embed_pending_tenders(db):
    """
    Generate embeddings for all tenders where embedded=False.
    """

    pending = db.get_unembedded_tenders()

    if not pending:
        logger.info("No pending embeddings.")
        return

    logger.info("Pending tenders : %s", len(pending))

    embedding_service = EmbeddingService()
    vector_service = VectorService()

    total_batches = (
        len(pending) + EMBEDDING_BATCH_SIZE - 1
    ) // EMBEDDING_BATCH_SIZE

    total_vectors = 0

    for batch_number, start in enumerate(
        range(0, len(pending), EMBEDDING_BATCH_SIZE),
        start=1
    ):

        batch = pending[start:start + EMBEDDING_BATCH_SIZE]

        texts = [
            tender["text"]
            for tender in batch
        ]

        start_time = time.time()

        embeddings = embedding_service.generate_embeddings(texts)

        vector_service.add_vectors(
            batch,
            embeddings
        )

        db.mark_tenders_as_embedded(
            [t["id"] for t in batch]
        )

        elapsed = time.time() - start_time

        total_vectors += len(batch)

        logger.info(
            "Batch %s/%s | %s vectors | %.2fs",
            batch_number,
            total_batches,
            len(batch),
            elapsed
        )

    vector_service.save()

    logger.info("Vector index saved.")
    logger.info("Total vectors : %s", vector_service.total_vectors)
    logger.info("Metadata      : %s", len(vector_service.metadata))
    logger.info("Vectors added : %s", total_vectors)


def main():

    start_time = time.time()

    scraper = PPRAScraper()
    parser = PPRAParser()

    document_service = DocumentService()

    with DatabaseService() as db:

        try:

            logger.info("========== AI Tender Pipeline Started ==========")

            scrape_and_prepare_documents(
                scraper,
                parser,
                db,
                document_service
            )

            embed_pending_tenders(db)

            logger.info(
                "Completed successfully in %.2f seconds",
                time.time() - start_time
            )

        except Exception:

            logger.exception("Pipeline failed.")
            raise


if __name__ == "__main__":
    main()


# def scraper():

#     start_time = time.time()

#     scraper = PPRAScraper()
#     parser = PPRAParser()

#     document_service = DocumentService()

#     with DatabaseService() as db:

#         try:

#             logger.info("========== AI Tender Pipeline Started ==========")

#             scrape_and_prepare_documents(
#                 scraper,
#                 parser,
#                 db,
#                 document_service
#             )

#             embed_pending_tenders(db)

#             logger.info(
#                 "Completed successfully in %.2f seconds",
#                 time.time() - start_time
#             )

#         except Exception:

#             logger.exception("Pipeline failed.")
#             raise


