from app.database.schema import Base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

class Song(Base):
    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, unique=True, nullable=False)
    cover_path = Column(String, nullable=True)
    title = Column(String, nullable=True)
    artist = Column(String, nullable=True)
    genre = Column(String, nullable=True)
    duration = Column(Float, nullable=True)

    audio_features = relationship('AudioFeatures', uselist=False, back_populates='song')
