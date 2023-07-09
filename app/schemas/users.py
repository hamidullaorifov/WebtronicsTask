from pydantic import BaseModel,EmailStr
from typing import List
from app.schemas.posts import Post

class UserBase(BaseModel):
    username: str
    email:EmailStr
    first_name: str = ""
    last_name: str = ""

    class Config():
        orm_mode = True


class UserCreate(UserBase):
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    first_name: str = ""
    last_name: str = ""

    class Config():
        orm_mode = True


    
