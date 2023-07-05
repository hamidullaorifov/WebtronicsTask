from pydantic import BaseModel
from typing import List
from datetime import datetime

class PostIn(BaseModel):
    content: str

    class Config():
        orm_mode = True

class Post(BaseModel):
    id: int
    content: str
    updated_at: datetime
    created_at: datetime


    class Config():
        orm_mode = True
class PostOut(Post):
    owner_id:int
    likes: int = 0
    dislikes: int = 0