# 🎙️ Automated Podcast Transcription & Analysis System

An end-to-end pipeline that converts podcast audio → clean transcript → topic-based segments → summaries → keyword extraction → timestamp-aligned insights.

---

## 🚀 Features Completed

### **1️⃣ Audio Transcription (Whisper ASR)**

* Batch transcription for multiple audio files.
* Whisper (`openai-whisper`) used for speech-to-text.
* Output stored as structured JSON:

```json
{
  "audio_file": "...",
  "language": "en",
  "segments": [
    { "start": 0.0, "end": 5.2, "text": "..." }
  ]
}
```

---

### **2️⃣ Transcript Cleaning**

* Removes filler tokens, unwanted characters, broken spacing.
* Cleaned transcripts stored as:

```
Bad Habit_cleaned.json
Confident_cleaned.json
...
```

---

### **3️⃣ Topic Segmentation**

Implemented two algorithms:

#### 🔹 **TextTiling (NLTK)**

* Paragraph-like segmentation based on lexical cohesion.

#### 🔹 **BERT Semantic Segmentation**

* Uses SentenceTransformers (MiniLM-L6-v2).
* Splits based on semantic similarity drop.
* Produces more accurate topic shifts.

Outputs stored as:

```
Bad Habit_cleaned_segments.json
Confident_cleaned_segments.json
...
```

Each file includes:

```json
{
  "texttiling_segments": [...],
  "bert_segments": [...]
}
```

---

### **4️⃣ Keyword Extraction (YAKE)**

* Extracts top keywords for each segment.
* Helps in indexing and search.

---

### **5️⃣ Summarization (T5-small)**

* Summarizes each segment using HuggingFace T5 model.
* Generates concise 20–80 token summaries.

---

### **6️⃣ Timestamp Alignment**

* Segment text aligned with Whisper timestamps.
* Start & end times included for navigation (UI ready).

---

### **7️⃣ Final Output (Per File)**

Each audio file generates a structured summary file:

```
Bad Habit_segments.json
Confident_segments.json
...
```

Example segment:

```json
{
  "segment_id": 1,
  "text": "...",
  "summary": "...",
  "keywords": ["...", "..."],
  "start_time": 12.40,
  "end_time": 34.52
}
```

---

### **8️⃣ WER Evaluation**

* Evaluates accuracy against human-written transcripts.
* Uses `jiwer` library.
  Example:

```
WER for Bad Habit: 0.094
```

---

## 🌐 Backend 

### **Tech Stack**

* Node.js
* Express.js
* MongoDB (Local)
* Mongoose ODM

---

### **Backend Features**

* REST API for podcasts & segments
* MongoDB persistence for:

  * Podcasts
  * Segments (timestamps, keywords, summaries)
* Search & keyword filtering support

---

### **API Endpoints**

#### 📌 Podcasts

```
GET /api/podcasts
```

Returns all uploaded podcasts

---

#### 📌 Segments by Podcast

```
GET /api/podcasts/:podcastId/segments
```

Optional query params:

```
?keyword=trauma
?search=brain
```

---

### **MongoDB Schema Overview**

#### Podcast

* title
* fileName
* audioUrl
* createdAt

#### Segment

* podcastId (ObjectId)
* segmentId
* text
* summary
* keywords
* startTime
* endTime

---

## 📂 Project Structure

```bash
automated-podcast-transcription/
│
├── backend/
│   ├── config/
│   │   └── db.js
│   ├── models/
│   │   ├── Podcast.js
│   │   └── Segment.js
│   ├── routes/
│   │   ├── podcastRoutes.js
│   │   └── segmentRoutes.js
│   ├── scripts/
│   │   └── importSegments.js
│   ├── server.js
│   └── package.json
│
├── data/
│   ├── transcripts/
│   └── segments/
│
├── src/  # Python pipeline
│   ├── transcription/
│   └── segmentation/
│
├── database/
│   ├── Bad Habit_segments.json
│   ├── Confident_segments.json
│   
├── requirements.txt
└── README.md
```
---

## 🛠️ Installation

### 1️⃣ Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Install FFmpeg

Ensure FFmpeg is installed and added to PATH.

---

## ▶️ Running the Pipeline

### **Transcription**

```bash
python -m src.transcription.batch_transcriber
```

### **Segmentation**

```bash
python -m src.segmentation.batch_segmenter
```

### **Keywords + Summaries + Timestamps**

```bash
python -m src.segmentation.batch_keyword_summarizer
```

### **WER Evaluation**

```bash
python -m src.transcription.batch_wer_evaluator
```

### **MongoDB Setup (Local)**

* Install MongoDB Community Edition
* Ensure MongoDB service is running

Check:

```bash
mongod
```

---

### **Backend Setup**

```bash
cd backend
npm install
```

Create `.env` file:

```env
PORT=5000
MONGO_URI=mongodb://127.0.0.1:27017/podcast-analyzer
```

---

### **Import Processed Segments into MongoDB**

```bash
node scripts/importSegments.js
```

---

### **Start Backend Server**

```bash
npm run dev
```

Server runs at:

```
http://localhost:5000
```

---

## 🔍 Testing API

* `http://localhost:5000/api/podcasts`
* `http://localhost:5000/api/podcasts/<PODCAST_ID>/segments`
* `http://localhost:5000/api/podcasts/<PODCAST_ID>/segments?keyword=trauma`

---

## ⚙️ Setup Instructions 

### **1️⃣ Clone Repository**

```bash
git clone <repo-url>
cd automated-podcast-transcription
```

---

### **2️⃣ Python Pipeline Setup**

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Ensure **FFmpeg** is installed and added to PATH.

---

### **3️⃣ Run Python Processing**

```bash
python -m src.transcription.batch_transcriber
python -m src.segmentation.batch_segmenter
python -m src.segmentation.batch_keyword_summarizer
```

---

### **4️⃣ MongoDB Setup (Local)**

* Install MongoDB Community Edition
* Ensure MongoDB service is running

Check:

```bash
mongod
```

---

### **5️⃣ Backend Setup**

```bash
cd backend
npm install
```

Create `.env` file:

```env
PORT=5000
MONGO_URI=mongodb://127.0.0.1:27017/podcast-analyzer
```

---

### **6️⃣ Import Processed Segments into MongoDB**

```bash
node scripts/importSegments.js
```

---

### **7️⃣ Start Backend Server**

```bash
npm run dev
```

Server runs at:

```
http://localhost:5000
```

---

## 🎯 Next Steps (Week 4 – UI & Indexing)

* MERN-based transcript viewer.
* Search and keyword filtering.
* Segment jumping using timestamps.
* Interactive transcript navigation UI.

---

## 👨‍💻 Tech Stack Used

### **Python Backend**

* Whisper ASR
* NLTK
* Sentence Transformers
* YAKE
* HuggingFace Transformers
* JiWER

### Backend

* Node.js
* Express.js
* MongoDB
* Mongoose

### Frontend (Upcoming)

* React
* Tailwind CSS

---

## 📌 Notes

* MongoDB is intentionally **local-only** for development
* No database files are pushed to Git (best practice)
* `.env` is required but not committed

## 🤝 Acknowledgements

* OpenAI Whisper – Speech-to-Text (ASR)
* HuggingFace Transformers – T5 summarization
* Sentence-Transformers – Semantic segmentation (MiniLM)
* NLTK – TextTiling based segmentation
* YAKE – Keyword extraction
* JiWER – Word Error Rate (WER) evaluation
* Node.js – Backend runtime environment
* Express.js – REST API framework
* MongoDB – NoSQL database
* Mongoose – MongoDB object data modeling (ODM)


