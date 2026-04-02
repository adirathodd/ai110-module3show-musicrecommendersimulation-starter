"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from src.recommender import load_songs, recommend_songs
except ImportError:
    from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Default verification profile for CLI checks.
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.82,
        "valence": 0.84,
        "tempo_bpm": 118,
        "likes_acoustic": False,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations\n")
    print("-" * 72)
    for rank, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        reasons = explanation.split(", ")

        print(f"{rank}. {song['title']}")
        print(f"   Score   : {score:.2f}")
        print("   Reasons :")
        for reason in reasons:
            print(f"     - {reason}")
        print("-" * 72)


if __name__ == "__main__":
    main()
