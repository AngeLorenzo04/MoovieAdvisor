from enum import Enum
import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class MoodType(str, Enum):
    DECOMPRESSION = "DECOMPRESSION"
    CATHARSIS = "CATHARSIS"
    HYPNOTIC = "HYPNOTIC"
    INTROSPECTION = "INTROSPECTION"

class InteractionStatus(str, Enum):
    SKIPPED = "SKIPPED"
    SEEN = "SEEN"
    CHOSEN = "CHOSEN"

class FeedbackRating(str, Enum):
    REVELATORY = "REVELATORY"
    FORMATIVE = "FORMATIVE"
    NOT_FOR_ME = "NOT_FOR_ME"

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    current_tier = Column(Integer, default=1)
    include_lower_tiers = Column(Boolean, default=True)
    
    interactions = relationship("UserInteraction", back_populates="user")

class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    tmdb_id = Column(Integer, unique=True, nullable=True)
    title = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    runtime = Column(Integer, nullable=False)  # in minutes
    director = Column(String(255), nullable=False)
    poster_url = Column(String(1024), nullable=True)
    
    mood_tag = Column(SQLEnum(MoodType))
    movement_tag = Column(String(255))
    tier = Column(Integer, default=1)
    
    tech_innovation = Column(Text, nullable=True)
    cultural_legacy = Column(Text, nullable=True)
    watch_tip = Column(Text, nullable=True)
    
    interactions = relationship("UserInteraction", back_populates="movie")

class UserInteraction(Base):
    __tablename__ = 'user_interactions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    movie_id = Column(Integer, ForeignKey('movies.id'))
    
    status = Column(SQLEnum(InteractionStatus))
    rating = Column(SQLEnum(FeedbackRating), nullable=True)
    interaction_timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    user = relationship("User", back_populates="interactions")
    movie = relationship("Movie", back_populates="interactions")
