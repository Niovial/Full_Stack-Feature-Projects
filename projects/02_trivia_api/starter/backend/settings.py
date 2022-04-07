import os
from dotenv import load_dotenv


load_dotenv()

db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")
db_host = os.environ.get("DB_HOST")
db_name = os.environ.get("DB_NAME")
db_path = "postgresql://{}:{}@{}/{}".format(db_user, db_password,
                    db_host, db_name)
