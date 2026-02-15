from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, Literal
from typing import Optional


class TriageCreate(BaseModel):
    external_id: str
    answers: Dict[str, Any]
