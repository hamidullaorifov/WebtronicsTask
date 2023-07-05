from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from database.db_setup import get_db
from typing import Annotated
from app.utils.auth import verify_password,create_access_token,get_hash_password,get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from database.db_setup import get_db
from app.models.users import User
from app.schemas.users import UserOut,UserCreate


router = APIRouter(prefix='/users',tags=['User'])
@router.post('/token')
async def get_access_token(request: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    username = request.username
    password = request.password
    user = db.query(User).filter(User.username==username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Incorrect username or password")
    if not verify_password(password,user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Incorrect username or password")
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/',response_model=UserOut,status_code=status.HTTP_201_CREATED)
async def create_user(request: UserCreate,db:Session = Depends(get_db)):
    user_data = request.dict()
    username = user_data.get('username')
    if db.query(User).filter(User.username==username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Username already exists")
    password = user_data.pop('password')
    hashed_password = get_hash_password(password)
    user = User(**user_data,password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user



