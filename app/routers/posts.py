from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session
from database.db_setup import get_db
from app.utils.auth import get_current_user
from fastapi.security import OAuth2PasswordBearer
from app.models.users import User
from app.models.posts import Post
from app.schemas.posts import PostIn,PostOut
from typing import Optional,Annotated
router = APIRouter(prefix='/posts',tags=['Post'])

@router.post('',response_model=PostOut, status_code=status.HTTP_201_CREATED)
async def create_post(
        request: PostIn,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
    
    post = Post(content=request.content,owner_id=current_user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post
    
