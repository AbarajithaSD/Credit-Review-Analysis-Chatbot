import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    GROQ_MODEL = os.getenv(
        "GROQ_MODEL",
        "qwen/qwen3.8-27b"
    )

    GROQ_WEB_MODEL = os.getenv(
        "GROQ_WEB_MODEL",
        "groq/compound"
    )

    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

    SECRET_KEY = os.getenv("FLASK_SECRET_KEY")