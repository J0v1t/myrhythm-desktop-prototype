from app.database.schema import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

class UserPreferences(Base):
    __tablename__ = 'preferences'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    favorite_genres = Column(String(255), nullable=True)
    favorite_artists = Column(String(255), nullable=True)
    
    user = relationship('User', backref='preferences')
   