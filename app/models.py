from pydantic import BaseModel
from dataclasses import dataclass
from typing import List


class AnswerVerdict(BaseModel):
    """AI model's answer"""

    is_correct: bool
    comment: str
    synonyms: List[str] = []
    example: str = ""


@dataclass
class PracticeSession:
    """Current user's word data"""

    user_id: int
    original_word: str
