from dotenv import load_dotenv
import os


load_dotenv()


DATABASE_URL = "sqlite:///./sql_app.db"

SECRET_KEY = os.getenv('SECRET_KEY')  
ALGORITHM = os.getenv('ALGORITHM')
try:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
except:
    ACCESS_TOKEN_EXPIRE_MINUTES = 30