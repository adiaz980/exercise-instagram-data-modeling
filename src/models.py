import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    full_name = Column(String(100), nullable=False)

    posts = relationship('Post', back_populates='user')
    comments = relationship('Comment', back_populates='user')
    likes = relationship('Like', back_populates='user')

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, nullable=False)
    caption = Column(String(500))
    image_url = Column(String(200), nullable=False)
    creation_time = Column(DateTime, default=func.now(), nullable=False)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', back_populates='posts')

    comments = relationship('Comment', back_populates='post')
    likes = relationship('Like', back_populates='post')

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True, nullable=False)
    text = Column(String(500), nullable=False)
    creation_time = Column(DateTime, default=func.now(), nullable=False)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', back_populates='comments')

    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    post = relationship('Post', back_populates='comments')

class Like(Base):
    __tablename__ = 'like'
    id = Column(Integer, primary_key=True, nullable=False)
    creation_time = Column(DateTime, default=func.now(), nullable=False)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', back_populates='likes')

    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    post = relationship('Post', back_populates='likes')

# Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e