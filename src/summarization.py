import os
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# -----------------------------
# LOAD ENV VARIABLES
# -----------------------------
load_dotenv()

# -----------------------------
# PATHS FROM .env
# -----------------------------
EVAL_FILE = os.getenv("EVALUATION_OUTPUT_FILE")
GRAPH_FOLDER = os.getenv("GRAPHS_DIR")

def summarize_results():

    # Create folder if not exists
    os.makedirs(GRAPH_FOLDER, exist_ok=True)

    df = pd.read_excel(EVAL_FILE)

    # Calculate averages
    avg_accuracy = df["Final Accuracy Score (%)"].mean()
    avg_wer = df["WER (%)"].mean()
    avg_cer = df["CER (%)"].mean()
    avg_similarity = df["Semantic Similarity"].mean()

    total_files = len(df)

    print("\n--------------- TRANSCRIPTION PERFORMANCE SUMMARY ---------------")
    print(f"Total evaluated files: {total_files}")
    print(f"Average WER: {avg_wer:.2f}%")
    print(f"Average CER: {avg_cer:.2f}%")
    print(f"Average Semantic Similarity Score: {avg_similarity:.3f}")
    print(f"\n>>> FINAL OVERALL TRANSCRIPTION ACCURACY: {avg_accuracy:.2f}% <<<")
    print("------------------------------------------------------------------")

    # Summary data
    metrics = {
        "Metric": ["Accuracy", "WER", "CER", "Similarity"],
        "Values": [avg_accuracy, avg_wer, avg_cer, avg_similarity * 100]
    }
    summary_df = pd.DataFrame(metrics)

    # -------- Graph 1: Bar Chart --------
    plt.figure(figsize=(8, 5))
    plt.bar(summary_df["Metric"], summary_df["Values"])
    plt.title("Average Evaluation Metrics")
    plt.ylabel("Percentage")
    plt.savefig(os.path.join(GRAPH_FOLDER, "Summary_Metrics.png"))
    plt.close()

    # -------- Graph 2: Histogram --------
    plt.figure(figsize=(10, 5))
    plt.hist(df["Final Accuracy Score (%)"], bins=20)
    plt.title("Accuracy Score Distribution Across Files")
    plt.xlabel("Accuracy (%)")
    plt.ylabel("File Count")
    plt.savefig(os.path.join(GRAPH_FOLDER, "Accuracy_Distribution.png"))
    plt.close()

    # -------- Graph 3: Pie Chart --------
    good = len(df[df["Final Accuracy Score (%)"] >= 90])
    moderate = len(df[(df["Final Accuracy Score (%)"] < 90) & (df["Final Accuracy Score (%)"] >= 70)])
    low = len(df[df["Final Accuracy Score (%)"] < 70])

    plt.figure(figsize=(6, 6))
    plt.pie(
        [good, moderate, low],
        labels=["High Quality", "Moderate", "Low"],
        autopct="%1.1f%%",
        startangle=140
    )
    plt.title("Transcript Quality Classification")
    plt.savefig(os.path.join(GRAPH_FOLDER, "Quality_Classification.png"))
    plt.close()

    print("\nGraphs saved in:", GRAPH_FOLDER)
    print(" - Summary_Metrics.png")
    print(" - Accuracy_Distribution.png")
    print(" - Quality_Classification.png")

    return {
        "Total Files": total_files,
        "Avg WER (%)": avg_wer,
        "Avg CER (%)": avg_cer,
        "Avg Semantic Similarity": avg_similarity,
        "Final Accuracy (%)": avg_accuracy
    }

if __name__ == "__main__":
    summarize_results()
