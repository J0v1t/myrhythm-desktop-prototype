from app.database.schema import Base, engine
from app.database.models import User, UserPreferences, Song, AudioFeatures

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database initialized.")
