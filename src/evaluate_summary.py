import re

def search_segments(query, max_results=10):
    """
    Return rows where query appears in summary, text, or keywords (case-insensitive).
    """
    q = query.strip().lower()
    if not q:
        return week3_df.head(max_results)

    mask_summary = week3_df["summary"].str.lower().str.contains(q, na=False)
    mask_text    = week3_df["text"].str.lower().str.contains(q, na=False)
    mask_kw      = week3_df["keywords"].str.lower().str.contains(q, na=False)

    hits = week3_df[mask_summary | mask_text | mask_kw].copy()
    return hits.head(max_results)

q1 = "chest pain"
print(f"\nSearch results for: '{q1}'")
print(search_segments(q1)[["file", "segment_id", "start_time_s", "summary", "keywords"]])