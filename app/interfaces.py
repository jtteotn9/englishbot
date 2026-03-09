from abc import ABC, abstractmethod
from .models import AnswerVerdict


class BaseAiChecker(ABC):
    """Base interface for type checking."""

    @abstractmethod
    async def check_answer(
        self, user_translation: str, original_word: str
    ) -> AnswerVerdict:
        """Returns answer's verdict"""
        pass
