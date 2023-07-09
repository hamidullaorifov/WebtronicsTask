from sqlalchemy import Column,Integer,String,ForeignKey,DateTime,Boolean,Table
from database.db_setup import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.db_setup import get_db
from app.utils.cache import set_likes,set_dislikes,get_likes,get_dislikes

import main
user_ractions_table = Table(
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

    reacting_users = relationship('User',secondary=user_ractions_table,back_populates='reacted_posts')


    @property
    def likes(self):
        likes_count = get_likes(self.id)
        if not likes_count:
            db = next(get_db())
            likes_count = db.query(user_ractions_table).filter_by(is_like=True,post_id=self.id).count()
            set_likes(self.id,likes_count)

        return likes_count 
    
    @property
    def dislikes(self):
        dislikes_count = get_dislikes(self.id)
        if not dislikes_count:
            db = next(get_db())
            dislikes_count = db.query(user_ractions_table).filter_by(is_like=False,post_id=self.id).count()
            set_dislikes(self.id,dislikes_count)

        return dislikes_count 

