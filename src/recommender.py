from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass
from collections import Counter
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
    popularity: int = 50
    release_decade: int = 2010
    mood_tags: str = ""
    instrumentalness: float = 0.5
    loudness_db: float = -10.0
    live_performance: float = 0.2

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
    preferred_decade: Optional[int] = None
    preferred_mood_tags: Optional[List[str]] = None
    target_popularity: int = 65
    likes_instrumental: Optional[bool] = None
    target_loudness_db: Optional[float] = None


MODE_WEIGHTS: Dict[str, Dict[str, float]] = {
    "balanced": {
        "genre": 1.8,
        "mood": 1.5,
        "energy": 3.0,
        "popularity": 1.0,
        "decade": 1.3,
        "mood_tags": 1.8,
        "instrumental": 0.8,
        "loudness": 0.6,
    },
    "genre_first": {
        "genre": 3.2,
        "mood": 1.0,
        "energy": 2.0,
        "popularity": 0.6,
        "decade": 1.2,
        "mood_tags": 1.2,
        "instrumental": 0.4,
        "loudness": 0.4,
    },
    "mood_first": {
        "genre": 1.0,
        "mood": 3.0,
        "energy": 2.2,
        "popularity": 0.7,
        "decade": 0.8,
        "mood_tags": 2.8,
        "instrumental": 0.6,
        "loudness": 0.4,
    },
    "energy_focused": {
        "genre": 0.8,
        "mood": 0.8,
        "energy": 4.2,
        "popularity": 0.5,
        "decade": 0.5,
        "mood_tags": 1.1,
        "instrumental": 0.5,
        "loudness": 1.5,
    },
}


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


def _normalize_tags(raw_tags: Any) -> List[str]:
    if not raw_tags:
        return []
    return [tag.strip().lower() for tag in str(raw_tags).split("|") if tag.strip()]


def _get_mode_weights(mode: str) -> Dict[str, float]:
    return MODE_WEIGHTS.get(mode, MODE_WEIGHTS["balanced"])


def _compute_component_scores(user_prefs: Dict, song: Dict, mode: str) -> Dict[str, float]:
    weights = _get_mode_weights(mode)

    genre_match = 1.0 if song["genre"] == user_prefs.get("genre") else 0.0
    mood_match = 1.0 if song["mood"] == user_prefs.get("mood") else 0.0

    energy_similarity = _clamp01(1.0 - abs(song["energy"] - user_prefs.get("energy", 0.5)))

    target_popularity = float(user_prefs.get("target_popularity", 65))
    popularity_similarity = _clamp01(1.0 - abs(float(song.get("popularity", 50)) - target_popularity) / 100.0)

    preferred_decade = user_prefs.get("preferred_decade")
    if preferred_decade is None:
        decade_similarity = 0.5
    else:
        decade_similarity = _clamp01(1.0 - abs(float(song.get("release_decade", 2010)) - float(preferred_decade)) / 40.0)

    user_tags = {tag.lower() for tag in user_prefs.get("preferred_mood_tags", [])}
    song_tags = set(_normalize_tags(song.get("mood_tags", "")))
    if user_tags:
        mood_tag_overlap = len(user_tags & song_tags) / len(user_tags)
    else:
        mood_tag_overlap = 0.0

    likes_instrumental = user_prefs.get("likes_instrumental")
    instrumentalness = _clamp01(float(song.get("instrumentalness", 0.5)))
    if likes_instrumental is None:
        instrumental_alignment = 0.5
    elif likes_instrumental:
        instrumental_alignment = instrumentalness
    else:
        instrumental_alignment = 1.0 - instrumentalness

    target_loudness = user_prefs.get("target_loudness_db")
    if target_loudness is None:
        loudness_alignment = 0.5
    else:
        loudness_alignment = _clamp01(1.0 - abs(float(song.get("loudness_db", -10.0)) - float(target_loudness)) / 30.0)

    return {
        "genre": genre_match * weights["genre"],
        "mood": mood_match * weights["mood"],
        "energy": energy_similarity * weights["energy"],
        "popularity": popularity_similarity * weights["popularity"],
        "decade": decade_similarity * weights["decade"],
        "mood_tags": mood_tag_overlap * weights["mood_tags"],
        "instrumental": instrumental_alignment * weights["instrumental"],
        "loudness": loudness_alignment * weights["loudness"],
    }


def _song_to_dict(song: Song) -> Dict[str, Any]:
    return {
        "id": song.id,
        "title": song.title,
        "artist": song.artist,
        "genre": song.genre,
        "mood": song.mood,
        "energy": song.energy,
        "tempo_bpm": song.tempo_bpm,
        "valence": song.valence,
        "danceability": song.danceability,
        "acousticness": song.acousticness,
        "popularity": song.popularity,
        "release_decade": song.release_decade,
        "mood_tags": song.mood_tags,
        "instrumentalness": song.instrumentalness,
        "loudness_db": song.loudness_db,
        "live_performance": song.live_performance,
    }


def _user_to_dict(user: UserProfile) -> Dict[str, Any]:
    return {
        "genre": user.favorite_genre,
        "mood": user.favorite_mood,
        "energy": user.target_energy,
        "likes_acoustic": user.likes_acoustic,
        "preferred_decade": user.preferred_decade,
        "preferred_mood_tags": user.preferred_mood_tags or [],
        "target_popularity": user.target_popularity,
        "likes_instrumental": user.likes_instrumental,
        "target_loudness_db": user.target_loudness_db,
    }

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    @staticmethod
    def _compute_score(user: UserProfile, song: Song, mode: str = "balanced") -> Tuple[float, Dict[str, float]]:
        user_prefs = _user_to_dict(user)
        song_dict = _song_to_dict(song)
        component_scores = _compute_component_scores(user_prefs, song_dict, mode)
        total = sum(component_scores.values())
        return total, component_scores

    def recommend(self, user: UserProfile, k: int = 5, mode: str = "balanced", diversity_penalty: float = 0.75) -> List[Song]:
        scored = []
        for song in self.songs:
            total, component_scores = self._compute_score(user, song, mode)
            scored.append((song, total, component_scores))

        remaining = scored[:]
        selected: List[Tuple[Song, float]] = []
        artist_counts: Counter = Counter()
        genre_counts: Counter = Counter()

        while remaining and len(selected) < k:
            best_index = 0
            best_adjusted = float("-inf")

            for idx, (song, base_score, _) in enumerate(remaining):
                penalty = (diversity_penalty * artist_counts[song.artist]) + (
                    (diversity_penalty * 0.6) * genre_counts[song.genre]
                )
                adjusted_score = base_score - penalty
                if adjusted_score > best_adjusted:
                    best_adjusted = adjusted_score
                    best_index = idx

            song, base_score, _ = remaining.pop(best_index)
            selected.append((song, base_score))
            artist_counts[song.artist] += 1
            genre_counts[song.genre] += 1

        selected.sort(key=lambda item: (-item[1], item[0].title.lower()))
        return [song for song, _ in selected]

    def explain_recommendation(self, user: UserProfile, song: Song, mode: str = "balanced") -> str:
        total, component_scores = self._compute_score(user, song, mode)
        reasons = [
            f"mode={mode}",
            f"genre (+{component_scores['genre']:.2f})",
            f"mood (+{component_scores['mood']:.2f})",
            f"energy (+{component_scores['energy']:.2f})",
            f"popularity (+{component_scores['popularity']:.2f})",
            f"decade (+{component_scores['decade']:.2f})",
            f"mood tags (+{component_scores['mood_tags']:.2f})",
            f"instrumental fit (+{component_scores['instrumental']:.2f})",
            f"loudness fit (+{component_scores['loudness']:.2f})",
        ]
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
                    "popularity": int(row.get("popularity", 50)),
                    "release_decade": int(row.get("release_decade", 2010)),
                    "mood_tags": row.get("mood_tags", ""),
                    "instrumentalness": float(row.get("instrumentalness", 0.5)),
                    "loudness_db": float(row.get("loudness_db", -10.0)),
                    "live_performance": float(row.get("live_performance", 0.2)),
                }
            )
    return songs


def score_song(user_prefs: Dict, song: Dict, mode: str = "balanced") -> Tuple[float, List[str]]:
    """Return a song's total score and human-readable scoring reasons."""
    component_scores = _compute_component_scores(user_prefs, song, mode)
    total = sum(component_scores.values())

    reasons = [
        f"mode={mode}",
        f"genre (+{component_scores['genre']:.2f})",
        f"mood (+{component_scores['mood']:.2f})",
        f"energy (+{component_scores['energy']:.2f})",
        f"popularity (+{component_scores['popularity']:.2f})",
        f"decade (+{component_scores['decade']:.2f})",
        f"mood tags (+{component_scores['mood_tags']:.2f})",
        f"instrumental fit (+{component_scores['instrumental']:.2f})",
        f"loudness fit (+{component_scores['loudness']:.2f})",
    ]
    return total, reasons

def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    mode: str = "balanced",
    diversity_penalty: float = 0.75,
) -> List[Tuple[Dict, float, str]]:
    """Score, diversity-rerank, and return the top-k song recommendations."""
    scored: List[Tuple[Dict, float, List[str]]] = []
    for song in songs:
        total, reasons = score_song(user_prefs, song, mode=mode)
        scored.append((song, total, reasons))

    remaining = sorted(
        scored,
        key=lambda item: (-item[1], -item[0].get("energy", 0.0), item[0]["title"].lower()),
    )

    top_k: List[Tuple[Dict, float, str]] = []
    artist_counts: Counter = Counter()
    genre_counts: Counter = Counter()

    while remaining and len(top_k) < k:
        best_index = 0
        best_adjusted = float("-inf")

        for idx, (song, base_score, reasons) in enumerate(remaining):
            artist_penalty = diversity_penalty * artist_counts[song["artist"]]
            genre_penalty = (diversity_penalty * 0.6) * genre_counts[song["genre"]]
            adjusted = base_score - artist_penalty - genre_penalty
            if adjusted > best_adjusted:
                best_adjusted = adjusted
                best_index = idx

        song, base_score, reasons = remaining.pop(best_index)
        artist_penalty = diversity_penalty * artist_counts[song["artist"]]
        genre_penalty = (diversity_penalty * 0.6) * genre_counts[song["genre"]]

        reasons_with_diversity = reasons + [
            f"artist diversity penalty (-{artist_penalty:.2f})",
            f"genre diversity penalty (-{genre_penalty:.2f})",
            f"final adjusted score ({base_score - artist_penalty - genre_penalty:.2f})",
        ]
        top_k.append((song, base_score, ", ".join(reasons_with_diversity)))

        artist_counts[song["artist"]] += 1
        genre_counts[song["genre"]] += 1

    return top_k
