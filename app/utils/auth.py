from fastapi import status,Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt,ExpiredSignatureError
from datetime import datetime,timedelta
from app.models.users import User
from database.db_setup import SessionLocal
import requests
import config

SECRET_KEY = config.SECRET_KEY  
ALGORITHM = config.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = config.ACCESS_TOKEN_EXPIRE_MINUTES



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Verifying email using emailhunter 
def verify_email(email:str):
    response = requests.get(
        url=config.EMAIL_HUNTER_API_ROOT,
        params={
            "email":email,
            "api_key":config.EMAIL_HUNTER_API_KEY
            }
        )

    result = {"valid":True,"message":""}
    if response.ok:
        response_data = response.json()

        data = response_data.get("data")
        email_status = data.get("status")

        if email_status == "invalid" or email_status == "disposable":
            result["valid"] = False
            result["message"] = email_status
            return result

        # Check if email is disposable
        if data.get("disposable"):
            result["valid"] = False
            result["message"] ="disposable"
        return result

    elif response.status_code == 400:
        result["valid"] = False
        result["message"] = "invalid"

    else:
        raise HTTPException(status_code=response.status_code)





def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)



def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str=Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception
        
        with SessionLocal() as db:
            user = db.query(User).filter(User.username==username).first()
        
        if not user:
            raise credentials_exception
        return user

    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token has expired")
    except JWTError:
        raise credentials_exception
    



def get_hash_password(password):
    return pwd_context.hash(password)