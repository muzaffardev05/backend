class DocumentService:

    def build_document(self, tender):

        return f"""
    Website: {tender["website"]}

    Tender Number: {tender["tender_no"]}

    Reference Number: {tender["reference_number"]}

    Title:
    {tender["title"]}


    Organization:
    {tender["organization"]}

    Department:
    {tender["department"] if tender["department"] else "Unknown"}

    Category:
    {tender["category"]}

    Location:
    {tender["location"]}

    source_url:
    {tender["source_url"]}


    Published Date:
    {tender["publish_date"]}

    Closing Date:
    {tender["closing_date"]}




    """.strip()