# 🎧 Model Card: RhythmMatch 1.0

## Model Name
RhythmMatch 1.0.

## Goal / Task
This model suggests songs from a small catalog.
It tries to match a user's favorite genre, favorite mood, and target energy.

## Data Used
The dataset has 30 songs from one CSV file.
Each song has genre, mood, energy, tempo, valence, danceability, and acousticness.
The catalog covers many genres and moods, but each one has very few songs.
I did not add or remove songs.
A limit is that the data is small and may not represent broad music taste.

## Algorithm Summary
The model gives points for genre match and mood match.
It also gives energy points based on how close the song energy is to the user's target.
Energy has the biggest impact because it can add up to 4 points.
The model sorts songs by total score and returns the top results.
If scores tie, it prefers higher energy match, then song title order.

## Observed Behavior / Biases
The model often favors energy over mood and genre.
In a conflict profile, high-energy songs can win even with weak mood match.
With out-of-range energy input, it still returns songs instead of warning the user.
This can create repetitive recommendations and reduce emotional variety.

## Evaluation Process
I tested five user profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock, Conflict Case, and Out-of-Range Energy.
I compared top-5 songs and checked the score explanations.
Normal profiles looked reasonable.
Conflict and edge-case profiles showed stronger energy bias.

## Intended Use and Non-Intended Use
Intended use: classroom practice for understanding ranking rules and recommender behavior.
Intended use: quick simulation with a small music catalog.
Non-intended use: real music product decisions for diverse users.
Non-intended use: high-stakes or sensitive decisions about people.

## Ideas for Improvement
1. Clamp or validate user inputs like energy so invalid values are handled safely.
2. Rebalance feature weights so mood and genre are not overshadowed by energy.
3. Add a diversity rule so top recommendations are less repetitive.

## Personal Reflection
My biggest learning moment was seeing how small weight changes can shift rankings a lot.
At first, I assumed tiny math changes would not matter much.
After testing conflict and edge-case profiles, I saw that they matter a lot.

AI tools helped me move faster when drafting explanations and planning test profiles.
I still had to double-check score logic, profile inputs, and result interpretation.
I learned that AI suggestions are useful, but they are not automatically correct for my exact code.

I was surprised that this simple algorithm still felt like a recommender.
Even with basic rules, the top songs often looked personally relevant.
That made the system feel smart, even though the logic was straightforward.

If I extended this project, I would add input validation, diversity constraints, and more user preferences.
I would also test on a bigger catalog and compare multiple scoring strategies side by side.
