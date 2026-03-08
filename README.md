# 🚗 VisionDrive - Driving Intelligence

![VisionDrive Banner](https://img.shields.io/badge/Status-Active-brightgreen.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-purple)

**VisionDrive** is an advanced AI-powered Augmented Reality (AR) driving assistant and active collision warning system. Designed to make driving safer and more intelligent, it leverages real-time computer vision to detect road hazards, predict collision risks, and provide an immersive heads-up display (HUD).

## ✨ Key Features

- **AR Heads-Up Display (HUD)**: Real-time overlay of lane detection, object tagging, and navigation instructions on the video feed.
- **AI Hazard Detection**: Utilizes YOLOv8 for rapid object detection (cars, pedestrians, motorcycles) and prioritizes them based on collision risk.
- **Intelligent Black Box**: Continuously records the last few minutes of driving footage. In the event of an accident, it locks the footage for review and evidence.
- **Emergency Automatic SOS**: Automatically freeze the black box data and trigger an emergency call (`112`) when extreme risk or an airbag deployment is simulated.
- **Live Maps Integration**: Displays a live minimap based on simulated GPS coordinates using OpenStreetMap.
- **Full-Stack Dashboard**: Includes a comprehensive frontend and backend system to view history, generate PDF accident reports, and monitor fleet data.

## 🛠️ Technology Stack

- **Computer Vision & AI**: OpenCV, Ultralytics YOLOv8
- **Core Logic**: Python, NumPy
- **Maps**: StaticMap (OpenStreetMap), Requests
- **Backend API**: FastAPI / Node.js
- **Frontend Dashboard**: React.js / Node.js

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3.8+ and Node.js installed on your machine.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/pratikforge/VisionDrive---Driving-Intelligence.git
   cd VisionDrive---Driving-Intelligence
   ```

2. **Install Python Dependencies:**
   ```bash
   pip install opencv-python numpy ultralytics staticmap requests
   ```

3. **Install Full-Stack Dependencies:**
   ```bash
   # For Backend
   cd backend
   npm install # or pip install -r requirements.txt if using python backend
   
   # For Frontend
   cd ../frontend
   npm install
   ```

### Running the System

1. **Start the Vision Engine:**
   ```bash
   python visiondrive.py
   ```
2. **Start the Dashboard:**
   ```bash
   # Terminal 1 (Backend)
   cd backend
   uvicorn server:app --reload
   
   # Terminal 2 (Frontend)
   cd frontend
   npm start
   ```

### ⌨️ Controls (Simulation Mode)

- `Q` - Quit the application.
- `B` - Simulate Airbag Deployment (Triggers SOS, locks black box recording).
- `W` - Navigate Straight.
- `A` - Navigate Left.
- `D` - Navigate Right.

## 📂 Project Structure

- `visiondrive.py` - Core AI vision loop, HUD drawing, map integration, and AR overlays.
- `dashcam_live.py` - Secondary live feed viewer and processing.
- `backend/` - Server-side logic and API routes for handling black box telemetry and emergency events.
- `frontend/` - React-based user interface for the driving dashboard and post-drive reports.
- `generate_report_pdf.py` - Generates post-accident analysis documents.

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve the AI models, HUD rendering, or web dashboard features.
