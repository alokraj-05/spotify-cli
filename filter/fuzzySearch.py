from fuzzywuzzy import fuzz
import re

def _normalize(text):
	# lower, strip, collapse whitespace
	return re.sub(r'\s+', ' ', (text or '').strip().lower())

def fuzzy_search(tracks, user_input, top_n=5):
	"""
	Accepts:
	 - tracks: list of Spotify track items (either raw track objects or playlist item dicts that contain 'track')
	 - user_input: string from user
	 - top_n: number of top results to return

	Returns: list of dicts: {uri, name, artist, popularity, score, substring, final_score}
	Sorted by: final_score (desc), popularity (desc)
	"""
	if not tracks or not user_input:
		return []

	q_raw = user_input.strip()
	if not q_raw:
		return []

	q = _normalize(q_raw)
	q_tokens = [t for t in re.split(r'\W+', q) if t]

	results = []
	for item in tracks:
		track_obj = item.get('track') if isinstance(item, dict) and 'track' in item else item
		if not isinstance(track_obj, dict):
			continue

		name = track_obj.get('name') or ''
		artists = track_obj.get('artists') or []
		artist = artists[0].get('name') if artists and isinstance(artists[0], dict) else ''
		popularity = int(track_obj.get('popularity', 0) or 0)
		uri = track_obj.get('uri')

		n_name = _normalize(name)
		n_artist = _normalize(artist)
		combined = f"{n_name} {n_artist}".strip()

		# fuzzy scores (0-100)
		score_name = fuzz.token_set_ratio(q, n_name) if n_name else 0
		score_artist = fuzz.token_set_ratio(q, n_artist) if n_artist else 0
		score_both = fuzz.token_set_ratio(q, combined) if combined else 0

		# direct token overlap (fraction of query tokens present in name/artist)
		match_tokens = 0
		for t in q_tokens:
			if t and (t in n_name.split() or t in n_artist.split()):
				match_tokens += 1
		overlap_score = (match_tokens / len(q_tokens)) if q_tokens else 0  # 0..1

		# substring exact match
		substring = (q in n_name) or (q in n_artist)

		# Combined final score weighting (tuneable)
		# Give high weight to combined fuzzy match, medium to name/artist, small to overlap
		final_score = (0.6 * score_both) + (0.3 * max(score_name, score_artist)) + (0.1 * overlap_score * 100)
		# bonus for substring exact match
		if substring:
			final_score += 20

		# clamp and int
		final_score = int(round(max(0, min(100, final_score))))

		results.append({
			"uri": uri,
			"name": name,
			"artist": artist,
			"popularity": popularity,
			"score_name": score_name,
			"score_artist": score_artist,
			"score_both": score_both,
			"overlap": overlap_score,
			"substring": substring,
			"final_score": final_score
		})

	# sort primarily by final_score (desc), then popularity (desc)
	results.sort(key=lambda r: (r['final_score'], r['popularity']), reverse=True)

	return results[:top_n]

