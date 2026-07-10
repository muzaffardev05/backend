

class ContextBuilder:

    def build(self,tenders):
        contexts=[]
        for i, tender in enumerate(tenders,start=1):
            contexts.append(f"""
Tender {i}

Tender no:
{tender.get("tender_id")}

Title:
{tender.get("title")}

Organization:
{tender.get("organization")}

Department:
{tender.get("department")}

Location:
{tender.get("location")}

Publish Date:
{tender.get("publish_date")}

Closing Date:
{tender.get("closing_date")}

Status:
{tender.get("status")}




""")
            
        return "\n".join(contexts)