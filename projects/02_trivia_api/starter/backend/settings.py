import os
from dotenv import load_dotenv


load_dotenv()

db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")
