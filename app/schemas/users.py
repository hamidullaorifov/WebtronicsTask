from pydantic import BaseModel
from typing import List
from app.schemas.posts import Post

class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str

    class Config():
        orm_mode = True


class UserCreate(UserBase):
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str

    class Config():
        orm_mode = True


class UserDetails(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str

    class Config():
        orm_mode = True
    posts: List[Post] = []
    liked_posts: List[Post] = []
    disliked_posts: List[Post] = []
