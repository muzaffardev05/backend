class DocumentService:

    def build_document(self, tender):

        department = tender.get("department") or "Unknown"

        return f"""
Title: {tender["title"]}

Organization: {tender["organization"]}

Department: {department}

Category: {tender["category"]}

Location: {tender["location"]}

Reference Number: {tender["reference_number"]}

Tender Number: {tender["tender_no"]}

Status: {tender.get("status", "Published")}

Published Date: {tender["publish_date"]}

Closing Date: {tender["closing_date"]}

Source Website: {tender["website"]}

Source URL: {tender["source_url"]}
""".strip()