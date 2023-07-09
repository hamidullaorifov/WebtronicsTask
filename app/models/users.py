from database.db_setup import Base
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import relationship
from .posts import Post,user_reactions_table
                       

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,index=True,nullable=False,unique=True)
    email = Column(String,unique=True,nullable=False)
    first_name = Column(String,nullable=True)
    last_name = Column(String,nullable=True)
    password = Column(String(100),nullable=False)

    posts = relationship('Post',backref='owner')
    reacted_posts = relationship('Post',secondary=user_reactions_table,back_populates='reacting_users')
    