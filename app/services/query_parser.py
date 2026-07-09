import re

from app.data.locations import LOCATIONS
from app.data.stopwords import QUERY_STOPWORDS
class QueryParser:
    def __init__(self):
        self.locations=LOCATIONS
        

    def _extract_locations(self, text: str):
        found=[]
        remaining=text
        lower=text.lower()
        for canonical,aliases in self.locations.items():
            for alias in aliases:
                pattern=r"\b{}\b".format(re.escape(alias))
                if re.findall(pattern,lower):
                    found.append(canonical)
                    remaining=re.sub(pattern,"",remaining,flags=re.IGNORECASE)
                    break

        remaining=re.sub(r"\s+"," ",remaining).strip()
        return found,remaining   

    def _clean_query(self,text:str):
        words=re.findall(r"\w+",text.lower())
        clean=[]
        for word in words:
            if word.lower() in QUERY_STOPWORDS:
                continue
            clean.append(word)
        return " ".join(clean)

    def parse(self,question:str):
        original=question.strip()
        semantic_query=self._clean_query(original)

        filters={
            "location":[],
            "category":[],
            "organization":[],
            "status":[],
            "publish_date":None,
            "closing_date":None,
            "expired":None,
            "tender_no":None,

        }
        locations,semantic_query=self._extract_locations(semantic_query)
        filters["location"]=locations
        return {
            "semantic_query":semantic_query,
            "filters":filters,
        }
    




parser = QueryParser()

print(
    parser.parse(
        "Firewall and IDS tenders in Islamabad and khi published in the last 30 days"
    )
)