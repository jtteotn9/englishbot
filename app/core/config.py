import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN") or ""

if not BOT_TOKEN or BOT_TOKEN == "":
    raise ValueError("BOT_TOKEN не найден в файле .env!")

BOT_TOKEN: str = BOT_TOKEN
