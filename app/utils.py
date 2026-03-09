import json
import random


def get_random_word():
    try:
        with open("words.json", "r", encoding="utf-8") as f:
            words = json.load(f)  # Теперь это просто список ["word1", "word2", ...]

        if not words:
            return "apple"  # Запасное слово

        return random.choice(words)  # Возвращает просто строку, например "Internet"
    except:
        return "error"
