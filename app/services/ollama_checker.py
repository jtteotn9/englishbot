import httpx
import logging
import json
from ..interfaces import BaseAiChecker
from ..models import AnswerVerdict

SYSTEM_PROMPT = """
    Роль: «Ты — опытный учитель английского».
    Задача: «Тебе дают английское слово и перевод пользователя на русский. Проверь его».
    Уровни: «Определи уровень слова по шкале CEFR».
    Формат: «Отвечай ТОЛЬКО в формате JSON».
    Важно: Нужно добавить строчку: "Помни, что оригинальное слово — английское, а пользователь переводит его на русский язык".
    Ты ДОЛЖЕН ответить СТРОГО в формате JSON.
    Структура ответа:
    {
      "is_correct": boolean, // true, если перевод верный или является близким синонимом
      "comment": "строка с кратким пояснением на русском языке",
      "synonyms": ["synonym1", "synonym2"], // Strictly in English, 3-5 words, only direct synonyms
      "example": "All explanations in Russian, but synonyms and example-sentence base in English"
    }

    Никакого лишнего текста, только JSON.
    """


class OllamaAiChecker(BaseAiChecker):
    def __init__(self, model_name: str = "llama3"):
        self.model_name = model_name
        self.url = "http://localhost:11434/api/generate"

    async def check_answer(
        self, user_translation: str, original_word: str
    ) -> AnswerVerdict:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.url,
                    json={
                        "model": self.model_name,
                        "prompt": f"Word: {original_word}, Translation: {user_translation}",
                        "system": SYSTEM_PROMPT,
                        "stream": False,
                        "format": "json",
                    },
                )
                response.raise_for_status()

                result_data = response.json()
                ai_response_str = result_data.get("response", "")

                return AnswerVerdict.model_validate_json(ai_response_str)

        except (httpx.HTTPError, json.JSONDecodeError, Exception) as e:
            logging.error(f"Ollama error: {e}")

            return AnswerVerdict(
                is_correct=False,
                comment="Извини, мой ИИ-мозг немного перегрелся. Попробуй позже!",
                synonyms=[],
                example="Error occurred",
            )
