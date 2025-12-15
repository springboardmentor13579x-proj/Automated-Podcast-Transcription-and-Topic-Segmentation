import fs from "fs";
import path from "path";
import dotenv from "dotenv";
import mongoose from "mongoose";
import Podcast from "../models/Podcast.js";
import Segment from "../models/Segment.js";

dotenv.config();

const __dirname = path.resolve();
const dataDir = path.join(__dirname, "..", "database");

const importData = async () => {
  try {
    await mongoose.connect(process.env.MONGO_URI);

    const files = fs.readdirSync(dataDir).filter(f => f.endsWith("_segments.json"));

    for (const file of files) {
      const filePath = path.join(dataDir, file);
      const json = JSON.parse(fs.readFileSync(filePath));

      const title = file.replace("_segments.json", "");

      const podcast = await Podcast.create({
        title,
        fileName: file,
        audioUrl: `/audio/${title}.mp3`
      });

        console.log("Importing:", file);
        for (const seg of json) {
        // Fix missing timestamps
        const start = seg.start_time ?? 0;
        const end = seg.end_time ?? (start + 5); // fallback: +5 seconds length

        if (!seg.end_time) {
         console.log(`⚠️  Missing end_time in segment ${seg.segment_id} of ${title}. Using fallback.`);
        }

        await Segment.create({
            podcastId: podcast._id,
            segmentId: seg.segment_id,
            text: seg.text || "",
            summary: seg.summary || "",
            keywords: seg.keywords || [],
            startTime: start,
            endTime: end
        });

        }

      console.log(`Imported ${json.length} segments for ${title}`);
    }

    console.log("Import complete");
    process.exit();
  } catch (err) {
    console.error(err);
    process.exit(1);
  }
};

importData();
