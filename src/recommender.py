from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    @staticmethod
    def _compute_score(user: UserProfile, song: Song) -> Tuple[float, float, float, float]:
        genre_points = 2.0 if song.genre == user.favorite_genre else 0.0
        mood_points = 1.0 if song.mood == user.favorite_mood else 0.0

        diff = abs(song.energy - user.target_energy)
        energy_points = max(0.0, 2.0 - (2.0 * diff))

        total = genre_points + mood_points + energy_points
        return total, genre_points, mood_points, energy_points

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored = []
        for song in self.songs:
            total, _, _, energy_points = self._compute_score(user, song)
            scored.append((song, total, energy_points))

        scored.sort(key=lambda item: (-item[1], -item[2], item[0].title.lower()))
        return [song for song, _, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        total, genre_points, mood_points, energy_points = self._compute_score(user, song)
        reasons = []

        if genre_points > 0:
            reasons.append("genre match (+2.0)")
        else:
            reasons.append("no genre match (+0.0)")

        if mood_points > 0:
            reasons.append("mood match (+1.0)")
        else:
            reasons.append("no mood match (+0.0)")

        reasons.append(f"energy closeness (+{energy_points:.2f})")
        return f"{song.title} scored {total:.2f}: " + ", ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into typed dictionaries."""
    songs: List[Dict] = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append(
                {
                    "id": int(row["id"]),
                    "title": row["title"],
                    "artist": row["artist"],
                    "genre": row["genre"],
                    "mood": row["mood"],
                    "energy": float(row["energy"]),
                    "tempo_bpm": float(row["tempo_bpm"]),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                }
            )
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Return a song's total score and human-readable scoring reasons."""
    reasons: List[str] = []

    genre_points = 2.0 if song["genre"] == user_prefs["genre"] else 0.0
    if genre_points > 0:
        reasons.append("genre match (+2.0)")
    else:
        reasons.append("no genre match (+0.0)")

    mood_points = 1.0 if song["mood"] == user_prefs["mood"] else 0.0
    if mood_points > 0:
        reasons.append("mood match (+1.0)")
    else:
        reasons.append("no mood match (+0.0)")

    diff = abs(song["energy"] - user_prefs["energy"])
    energy_points = max(0.0, 2.0 - (2.0 * diff))
    reasons.append(f"energy closeness (+{energy_points:.2f})")

    total = genre_points + mood_points + energy_points
    return total, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score, rank, and return the top-k song recommendations."""
    scored: List[Tuple[Dict, float, List[str]]] = [
        (song, *score_song(user_prefs, song)) for song in songs
    ]

    ranked = sorted(scored, key=lambda item: item[1], reverse=True)
    top_k = ranked[:k]

    return [
        (song, total, ", ".join(reasons))
        for song, total, reasons in top_k
    ]
