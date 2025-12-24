import express from "express";
import dotenv from "dotenv";
import cors from "cors";
import path from "path";
import { fileURLToPath } from "url";

import connectDB from "./config/db.js";
import podcastRoutes from "./routes/podcastRoutes.js";
import segmentRoutes from "./routes/segmentRoutes.js";
import uploadRoutes from "./routes/uploadRoutes.js";
import logger from "./utils/logger.js"; // ✅ ADDED (Winston logger)

dotenv.config();

// Resolve __dirname for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Connect to MongoDB
connectDB();

const app = express();

/* ===============================
   MIDDLEWARE
   =============================== */
app.use(cors({
  origin: "http://localhost:8080"
}));
app.use(express.json());

/* ===============================
   STATIC FILE SERVING
   =============================== */
// This exposes backend/uploads to the browser
app.use(
  "/uploads",
  express.static(path.join(__dirname, "uploads"))
);

/* ===============================
   FRONTEND LOGGING API (NEW)
   =============================== */
app.post("/api/logs", (req, res) => {
  const { level, message, data } = req.body;

  if (level === "error") {
    logger.error(`[FRONTEND] ${message} ${JSON.stringify(data)}`);
  } else {
    logger.info(`[FRONTEND] ${message} ${JSON.stringify(data)}`);
  }

  res.status(200).json({ status: "logged" });
});

/* ===============================
   API ROUTES
   =============================== */
app.use("/api/podcasts", podcastRoutes);
app.use("/api", segmentRoutes);
app.use("/api", uploadRoutes);

/* ===============================
   HEALTH CHECK
   =============================== */
app.get("/", (req, res) => {
  res.send("Podcast Analyzer API is running...");
});

/* ===============================
   START SERVER
   =============================== */
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
