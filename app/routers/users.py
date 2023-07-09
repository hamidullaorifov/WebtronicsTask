from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from database.db_setup import get_db
from app.utils.auth import verify_password,create_access_token,get_hash_password,verify_email
from fastapi.security import OAuth2PasswordRequestForm
from app.models.users import User
from app.schemas.users import UserOut,UserCreate


router = APIRouter(tags=['User'])

# Get access token
@router.post('/token')
async def get_access_token(request: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    username = request.username
    password = request.password

    user = db.query(User).filter(User.username==username).first()
    
    # Check username and password are correct
    if not user or not verify_password(password,user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Incorrect username or password")

    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}

# User registration
@router.post('/signup',response_model=UserOut,status_code=status.HTTP_201_CREATED)
async def create_user(request: UserCreate,db:Session = Depends(get_db)):
    username = request.username
    email = request.email
    
    # Check if the username already exists in the database
    if db.query(User).filter(User.username==username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Username already exists")
    
    # Check if the email already exists in the database
    if db.query(User).filter(User.email==email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already exists")
    
    # Email verification using emailhuter.co 
    email_verification = verify_email(email)

    if not email_verification['valid']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Email is {email_verification['message']}")

    hashed_password = get_hash_password(request.password)
    user = User(password=hashed_password,**request.dict(exclude={'password'}))

    # Save user to database
    db.add(user)
    db.commit()
    db.refresh(user)
    return user



