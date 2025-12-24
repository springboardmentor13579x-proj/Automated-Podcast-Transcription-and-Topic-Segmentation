import { useNavigate } from "react-router-dom";
import { Sparkles, Zap, FileText } from "lucide-react";
import FileUpload from "../components/FileUpload";
import { uploadAudio } from "../services/api";
import logger from "../utils/logger"; // ADDED

const features = [
  {
    icon: Sparkles,
    title: "AI-Powered Transcription",
    description: "State-of-the-art speech recognition for accurate transcripts",
  },
  {
    icon: Zap,
    title: "Smart Segmentation",
    description: "Automatic topic detection and content organization",
  },
  {
    icon: FileText,
    title: "Structured Podcast Intelligence",
    description: "Convert long-form audio into searchable, structured knowledge",
  },

];

const UploadPage = () => {
  const navigate = useNavigate();

  const handleUpload = async (file) => {
    try {
      //  Call backend API
      const response = await uploadAudio(file);

      //  LOG UPLOAD RESULT (ADDED)
      logger.info("Upload API success", {
        podcastId: response?.podcastId,
        fileName: file.name,
      });

      // Navigate only after successful upload
      navigate("/processing", {
        state: { fileName: file.name },
      });
    } catch (error) {
      console.error("Upload failed:", error);
      alert("Audio upload failed. Please try again.");
    }
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] flex flex-col items-center justify-center px-4 py-16">
      {/* Hero Section */}
      <div className="text-center mb-12 animate-fade-in">
        <h1 className="text-4xl sm:text-5xl font-bold text-foreground mb-4">
          Transform Your Podcasts with{" "}
          <span className="gradient-text">AI Analysis</span>
        </h1>
        <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
          Upload your audio files and get intelligent transcriptions, topic
          segmentation, and comprehensive summaries in minutes.
        </p>
      </div>

      {/* Upload Component */}
      <div className="w-full max-w-2xl mb-16 animate-slide-up">
        <FileUpload onUpload={handleUpload} />
      </div>

      {/* Features */}
      <div
        className="grid grid-cols-1 sm:grid-cols-3 gap-6 w-full max-w-4xl animate-fade-in"
        style={{ animationDelay: "200ms" }}
      >
        {features.map((feature, index) => {
          const Icon = feature.icon;
          return (
            <div
              key={index}
              className="text-center p-6 rounded-xl bg-card border border-border"
            >
              <div className="inline-flex p-3 rounded-xl bg-primary/10 mb-4">
                <Icon className="h-6 w-6 text-primary" />
              </div>
              <h3 className="font-semibold text-foreground mb-2">
                {feature.title}
              </h3>
              <p className="text-sm text-muted-foreground">
                {feature.description}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default UploadPage;
