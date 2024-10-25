import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('PGUSER')}:{os.getenv('PGPASSWORD')}@{os.getenv('PGHOST')}:{os.getenv('PGPORT')}/{os.getenv('PGDATABASE')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False