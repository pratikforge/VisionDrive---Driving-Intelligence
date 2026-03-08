"""
VisionDrive Project Report — PDF Generator
Generates a professional PDF report from the project analysis.
"""

from fpdf import FPDF
import os

class VisionDriveReport(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(120, 120, 120)
            self.cell(0, 8, "VisionDrive - Project Report", align="L")
            self.cell(0, 8, f"Page {self.page_no()}", align="R")
            self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, "VisionDrive AR Navigation System - Confidential", align="C")

    def section_title(self, title, icon=""):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(30, 30, 30)
        self.ln(4)
        self.cell(0, 10, f"{icon}  {title}" if icon else title, new_x="LMARGIN", new_y="NEXT")
        # Accent line
        self.set_draw_color(255, 120, 30)
        self.set_line_width(0.8)
        self.line(self.l_margin, self.get_y(), self.l_margin + 60, self.get_y())
        self.ln(6)

    def sub_title(self, title):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(50, 50, 50)
        self.ln(2)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

    def sub_sub_title(self, title):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(70, 70, 70)
        self.ln(1)
        self.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def bold_text(self, text):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def bullet(self, text, indent=10):
        x = self.get_x()
        self.set_font("Helvetica", "", 10)
        self.set_text_color(50, 50, 50)
        self.cell(indent)
        self.set_font("Helvetica", "B", 10)
        self.cell(5, 5.5, "-")
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 5.5, f"  {text}")
        self.ln(1)

    def code_block(self, text):
        self.set_font("Courier", "", 9)
        self.set_fill_color(240, 240, 240)
        self.set_text_color(40, 40, 40)
        self.ln(1)
        for line in text.split("\n"):
            self.cell(5)
            self.cell(0, 5, f"  {line}", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

    def table(self, headers, rows, col_widths=None):
        if col_widths is None:
            avail = self.w - self.l_margin - self.r_margin
            col_widths = [avail / len(headers)] * len(headers)

        # Header
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(45, 45, 55)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 8, f"  {h}", border=1, fill=True)
        self.ln()

        # Rows
        self.set_font("Helvetica", "", 9)
        self.set_text_color(50, 50, 50)
        fill = False
        for row in rows:
            if self.get_y() > 265:
                self.add_page()
            if fill:
                self.set_fill_color(248, 248, 248)
            else:
                self.set_fill_color(255, 255, 255)
            max_h = 8
            for i, cell_text in enumerate(row):
                self.cell(col_widths[i], max_h, f"  {cell_text}", border=1, fill=True)
            self.ln()
            fill = not fill
        self.ln(3)

    def highlight_box(self, text, color=(255, 245, 230)):
        self.set_fill_color(*color)
        self.set_draw_color(255, 120, 30)
        self.set_font("Helvetica", "I", 10)
        self.set_text_color(80, 50, 10)
        y = self.get_y()
        self.rect(self.l_margin, y, self.w - self.l_margin - self.r_margin, 12, style="DF")
        self.cell(5)
        self.cell(0, 12, text)
        self.ln(16)


def generate_report():
    pdf = VisionDriveReport()

    # ===================== COVER PAGE =====================
    pdf.add_page()
    pdf.ln(50)
    pdf.set_font("Helvetica", "B", 36)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 15, "VisionDrive", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 18)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, "AI-Powered AR Driving Assistant", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)

    # Accent bar
    pdf.set_fill_color(255, 120, 30)
    bar_w = 80
    pdf.rect((pdf.w - bar_w) / 2, pdf.get_y(), bar_w, 3, style="F")
    pdf.ln(15)

    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 8, "Complete Project Report", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, "February 2026", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(30)
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(130, 130, 130)
    pdf.multi_cell(0, 6,
        "VisionDrive is an AI-powered Augmented Reality driving assistant that uses\n"
        "a single camera + YOLOv8 object detection to provide real-time navigation,\n"
        "risk assessment, and a black-box recording system.", align="C")

    # ===================== TABLE OF CONTENTS =====================
    pdf.add_page()
    pdf.section_title("Table of Contents")
    toc = [
        "1.  Project Overview",
        "2.  Architecture Overview",
        "3.  Project Structure",
        "4.  Core Engine (visiondrive.py)",
        "    4.1  Processing Pipeline",
        "    4.2  BlackBoxSystem",
        "    4.3  Risk Scoring Engine",
        "    4.4  Airbag Deployment State Machine",
        "    4.5  Keyboard Controls",
        "5.  Backend (server.py)",
        "    5.1  API Endpoints",
        "6.  Frontend (React Dashboard)",
        "    6.1  Pages",
        "    6.2  Components",
        "7.  Data Flow",
        "8.  Technology Stack",
        "9.  Key Design Decisions",
    ]
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(50, 50, 50)
    for item in toc:
        pdf.cell(10)
        pdf.cell(0, 7, item, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    # ===================== 1. PROJECT OVERVIEW =====================
    pdf.add_page()
    pdf.section_title("1. Project Overview")
    pdf.body_text(
        "VisionDrive is a cutting-edge single-camera AR ADAS (Advanced Driver Assistance System) "
        "that combines risk fusion, Heads-Up Display (HUD), and a rolling black-box recorder into "
        "one intelligent navigation solution."
    )
    pdf.body_text(
        "Using advanced computer vision and real-time object detection, VisionDrive enhances the "
        "driving experience by projecting navigation cues and safety alerts directly onto the "
        "driver's field of view through augmented reality."
    )
    pdf.body_text(
        "The integrated black-box system continuously records the journey, ensuring a reliable "
        "record of critical moments while on the road. In the event of a crash, the system "
        "automatically locks all recordings to preserve evidence."
    )

    # ===================== 2. ARCHITECTURE =====================
    pdf.section_title("2. Architecture Overview")
    pdf.body_text("The system consists of three main layers:")
    pdf.ln(2)

    pdf.bold_text("Layer 1: React Frontend (Port 3000)")
    pdf.bullet("Serves as the user dashboard and control panel")
    pdf.bullet("Allows launching the CV engine and viewing black-box recordings")

    pdf.bold_text("Layer 2: FastAPI Backend (Port 8000)")
    pdf.bullet("REST API that bridges frontend and engine")
    pdf.bullet("Manages MongoDB data, launches engine subprocess, serves video files")

    pdf.bold_text("Layer 3: VisionDrive CV Engine")
    pdf.bullet("Standalone Python process with OpenCV windows")
    pdf.bullet("Runs YOLOv8 detection, calculates risk, renders AR HUD, records black-box data")

    pdf.ln(2)
    pdf.highlight_box("The CV engine runs locally via OpenCV — it is NOT streamed through the browser.")

    # ===================== 3. PROJECT STRUCTURE =====================
    pdf.section_title("3. Project Structure")
    pdf.table(
        ["Path", "Purpose"],
        [
            ["visiondrive.py", "Core CV engine - the heart of the project"],
            ["backend/server.py", "FastAPI server (API + engine launcher)"],
            ["backend/.env", "MongoDB URL + DB name"],
            ["backend/requirements.txt", "Python dependencies (FastAPI, Motor, YOLO, etc.)"],
            ["frontend/src/", "React app with Tailwind CSS + Radix UI"],
            ["blackbox_data/", "Recorded video chunks (.mp4 files)"],
            ["yolov8n.pt", "Pre-trained YOLOv8 nano model weights (~6.5 MB)"],
            ["create_demo_videos.py", "Script to create placeholder demo videos"],
            ["test_result.md", "Testing protocol and results tracking"],
        ],
        col_widths=[60, 110]
    )

    # ===================== 4. CORE ENGINE =====================
    pdf.add_page()
    pdf.section_title("4. Core Engine - visiondrive.py")
    pdf.body_text(
        "This is the most important file in the project. It runs a real-time computer vision "
        "pipeline using OpenCV and YOLOv8, processing video frames to provide augmented reality "
        "navigation and safety alerts."
    )

    # 4.1
    pdf.sub_title("4.1  Processing Pipeline")
    pdf.body_text("Each frame goes through the following steps:")
    steps = [
        "Opens a video feed (video.mp4 or webcam via OpenCV)",
        "Runs YOLOv8 object detection on every frame, detecting cars, trucks, buses, motorbikes, bicycles, and pedestrians",
        "Calculates a risk score (0-100) based on detected object size multiplied by priority weight",
        "Renders an AR HUD overlay on the video with lane overlay, navigation arrows, status bars",
        "Records the processed frame to the black-box system",
        "Checks for potential accident conditions and triggers safety protocols if needed",
    ]
    for i, step in enumerate(steps, 1):
        pdf.bullet(f"Step {i}: {step}")

    # 4.2
    pdf.sub_title("4.2  BlackBoxSystem - Flight Recorder for Cars")
    pdf.body_text(
        "The BlackBoxSystem class implements a rolling video recorder inspired by aircraft "
        "flight data recorders. It continuously records the driving session in manageable chunks."
    )
    pdf.bold_text("Key Behaviors:")
    pdf.bullet("Records video in 10-second rolling chunks (configurable via CHUNK_DURATION)")
    pdf.bullet("Keeps only the last 5 chunks, auto-deletes oldest (50 seconds of footage)")
    pdf.bullet("On crash detection: locks ALL recordings, prevents overwrite, preserves evidence")
    pdf.bullet("Writes a flight_data.csv log with timestamps, speed, and risk levels")
    pdf.bullet("Uses OpenCV VideoWriter with mp4v codec")

    pdf.ln(2)
    pdf.bold_text("BlackBoxSystem Methods:")
    pdf.table(
        ["Method", "Description"],
        [
            ["__init__(folder, max_files)", "Creates folder, cleans old files, initializes CSV log"],
            ["start_new_chunk(frame_size, fps)", "Releases old writer, creates new MP4 file, manages queue"],
            ["update(frame, speed, risk)", "Writes frame to current chunk, auto-rotates when time expires"],
            ["emergency_lock()", "Locks system permanently - no more recording or deletion"],
            ["release()", "Cleanly releases the video writer on shutdown"],
        ],
        col_widths=[60, 110]
    )

    # 4.3
    pdf.sub_title("4.3  Risk Scoring Engine")
    pdf.body_text(
        "The risk scoring system uses a weighted area-based approach. Each detected object's "
        "bounding box area is multiplied by a priority weight based on the object type. "
        "The largest weighted area determines the raw risk score."
    )
    pdf.bold_text("Object Priority Weights:")
    pdf.table(
        ["Object Type", "Weight", "Rationale"],
        [
            ["Motorbike / Bicycle", "4.0x (highest)", "Most vulnerable road users"],
            ["Person (pedestrian)", "3.0x", "High vulnerability on road"],
            ["Car", "2.5x", "Common collision partner"],
            ["Truck / Bus", "2.0x", "Large but predictable"],
        ],
        col_widths=[50, 45, 75]
    )

    pdf.bold_text("Risk Calculation Formula:")
    pdf.code_block(
        "weighted_area = bounding_box_area * priority_weight\n"
        "raw_risk = min(100, (max_weighted_area / 150,000) * 100)\n"
        "smoothed_risk = 0.2 * raw_risk + 0.8 * previous_smoothed_risk"
    )
    pdf.body_text(
        "The exponential smoothing (alpha=0.2) prevents the risk meter from flickering rapidly, "
        "providing a stable reading. Objects below the hood line (bottom 20% of frame) are "
        "filtered out to avoid false positives from the vehicle's own hood."
    )

    # 4.4
    pdf.add_page()
    pdf.sub_title("4.4  Airbag Deployment State Machine")
    pdf.body_text("The system uses a two-state machine to handle airbag deployment scenarios:")
    pdf.ln(2)
    pdf.table(
        ["State", "Condition", "Behavior"],
        [
            ["NORMAL", "Default", "Normal AR HUD display, risk monitoring active"],
            ["LOCKED", "B key pressed", "Airbag deployed, system frozen, black box locked permanently"],
        ],
        col_widths=[35, 50, 85]
    )

    pdf.bold_text("State Transitions:")
    pdf.bullet("NORMAL -> LOCKED: User presses B key to simulate airbag deployment")
    pdf.bullet("LOCKED -> LOCKED: Permanent state, black box data is frozen and preserved")
    pdf.bullet("No clips are deleted; no new clips are generated after deployment")

    # 4.5
    pdf.sub_title("4.5  Keyboard Controls")
    pdf.table(
        ["Key", "Action"],
        [
            ["Q", "Quit the application"],
            ["B", "Simulate airbag deployment (immediately freezes system and black box)"],
            ["W", "Set navigation direction to STRAIGHT"],
            ["A", "Set navigation direction to LEFT turn"],
            ["D", "Set navigation direction to RIGHT turn"],
        ],
        col_widths=[30, 140]
    )

    # ===================== 5. BACKEND =====================
    pdf.add_page()
    pdf.section_title("5. Backend - server.py")
    pdf.body_text(
        "The backend is a FastAPI server that acts as a bridge between the React frontend "
        "and the VisionDrive CV engine. It provides REST API endpoints for engine control, "
        "video retrieval, and basic status tracking via MongoDB."
    )
    pdf.bold_text("Key Technologies:")
    pdf.bullet("FastAPI + Uvicorn (async Python web server)")
    pdf.bullet("Motor (async MongoDB driver for non-blocking database operations)")
    pdf.bullet("Pydantic v2 (data validation and serialization)")
    pdf.bullet("CORS middleware enabled for frontend communication")

    # 5.1
    pdf.sub_title("5.1  API Endpoints")
    pdf.table(
        ["Method", "Endpoint", "Purpose"],
        [
            ["GET", "/api/", "Health check - returns 'Hello World'"],
            ["POST", "/api/status", "Create a status check entry (stored in MongoDB)"],
            ["GET", "/api/status", "List all status check entries"],
            ["POST", "/api/launch-engine", "Launch visiondrive.py as a subprocess"],
            ["GET", "/api/blackbox-videos", "List all black box recordings with metadata"],
            ["GET", "/api/blackbox-videos/{filename}", "Stream/download a specific recording"],
        ],
        col_widths=[20, 60, 90]
    )

    pdf.bold_text("Engine Launch Mechanism:")
    pdf.body_text(
        "The /api/launch-engine endpoint uses Python's subprocess.Popen to start visiondrive.py "
        "as a detached process (start_new_session=True). This means the CV engine runs "
        "independently of the web server and opens its own OpenCV windows on the local machine."
    )

    # ===================== 6. FRONTEND =====================
    pdf.section_title("6. Frontend - React Dashboard")
    pdf.body_text(
        "The frontend is a 3-page single-page application built with Create React App, "
        "customized with CRACO. It uses Tailwind CSS for styling, Radix UI for accessible "
        "component primitives, and Axios for HTTP requests."
    )

    # 6.1
    pdf.sub_title("6.1  Pages")
    pdf.table(
        ["Page", "Route", "Description"],
        [
            ["Home", "/", "Hero section with 'Open App' button that launches the CV engine"],
            ["Features", "/features", "Grid of black box videos; click to play in modal"],
            ["About", "/about", "Description of VisionDrive and key features list"],
        ],
        col_widths=[30, 30, 110]
    )

    # 6.2
    pdf.sub_title("6.2  Key Components")
    pdf.table(
        ["Component", "File", "Purpose"],
        [
            ["Navbar", "Navbar.js", "Fixed top nav with logo, links, and Start button"],
            ["VideoModal", "VideoModal.js", "Full-screen modal for playing black box videos"],
            ["UI Primitives", "ui/ (46 files)", "Radix-based accessible components (buttons, dialogs, etc.)"],
        ],
        col_widths=[40, 45, 85]
    )

    # ===================== 7. DATA FLOW =====================
    pdf.add_page()
    pdf.section_title("7. End-to-End Data Flow")
    pdf.bold_text("Flow 1: Launching the Engine")
    pdf.bullet("User clicks 'Open App' or 'Start' on the frontend")
    pdf.bullet("Frontend sends POST request to /api/launch-engine")
    pdf.bullet("Backend spawns visiondrive.py as a detached subprocess")
    pdf.bullet("CV engine opens OpenCV windows showing AR HUD and mini-map")
    pdf.bullet("Engine begins recording chunks to blackbox_data/ folder")

    pdf.ln(3)
    pdf.bold_text("Flow 2: Viewing Black Box Recordings")
    pdf.bullet("User navigates to Features page")
    pdf.bullet("Frontend sends GET request to /api/blackbox-videos")
    pdf.bullet("Backend reads blackbox_data/ directory, returns file list with metadata")
    pdf.bullet("Frontend displays video grid with thumbnails")
    pdf.bullet("User clicks a video -> VideoModal opens -> streams MP4 from backend")

    pdf.ln(3)
    pdf.bold_text("Flow 3: Airbag Deployment")
    pdf.bullet("User presses B key to simulate airbag deployment")
    pdf.bullet("System immediately transitions to LOCKED state")
    pdf.bullet("'AIRBAG DEPLOYED / SYSTEM FROZEN' banner appears on screen")
    pdf.bullet("BlackBoxSystem.emergency_lock() is called -> all recordings preserved")
    pdf.bullet("No new clips are generated; existing clips remain intact")

    # ===================== 8. TECH STACK =====================
    pdf.section_title("8. Technology Stack")
    pdf.table(
        ["Layer", "Technologies"],
        [
            ["CV Engine", "Python, OpenCV, YOLOv8 (Ultralytics), NumPy"],
            ["Backend", "FastAPI, Uvicorn, Motor (MongoDB async), Pydantic v2"],
            ["Frontend", "React 19, Tailwind CSS 3, Radix UI, Axios, Recharts"],
            ["Database", "MongoDB (via Motor async driver)"],
            ["Build Tools", "CRACO, PostCSS, Yarn, ESLint"],
            ["ML Model", "YOLOv8 Nano (yolov8n.pt, ~6.5 MB)"],
        ],
        col_widths=[40, 130]
    )

    # ===================== 9. DESIGN DECISIONS =====================
    pdf.section_title("9. Key Design Decisions")

    decisions = [
        ("Single-Camera Approach",
         "No LiDAR or multi-camera rig needed. Uses a single video feed with YOLOv8 for "
         "cost-effective deployment. Makes the system accessible for any vehicle."),
        ("Rolling Black Box",
         "Only the last 50 seconds of footage is kept (5 x 10-second chunks) to manage "
         "storage. Oldest chunks are auto-deleted unless an emergency lock is triggered."),
        ("Weighted Risk Fusion",
         "Risk is weighted by object type, not just proximity. A pedestrian triggers a "
         "higher alert than a truck at the same apparent distance, reflecting real-world danger."),
        ("Local CV Execution",
         "The CV engine runs locally via OpenCV windows rather than streaming through the "
         "browser. This ensures low-latency processing critical for driver safety."),
        ("Exponential Smoothing",
         "Risk readings use alpha=0.2 smoothing to prevent the HUD risk meter from "
         "flickering rapidly, providing a stable, readable output for the driver."),
        ("Detached Subprocess",
         "The backend launches the engine as a detached process (start_new_session=True), "
         "so the engine keeps running even if the web server restarts."),
    ]

    for title, desc in decisions:
        pdf.bold_text(title)
        pdf.body_text(desc)

    # ===================== OUTPUT =====================
    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "VisionDrive_Project_Report.pdf"
    )
    pdf.output(output_path)
    print(f"\nPDF report generated successfully!")
    print(f"Location: {output_path}")
    return output_path


if __name__ == "__main__":
    generate_report()
