from sqlalchemy import Column,Integer,String,ForeignKey,DateTime,Boolean,Table
from database.db_setup import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.db_setup import get_db

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
        db = next(get_db())
        return db.query(user_ractions_table).filter_by(is_like=True,post_id=self.id).count()
    
    @property
    def dislikes(self):
        db = next(get_db())
        return db.query(user_ractions_table).filter_by(is_like=False,post_id=self.id).count()
        