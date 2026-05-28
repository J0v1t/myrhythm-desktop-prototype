import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from app.music.recommendation.recommendation_engine import RecommendationEngine

engine = RecommendationEngine()
results = engine.recommend(
    user_id=1,
    fer_emotion="happy",
    hr_emotion=None,
    nlp_text=None,
    combined_mode=False,
    candidate_limit=200,
    top_k=10
)

for r in results:
    print(r["score"], r["title"], "-", r["artist"], "|", r["genre"], "|", r["breakdown"])
    