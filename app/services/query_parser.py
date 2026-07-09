import re
from datetime import date
from app.data.locations import LOCATIONS
from app.data.stopwords import QUERY_STOPWORDS
from app.utils.date_parser import DateParser
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


    def _extract_publish_date(self, text):

        lower = text.lower()

        remaining = text

        publish = None

        patterns = [

            (
                r"\bpublished\s+today\b",
                DateParser.today
            ),

            (
                r"\btoday\b",
                DateParser.today
            ),

            (
                r"\bpublished\s+yesterday\b",
                DateParser.yesterday
            ),

            (
                r"\byesterday\b",
                DateParser.yesterday
            ),

            (
                r"\bthis\s+week\b",
                DateParser.this_week
            ),

            (
                r"\blast\s+week\b",
                DateParser.last_week
            ),

            (
                r"\bthis\s+month\b",
                DateParser.this_month
            )

        ]

        for pattern, func in patterns:

            if re.search(pattern, lower):

                publish = {}

                publish["from"], publish["to"] = func()

                remaining = re.sub(
                    pattern,
                    " ",
                    remaining,
                    flags=re.IGNORECASE
                )

                break
                
        if publish is None:
            match=re.search(r"(?:published\s+)?after\s(.+)",lower,flags=re.IGNORECASE)
            if match:
                d=DateParser.parse_date(match.group(1))
                if d:
                    publish={
                        "from":d,
                        "to":date.max
                    }
                    remaining=re.sub(r"(?:published\s+)?after\s+.+"," ",remaining,flags=re.IGNORECASE)
        
        if publish is None:
            match=re.search(r"(?:published\s+)?before\s+(.+)",lower)
            if match:
                d=DateParser.parse_date(match.group(1))
                if d:
                    publish={
                        "from":date.min,"to":d
                    }
                    remaining=re.sub(r"(?:published\s+)?before\s+.+"," ",remaining,flags=re.IGNORECASE)
        


        if publish is None:
            match=re.search(r"(?:published\s+)?between\s+(.+?)\s+and\s(.+)",lower,flags=re.IGNORECASE)
            if match:
                d1=DateParser.parse_date(match.group(1))
                d2=DateParser.parse_date(match.group(2))
                if d1 and d2:
                    publish={
                        "from":min(d1,d2),
                        "to":max(d1,d2)
                    }
                    remaining=re.sub(r"(?:published\s+)?between\s+(.+?)\s+and\s+(.+)"," ",remaining,flags=re.IGNORECASE)

        if publish is None:
            match=re.search(r"(?:published\s+)?on\s+(.+)",lower,flags=re.IGNORECASE)
            if match:
                d=DateParser.parse_date(match.group(1))
                if d:
                    publish={
                        "from":d,
                        "to":d
                    }
                    remaining=re.sub(r"(?:published\s+)?on\s+.+","",remaining,flags=re.IGNORECASE)
        remaining = re.sub(r"\s+", " ", remaining).strip()
        return publish, remaining


    def _extract_closing_date(self,text):
        lower=text.lower()
        remaining=text
        closing=None
        patterns = [

                    (
                        r"\bclosing\s+today\b",
                        DateParser.today
                    ),

                    (
                        r"\bclosing\s+tomorrow\b",
                        DateParser.tomorrow
                    ),

                    (
                        r"\bclosing\s+yesterday\b",
                        DateParser.yesterday
                    ),

                    (
                        r"\bclosing\s+this\s+week\b",
                        DateParser.this_week
                    ),

                    (
                        r"\bclosing\s+last\s+week\b",
                        DateParser.last_week
                    ),

                    (
                        r"\bclosing\s+this\s+month\b",
                        DateParser.this_month
                    )
                      ]
        for pattern, func in patterns:

            if re.search(pattern, lower):

                f, t = func()

                closing = {
                    "from": f,
                    "to": t
                }

                remaining = re.sub(
                    pattern,
                    " ",
                    remaining,
                    flags=re.I
                )

                break

        if closing is None:
            match=re.search(r"closing\s+after\s+(.+)",lower)
            if match:
                d=DateParser.parse_date(match.group(1))
                if d:
                    closing={
                        "from":d,
                        "to":date.max
                    }
                    remaining=re.sub(r"closing\s+after\s+.+"," ", remaining,flags=re.I)

        if closing is None:
            match=re.search(r"closing\s+before\s+(.+)",lower)
            if match:
                d=DateParser.parse_date(match.group(1))
                if d:
                    closing={
                        "from":date.min,
                        "to":d
                    } 
                    remaining=re.sub(r"closing\s+before\s+.+"," ",remaining,flags=re.I)       

        if closing is None:
            match=re.search(r"closing\s+on\s+(.+)",lower)
            if match:
                d=DateParser.parse_date(match.group(1))
                if d:
                    closing={
                        "from":d,
                        "to":d
                    }
                    remaining=re.sub(r"closing\s+on\s+.+"," ",remaining,flags=re.I)
        if closing is None:
            match=re.search(r"closing\s+between\s+(.+?)\s+and\s+(.+)",lower)     
            if match:
                d1=DateParser.parse_date(match.group(1)
                )
                d2=DateParser.parse_date(match.group(2))
                if d1 and d2:
                    closing={
                        "from":min(d1,d2),
                        "to":max(d1,d2)
                    }
                    remaining=re.sub(r"closing\s+between\s+.+"," ",remaining,flags=re.I)
        remaining=re.sub(r"\s+"," ",remaining).strip()

        return closing,remaining
    
    def parse(self,question:str):
        original=question.strip()
        print("orignal",original)
        semantic_query=original
        
     

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
        closing, semantic_query = self._extract_closing_date(
            semantic_query
        )

        filters["closing_date"] = closing
        publish, semantic_query = self._extract_publish_date(
    semantic_query
)
        filters['publish_date']=publish
        semantic_query=self._clean_query(semantic_query)
        return {
            "semantic_query":semantic_query,
            "filters":filters,
        }
    




parser = QueryParser()

print(
    parser.parse(
        "Cyber security tenders closing between July 1 and July 10"
    )
)