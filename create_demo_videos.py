import os

# Create simple demo video files (placeholder files)
# These will be replaced by actual recordings when visiondrive.py runs

demo_videos = [
    "rec_20250115_120000.mp4",
    "rec_20250115_130000.mp4",
    "rec_20250115_140000.mp4",
]

os.makedirs("/app/blackbox_data", exist_ok=True)

for video_name in demo_videos:
    video_path = os.path.join("/app/blackbox_data", video_name)
    # Create a minimal valid MP4 file header
    # This is a minimal MP4 that video players will recognize
    with open(video_path, "wb") as f:
        # Basic MP4 structure with ftyp and moov atoms
        f.write(b'\x00\x00\x00\x20\x66\x74\x79\x70\x69\x73\x6f\x6d\x00\x00\x02\x00'
                b'\x69\x73\x6f\x6d\x69\x73\x6f\x32\x6d\x70\x34\x31\x00\x00\x00\x08'
                b'\x66\x72\x65\x65')
        # Pad with some data to make it look like a video file
        f.write(b'\x00' * 1024)

print(f"Created {len(demo_videos)} demo video files in /app/blackbox_data/")
