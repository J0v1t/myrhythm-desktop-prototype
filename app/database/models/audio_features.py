from app.database.schema import Base
from sqlalchemy import Column, Integer, Text, String, Float, ForeignKey
from sqlalchemy.orm import relationship
import json, time

class AudioFeatures(Base):
    __tablename__ = 'audio_features'

    id = Column(Integer, primary_key=True)
    song_id = Column(Integer, ForeignKey('songs.id'), unique=True)
    file_hash = Column(String, nullable=False)
    features_json = Column(Text, nullable=False)
    last_scanned = Column(Float, default=lambda: time.time())

    song = relationship('Song', back_populates='audio_features')

    def set_features(self, features_dict):
        self.features_json = json.dumps(features_dict)


    def get_features(self):
        return json.loads(self.features_json)