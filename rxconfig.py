import reflex as rx
import os
from dotenv import load_dotenv

load_dotenv()

config = rx.Config(
    app_name="lahacks2024",
    db_url=os.getenv("POSTGRES_URL")
)