import express from "express";
import Podcast from "../models/Podcast.js";
import Segment from "../models/Segment.js";

const router = express.Router();

// GET ALL PODCASTS
router.get("/", async (req, res) => {
  try {
    const podcasts = await Podcast.aggregate([
      {
        $lookup: {
          from: "segments",
          localField: "_id",
          foreignField: "podcastId",
          as: "segments"
        }
      },
      {
        $addFields: {
          segmentCount: { $size: "$segments" }
        }
      },
      {
        $project: {
          segments: 0
        }
      },
      {
        $sort: { createdAt: -1 }
      }
    ]);

    res.json(podcasts);
  } catch (err) {
    res.status(500).json({ error: "Failed to fetch podcasts" });
  }
});

// GET PODCAST BY ID
router.get("/:id", async (req, res) => {
  try {
    const podcast = await Podcast.findById(req.params.id);
    if (!podcast) return res.status(404).json({ error: "Not found" });

    res.json(podcast);
  } catch (err) {
    res.status(500).json({ error: "Failed to fetch podcast" });
  }
});

export default router;
