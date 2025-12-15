import express from "express";
import dotenv from "dotenv";
import cors from "cors";
import connectDB from "./config/db.js";

import podcastRoutes from "./routes/podcastRoutes.js";
import segmentRoutes from "./routes/segmentRoutes.js";

dotenv.config();

// Connect to MongoDB
connectDB();

const app = express();

app.use(cors());
app.use(express.json());

// Routes
app.use("/api/podcasts", podcastRoutes);
app.use("/api", segmentRoutes);

app.get("/", (req, res) => {
  res.send("Podcast Analyzer API is running...");
});

// Start server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
});
