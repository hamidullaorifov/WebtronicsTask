from fastapi.security import OAuth2PasswordBearer
from fastapi import status,Depends,HTTPException
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime,timedelta


SECRET_KEY = "your-secret-key"  
ALGORITHM = "HS256"  
ACCESS_TOKEN_EXPIRE_MINUTES = 30



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username

def authenticate_user(username: str, password: str):
    # Add your logic here to authenticate the user
    # You can retrieve the user from a database or any other storage
    # Compare the provided username and password with the stored values
    # Return True if authentication succeeds, otherwise False
    return False


def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)



def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(data, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        # token_data = Token(username=username)
    except JWTError:
        raise credentials_exception



def get_hash_password(password):
    return pwd_context.hash(password)