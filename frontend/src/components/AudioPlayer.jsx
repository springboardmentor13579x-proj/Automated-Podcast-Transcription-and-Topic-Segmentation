import { useEffect, useRef, useState } from 'react';
import {
  Play,
  Pause,
  SkipBack,
  SkipForward,
  Volume2,
  VolumeX
} from 'lucide-react';
import logger from '../utils/logger';

const AudioPlayer = ({ title, audioUrl }) => {
  const audioRef = useRef(null);

  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [volume, setVolume] = useState(75);
  const [isMuted, setIsMuted] = useState(false);

  const resolvedAudioUrl = audioUrl
    ? `http://localhost:5000${audioUrl}`
    : '';

  /* ===============================
     AUDIO EVENTS
     =============================== */
  useEffect(() => {
    const audio = audioRef.current;
    if (!audio || !resolvedAudioUrl) return;

    logger.info("AudioPlayer resolved audioUrl", {
      resolvedAudioUrl
    });

    audio.src = resolvedAudioUrl;
    audio.load();

    const onLoaded = () => {
      logger.info("Audio metadata loaded", {
        duration: audio.duration
      });
      setDuration(audio.duration || 0);
    };

    const onTimeUpdate = () => {
      setCurrentTime(audio.currentTime);
    };

    const onError = () => {
      logger.error("Audio failed to load", {
        resolvedAudioUrl
      });
    };

    audio.addEventListener('loadedmetadata', onLoaded);
    audio.addEventListener('timeupdate', onTimeUpdate);
    audio.addEventListener('error', onError);

    return () => {
      audio.removeEventListener('loadedmetadata', onLoaded);
      audio.removeEventListener('timeupdate', onTimeUpdate);
      audio.removeEventListener('error', onError);
    };
  }, [resolvedAudioUrl]);

  /* ===============================
     PLAY / PAUSE
     =============================== */
  const togglePlay = () => {
    const audio = audioRef.current;
    if (!audio) return;

    if (isPlaying) {
      audio.pause();
      setIsPlaying(false);
    } else {
      audio.play()
        .then(() => setIsPlaying(true))
        .catch(() => {
          logger.error("Audio play failed", { resolvedAudioUrl });
        });
    }
  };

  /* ===============================
     SEEK
     =============================== */
  const handleProgressClick = (e) => {
    const audio = audioRef.current;
    if (!audio || duration === 0) return;

    const rect = e.currentTarget.getBoundingClientRect();
    const clickPosition = (e.clientX - rect.left) / rect.width;
    audio.currentTime = clickPosition * duration;
  };

  /* ===============================
     VOLUME
     =============================== */
  useEffect(() => {
    if (!audioRef.current) return;
    audioRef.current.volume = isMuted ? 0 : volume / 100;
  }, [volume, isMuted]);

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const progress =
    duration > 0 ? (currentTime / duration) * 100 : 0;

  return (
    <div className="card-elevated p-6">
      <audio ref={audioRef} preload="metadata" />

      <div className="flex items-center gap-4 mb-4">
        <div className="p-3 rounded-xl bg-primary/10">
          <Volume2 className="h-6 w-6 text-primary" />
        </div>
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold truncate">{title}</h3>
          <p className="text-sm text-muted-foreground">Audio Player</p>
        </div>
      </div>

      <div
        className="h-2 bg-muted rounded-full cursor-pointer mb-4"
        onClick={handleProgressClick}
      >
        <div
          className="h-full bg-primary rounded-full"
          style={{ width: `${progress}%` }}
        />
      </div>

      <div className="flex justify-between text-sm text-muted-foreground mb-6">
        <span>{formatTime(currentTime)}</span>
        <span>{formatTime(duration)}</span>
      </div>

      <div className="flex items-center justify-center gap-4">
        <button onClick={() => (audioRef.current.currentTime -= 10)}>
          <SkipBack />
        </button>

        <button
          className="p-4 rounded-full bg-primary text-white"
          onClick={togglePlay}
        >
          {isPlaying ? <Pause /> : <Play />}
        </button>

        <button onClick={() => (audioRef.current.currentTime += 10)}>
          <SkipForward />
        </button>
      </div>

      <div className="flex items-center gap-3 mt-6">
        <button onClick={() => setIsMuted(!isMuted)}>
          {isMuted ? <VolumeX /> : <Volume2 />}
        </button>

        <input
          type="range"
          min="0"
          max="100"
          value={isMuted ? 0 : volume}
          onChange={(e) => {
            setVolume(Number(e.target.value));
            setIsMuted(false);
          }}
          className="flex-1"
        />
      </div>
    </div>
  );
};

export default AudioPlayer;
