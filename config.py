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


CLEARBIT_KEY = 'pk_f17d9626bd99938c6b742a3108a0de96'


EMAIL_HUNTER_API_KEY = '2f41980b39075899a766a53490a733cd505bca78'

EMAIL_HUNTER_API_ROOT = 'https://api.hunter.io/v2/email-verifier'
