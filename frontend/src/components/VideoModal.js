import React from "react";

const BACKEND_URL =
  process.env.REACT_APP_BACKEND_URL || "http://127.0.0.1:8000";

const VideoModal = ({ video, onClose }) => {
  if (!video) return null;

  const videoSrc = `${BACKEND_URL}${video.path}`;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 modal-overlay"
      onClick={onClose}
      data-testid="video-modal"
    >
      <div
        className="glass-card max-w-4xl w-full p-6"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <h3
            className="text-white text-xl font-semibold"
            data-testid="modal-title"
          >
            {video.filename}
          </h3>

          <button
            onClick={onClose}
            className="text-white hover:text-gray-300 transition-colors"
            data-testid="close-modal-button"
          >
            ✕
          </button>
        </div>

        {/* Video Player */}
        <div className="aspect-video bg-black rounded-lg overflow-hidden">
          <video
            src={videoSrc}
            controls
            autoPlay
            className="w-full h-full"
            data-testid="video-player"
          />
        </div>

        {/* Info */}
        <div className="mt-4 text-white/70 text-sm">
          <p>Recorded: {new Date(video.modified).toLocaleString()}</p>
          <p>Size: {(video.size / 1024).toFixed(2)} KB</p>
        </div>
      </div>
    </div>
  );
};

export default VideoModal;