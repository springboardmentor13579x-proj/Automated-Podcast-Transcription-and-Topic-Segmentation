import mongoose from "mongoose";

const podcastSchema = new mongoose.Schema(
  {
    title: { type: String, required: true },
    fileName: { type: String, required: true },
    audioUrl: { type: String },
    description: { type: String },
    duration: { type: Number },
    tags: [String]
  },
  { timestamps: true }
);

const Podcast = mongoose.model("Podcast", podcastSchema);

export default Podcast;
