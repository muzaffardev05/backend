from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class RetrievalContext:

    query: str

    documents: list
    prompt_context:str

    created_at: datetime = field(default_factory=datetime.now)