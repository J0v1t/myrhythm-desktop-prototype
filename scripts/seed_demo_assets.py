from pathlib import Path
import math
import struct
import sys
import wave

from PIL import Image, ImageDraw, ImageFont

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.database.db_init import init_db
from app.database.models import Song, User, UserPreferences
from app.database.schema import SessionLocal


DEMO_ROOT = PROJECT_ROOT / "instance" / "demo_assets"
TRACKS_DIR = DEMO_ROOT / "tracks"
COVERS_DIR = DEMO_ROOT / "covers"

DEMO_USER_EMAIL = "demo@myrhythm.local"
DEMO_USER_PASSWORD = "demo123"

BASE_DEMO_TRACKS = [
    ("Bright Pulse", "MyRhythm Demo", "pop", "happy", 261.63, (247, 198, 89), (43, 120, 210)),
    ("Soft Signal", "MyRhythm Demo", "acoustic", "neutral", 196.00, (104, 170, 150), (29, 50, 76)),
    ("Rain Window", "MyRhythm Demo", "folk", "sad", 174.61, (83, 111, 173), (28, 32, 54)),
    ("High Voltage", "MyRhythm Demo", "rock", "angry", 329.63, (223, 87, 65), (44, 25, 25)),
    ("Orbit Drift", "MyRhythm Demo", "electronic", "happy", 392.00, (115, 91, 214), (30, 28, 60)),
    ("Late Metro", "MyRhythm Demo", "hip-hop", "neutral", 220.00, (208, 136, 79), (35, 35, 35)),
]
DEMO_TRACKS = []
for batch in range(4):
    for title, artist, genre, mood, frequency, start_color, end_color in BASE_DEMO_TRACKS:
        suffix = "" if batch == 0 else f" {batch + 1}"
        DEMO_TRACKS.append(
            (
                f"{title}{suffix}",
                artist,
                genre,
                mood,
                frequency * (1 + batch * 0.035),
                start_color,
                end_color,
            )
        )


def _slug(value: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "-" for ch in value).strip("-")


def _write_wave(path: Path, frequency: float, duration_seconds: float = 18.0) -> None:
    sample_rate = 44100
    amplitude = 12000
    frame_count = int(sample_rate * duration_seconds)
    frames = bytearray()
    for i in range(frame_count):
        t = i / sample_rate
        carrier = math.sin(2 * math.pi * frequency * t)
        harmony = 0.35 * math.sin(2 * math.pi * (frequency * 1.5) * t)
        pulse = 0.75 + 0.25 * math.sin(2 * math.pi * 1.2 * t)
        value = int(amplitude * pulse * (carrier + harmony) / 1.35)
        frames.extend(struct.pack("<h", value))

    with wave.open(str(path), "w") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(frames)


def _write_cover(path: Path, title: str, mood: str, start_color, end_color) -> None:
    size = 768
    image = Image.new("RGB", (size, size), start_color)
    draw = ImageDraw.Draw(image)
    for y in range(size):
        blend = y / max(size - 1, 1)
        color = tuple(int(start_color[i] * (1 - blend) + end_color[i] * blend) for i in range(3))
        draw.line([(0, y), (size, y)], fill=color)

    draw.ellipse((96, 96, 672, 672), outline=(255, 255, 255), width=8)
    draw.arc((150, 150, 618, 618), 205, 335, fill=(255, 255, 255), width=14)
    draw.text((64, 86), "MYRHYTHM", fill=(255, 255, 255), font=_font(44))
    draw.text((64, 570), title.upper(), fill=(255, 255, 255), font=_font(54))
    draw.text((64, 636), mood.capitalize(), fill=(240, 240, 240), font=_font(34))
    image.save(path)


def _font(size: int):
    for candidate in ("arial.ttf", "segoeui.ttf"):
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def seed_demo_assets() -> None:
    init_db()
    TRACKS_DIR.mkdir(parents=True, exist_ok=True)
    COVERS_DIR.mkdir(parents=True, exist_ok=True)

    db = SessionLocal()
    try:
        user = db.query(User).filter_by(email=DEMO_USER_EMAIL).first()
        if user is None:
            user = User(name="Demo Reviewer", email=DEMO_USER_EMAIL)
            user.set_password(DEMO_USER_PASSWORD)
            db.add(user)
            db.flush()

        prefs = db.query(UserPreferences).filter_by(user_id=user.id).first()
        if prefs is None:
            db.add(
                UserPreferences(
                    user_id=user.id,
                    favorite_genres="pop,electronic,rock,acoustic",
                    favorite_artists="MyRhythm Demo",
                )
            )

        for title, artist, genre, mood, frequency, start_color, end_color in DEMO_TRACKS:
            slug = _slug(title)
            track_path = TRACKS_DIR / f"{slug}.wav"
            cover_path = COVERS_DIR / f"{slug}.png"
            if not track_path.exists():
                _write_wave(track_path, frequency)
            if not cover_path.exists():
                _write_cover(cover_path, title, mood, start_color, end_color)

            song = db.query(Song).filter_by(file_path=str(track_path)).first()
            if song is None:
                song = Song(file_path=str(track_path))
                db.add(song)
            song.title = title
            song.artist = artist
            song.genre = genre
            song.duration = 18.0
            song.cover_path = str(cover_path)

        db.commit()
    finally:
        db.close()

    print("Seeded MyRhythm demo database.")
    print(f"Login: {DEMO_USER_EMAIL}")
    print(f"Password: {DEMO_USER_PASSWORD}")
    print(f"Tracks: {TRACKS_DIR}")
    print(f"Covers: {COVERS_DIR}")


if __name__ == "__main__":
    seed_demo_assets()
