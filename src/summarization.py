def summarize_segment(seg_text, top_k=5):
    sentences = sent_tokenize(seg_text)
    lead = sentences[0] if sentences else seg_text[:150]
    kws = extract_keywords(seg_text, top_k=top_k)
    return {
        "summary": lead,
        "keywords": ", ".join(kws)
    }

rows = []
for _, row in docs_df.iterrows():
    fname = row["file"]
    for seg_id, seg in enumerate(row["segments"]):
        info = summarize_segment(seg, top_k=5)
        rows.append({
            "file": fname,
            "segment_id": seg_id,
            "text": seg,
            "summary": info["summary"],
            "keywords": info["keywords"],
        })

week3_df = pd.DataFrame(rows)
print("\nWeek 3 results – first 10 rows:")
print(week3_df.head(10))
