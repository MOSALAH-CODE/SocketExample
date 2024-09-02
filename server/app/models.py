from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Level(Base):
    __tablename__ = 'levels'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    order = Column(Integer)
    groups = relationship("Group", back_populates="level")

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    level_id = Column(Integer, ForeignKey('levels.id'))
    level = relationship("Level", back_populates="groups")
    players = relationship("Player", back_populates="group")

class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    score = Column(Integer, default=0)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=True)
    group = relationship("Group", back_populates="players")
