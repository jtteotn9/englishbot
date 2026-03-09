import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from app.core.config import BOT_TOKEN
from app.services.ollama_checker import OllamaAiChecker
from app.models import PracticeSession
from app.utils import get_random_word


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

checker = OllamaAiChecker()

active_session: dict[int, PracticeSession] = {}


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if not message.from_user:
        return

    user_id = message.from_user.id
    word_to_learn = "apple"

    active_session[user_id] = PracticeSession(
        user_id=user_id, original_word=word_to_learn
    )

    await message.answer(f"Как переводится слово {word_to_learn}?")


@dp.message()
async def handle_translation(message: types.Message):
    if not message.from_user:
        return

    user_id = message.from_user.id

    session = active_session.get(user_id)
    if not session:
        await message.answer("Напиши /start, что бы начать упражнение")
        return

    if not message.text:
        return

    verdict = await checker.check_answer(
        user_translation=message.text, original_word=session.original_word
    )

    next_word_data = get_random_word()

    session.original_word = next_word_data

    if verdict.is_correct:
        text = (
            f"✅ Верно!\n\n"
            f"{verdict.comment}\n\n"
            f"📚 Синонимы: {', '.join(verdict.synonyms)}\n"
            f"💡 Пример: {verdict.example}"
        )
    else:
        text = f"❌ Не совсем так...\n\n{verdict.comment}"

    await message.answer(
        f"{text}\nСледующее слово: <b>{session.original_word}</b>", parse_mode="HTML"
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main=main())
