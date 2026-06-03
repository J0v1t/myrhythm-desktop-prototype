import json
from app.database.schema import db
from app.database.models.preference import UserPreferences


def _preference_query(user_id):
    query = getattr(UserPreferences, "query", None)
    if query is not None:
        return query.filter_by(user_id=user_id)
    return db.query(UserPreferences).filter_by(user_id=user_id)


def _write_session():
    return getattr(db, "session", db)


# ---- Save Preferences ----
def save_user_preferences(user_id, genres, artists, mood_map=None):
    prefs = _preference_query(user_id).first()
    if not prefs:
        prefs = UserPreferences(user_id=user_id)

    prefs.favorite_genres = ','.join(genres)
    prefs.favorite_artists = ','.join(artists)
    prefs.mood_mapping = json.dumps(mood_map or {})

    session = _write_session()
    session.add(prefs)
    session.commit()
    return prefs


# ---- Load Preferences ----
def load_user_preferences(user_id):
    prefs = _preference_query(user_id).first()
    if not prefs:
        return {"genres": [], "artists": [], "mood_map": {}}
    return {
        "genres": prefs.favorite_genres.split(',') if prefs.favorite_genres else [],
        "artists": prefs.favorite_artists.split(',') if prefs.favorite_artists else [],
        "mood_map": json.loads(prefs.mood_mapping or "{}")
    }


# ---- Delete or Reset Preferences ----
def reset_user_preferences(user_id):
    prefs = _preference_query(user_id).first()
    if prefs:
        session = _write_session()
        session.delete(prefs)
        session.commit()
        return True
    return False
