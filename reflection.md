# Reflection Comparisons

These notes compare each pair of tested user profiles using the latest run after the weight-shift experiment.

1. High-Energy Pop vs Chill Lofi: High-Energy Pop surfaces fast, high-energy songs like Gym Hero and Storm Runner, while Chill Lofi shifts to calmer tracks like Library Rain and Midnight Coding. This makes sense because their target energies are far apart.
2. High-Energy Pop vs Deep Intense Rock: Both profiles share high-energy songs, so Gym Hero appears in both lists, but Deep Intense Rock favors harder tracks like Wildflower Riot and Iron Anthem. The overlap comes from similar energy targets.
3. High-Energy Pop vs Conflict Case (High Energy + Melancholic): Both lists contain high-energy songs, but the conflict profile loses happy-pop context and becomes mostly pure energy matches. This shows the model is prioritizing energy over mood nuance.
4. High-Energy Pop vs Out-of-Range Energy (1.20): Out-of-range energy pushes recommendations toward the highest-energy songs overall, while High-Energy Pop still keeps some happy context through Sunrise City. The difference shows invalid inputs can distort intent.
5. Chill Lofi vs Deep Intense Rock: Chill Lofi returns low-energy, softer songs, while Deep Intense Rock returns aggressive, high-energy songs. This is an expected direction change based on opposite energy targets.
6. Chill Lofi vs Conflict Case (High Energy + Melancholic): Chill Lofi produces lofi/chill songs, but the conflict profile jumps to high-energy tracks with almost no mood agreement. That shift explains why users with mixed preferences may feel misunderstood.
7. Chill Lofi vs Out-of-Range Energy (1.20): Chill Lofi recommendations are calm and close to 0.35 energy, while out-of-range inputs force extreme-energy songs. This comparison highlights that the model needs input validation.
8. Deep Intense Rock vs Conflict Case (High Energy + Melancholic): These outputs overlap heavily because both ask for high energy, even though one asks for intense and the other asks for melancholic. Mood differences are getting flattened by the energy weight.
9. Deep Intense Rock vs Out-of-Range Energy (1.20): Both lists contain very energetic songs, but Out-of-Range Energy removes even the little genre/mood guidance and becomes a near "highest energy" ranking. This suggests the model can overfit to one numeric feature.
10. Conflict Case (High Energy + Melancholic) vs Out-of-Range Energy (1.20): Both lists are dominated by high-energy tracks, and neither consistently returns melancholic songs. In plain language, this is why Gym Hero keeps showing up: it is very energetic, so the model repeatedly treats it as a safe top match.
