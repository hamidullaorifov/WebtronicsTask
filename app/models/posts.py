from sqlalchemy import Column,Integer,String,ForeignKey,DateTime,Boolean,Table
from database.db_setup import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.db_setup import SessionLocal
from app.utils.cache import set_likes,set_dislikes,get_likes,get_dislikes

# Table for user likes and dislikes
user_reactions_table = Table(
    'user_reactions',
    Base.metadata,
    Column('is_like',Boolean,nullable=False),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('post_id', Integer, ForeignKey('posts.id'))
)


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    content = Column(String)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    updated_at = Column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())

    reacting_users = relationship('User',secondary=user_reactions_table,back_populates='reacted_posts')


    @property
    def likes(self):

        post_likes = get_likes(self.id)

        # If post likes is not set in the cache 
        if not post_likes:
            with SessionLocal() as db:
                post_likes = db.query(user_reactions_table).filter_by(is_like = True,post_id = self.id).count()
            set_likes(self.id,post_likes)

        return post_likes 
    
    @property
    def dislikes(self):

        post_dislikes = get_dislikes(self.id)

        # If post likes is not set in the cache 
        if not post_dislikes:
            with SessionLocal() as db:
                post_dislikes = db.query(user_reactions_table).filter_by(is_like = False,post_id = self.id).count()
            set_dislikes(self.id,post_dislikes)

        return post_dislikes 

