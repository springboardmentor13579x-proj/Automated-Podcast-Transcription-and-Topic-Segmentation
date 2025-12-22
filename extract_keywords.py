import os
from sklearn.feature_extraction.text import TfidfVectorizer

# Paths
INPUT_DIR = "../segmented/"
OUTPUT_DIR = "../keywords/"

# Create output folder automatically
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Read all segmented text
documents = []
file_names = []

for file in os.listdir(INPUT_DIR):
    if file.endswith("_segments.txt"):
        with open(os.path.join(INPUT_DIR, file), "r", encoding="utf-8") as f:
            documents.append(f.read())
            file_names.append(file)

# TF-IDF keyword extractor
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=10   # Top 10 keywords per file
)

tfidf_matrix = vectorizer.fit_transform(documents)
feature_names = vectorizer.get_feature_names_out()

# Save keywords for each file
for idx, file in enumerate(file_names):
    scores = tfidf_matrix[idx].toarray()[0]
    keywords = sorted(
        zip(feature_names, scores),
        key=lambda x: x[1],
        reverse=True
    )

    output_file = file.replace("_segments.txt", "_keywords.txt")
    with open(os.path.join(OUTPUT_DIR, output_file), "w", encoding="utf-8") as f:
        for word, score in keywords:
            f.write(f"{word}\n")

    print(f"Keywords extracted: {output_file}")

print("\nAll keyword files saved in /keywords folder")