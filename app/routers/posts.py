from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from database.db_setup import get_db
from app.utils.auth import get_current_user
from fastapi.security import OAuth2PasswordBearer
from app.models.users import User
from app.models.posts import Post
from app.schemas.posts import PostIn,PostOut
from typing import Optional,Annotated,List
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
    

@router.get('', response_model=List[PostOut])
async def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return posts


@router.get('/{id}',response_model=PostOut)
async def get_post(id:int,db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id==id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Post not found')
    return post

@router.put('/{id}',response_model=PostOut)
async def update_post(
    id:int,
    request:PostIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    post = db.query(Post).filter(Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Post not found')

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    try:
        post.content = request.content
        db.commit()
        db.refresh(post)
    except:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Database error")
    return post




@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    id:int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    post = db.query(Post).filter(Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Post not found')

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    try:
        db.delete(post)
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Database error")
    return {"message":"Post deleted"}

