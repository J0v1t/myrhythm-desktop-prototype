from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os

Base = declarative_base()

db_file_path = os.path.join(
  os.path.dirname(__file__),
  '..',
  '..',
  'instance',
  'myrhythm.db'
)

db_directory = os.path.dirname(db_file_path)

if not os.path.exists(db_directory):
  os.makedirs(db_directory, exist_ok=True)
  print(f"Created database directory: {db_directory}")

# Database configuration. Keep SQLite as the local default, but allow a
# DATABASE_URL override for future Postgres/Supabase-compatible adapters.
DATABASE_URI = os.environ.get("DATABASE_URL", f'sqlite:///{db_file_path}')

engine = create_engine(DATABASE_URI, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = scoped_session(SessionLocal)
