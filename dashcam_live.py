"""
VisionDrive Live Dashcam — MJPEG Streaming Server
==================================================
Captures the laptop webcam, runs YOLOv8 detection + professional HUD,
and streams frames as MJPEG over HTTP on port 8001.

Endpoints:
  GET /feed     → multipart/x-mixed-replace MJPEG stream
  GET /status   → JSON {active, fps, resolution}
  GET /stop     → Gracefully shuts down the server

Usage:
  python dashcam_live.py
"""

import cv2
import numpy as np
from ultralytics import YOLO
import time
import math
import datetime
import threading
from flask import Flask, Response, jsonify
import signal
import sys

# ================== CONFIGURATION ==================
WEBCAM_INDEX = 0
DISPLAY_W, DISPLAY_H = 960, 540       # Slightly smaller for web streaming
JPEG_QUALITY = 75                       # JPEG compression (0-100)

# ─── Color Palette (BGR) ───
C_BG_DARK     = (15, 15, 20)
C_ACCENT_CYAN = (230, 216, 0)
C_NEON_GREEN  = (100, 255, 120)
C_NEON_YELLOW = (50, 230, 255)
C_NEON_RED    = (60, 60, 255)
C_NEON_ORANGE = (50, 140, 255)
C_WHITE       = (255, 255, 255)
C_WHITE_DIM   = (180, 180, 190)
C_BLACK       = (0, 0, 0)
C_GRID_DIM    = (40, 40, 55)
C_BORDER      = (70, 70, 90)
C_PURPLE      = (200, 50, 160)

PRIORITY = {
    "motorbike": 4.0, "bicycle": 4.0, "person": 3.0,
    "car": 2.5, "truck": 2.0, "bus": 2.0
}

# ================== GLOBAL STATE ==================
current_fps = 0.0
is_active = False
shutdown_flag = False

# ================== DRAWING UTILITIES ==================

def draw_transparent_rect(frame, x, y, w, h, color, alpha=0.5):
    overlay = frame.copy()
    cv2.rectangle(overlay, (x, y), (x + w, y + h), color, -1)
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)


def draw_rounded_rect(frame, x, y, w, h, color, alpha=0.5, radius=12):
    overlay = frame.copy()
    r = min(radius, w // 2, h // 2)
    cv2.rectangle(overlay, (x + r, y), (x + w - r, y + h), color, -1)
    cv2.rectangle(overlay, (x, y + r), (x + w, y + h - r), color, -1)
    cv2.circle(overlay, (x + r, y + r), r, color, -1)
    cv2.circle(overlay, (x + w - r, y + r), r, color, -1)
    cv2.circle(overlay, (x + r, y + h - r), r, color, -1)
    cv2.circle(overlay, (x + w - r, y + h - r), r, color, -1)
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)


def draw_rounded_rect_border(frame, x, y, w, h, color, thickness=1, radius=12):
    r = min(radius, w // 2, h // 2)
    cv2.line(frame, (x + r, y), (x + w - r, y), color, thickness)
    cv2.line(frame, (x + r, y + h), (x + w - r, y + h), color, thickness)
    cv2.line(frame, (x, y + r), (x, y + h - r), color, thickness)
    cv2.line(frame, (x + w, y + r), (x + w, y + h - r), color, thickness)
    cv2.ellipse(frame, (x + r, y + r), (r, r), 180, 0, 90, color, thickness)
    cv2.ellipse(frame, (x + w - r, y + r), (r, r), 270, 0, 90, color, thickness)
    cv2.ellipse(frame, (x + r, y + h - r), (r, r), 90, 0, 90, color, thickness)
    cv2.ellipse(frame, (x + w - r, y + h - r), (r, r), 0, 0, 90, color, thickness)


def draw_glow_line(frame, pt1, pt2, color, thickness=2, glow_size=6, glow_alpha=0.12):
    overlay = frame.copy()
    cv2.line(overlay, pt1, pt2, color, thickness + glow_size)
    cv2.addWeighted(overlay, glow_alpha, frame, 1 - glow_alpha, 0, frame)
    cv2.line(frame, pt1, pt2, color, thickness)


def draw_corner_brackets(frame, x1, y1, x2, y2, color, thickness=2, length=18):
    cv2.line(frame, (x1, y1), (x1 + length, y1), color, thickness)
    cv2.line(frame, (x1, y1), (x1, y1 + length), color, thickness)
    cv2.line(frame, (x2, y1), (x2 - length, y1), color, thickness)
    cv2.line(frame, (x2, y1), (x2, y1 + length), color, thickness)
    cv2.line(frame, (x1, y2), (x1 + length, y2), color, thickness)
    cv2.line(frame, (x1, y2), (x1, y2 - length), color, thickness)
    cv2.line(frame, (x2, y2), (x2 - length, y2), color, thickness)
    cv2.line(frame, (x2, y2), (x2, y2 - length), color, thickness)


def draw_scan_line(frame, x1, y1, x2, y2, color, t):
    box_h = max(y2 - y1, 1)
    scan_y = y1 + int((t * 60) % box_h)
    overlay = frame.copy()
    cv2.line(overlay, (x1, scan_y), (x2, scan_y), color, 1)
    cv2.addWeighted(overlay, 0.35, frame, 0.65, 0, frame)


def draw_detection_box(frame, x1, y1, x2, y2, label, color, risk_val, t):
    draw_transparent_rect(frame, x1, y1, x2 - x1, y2 - y1, color, 0.07)
    draw_corner_brackets(frame, x1, y1, x2, y2, color, thickness=2, length=20)
    draw_scan_line(frame, x1, y1, x2, y2, color, t)

    tag_text = label.upper()
    (tw, th), _ = cv2.getTextSize(tag_text, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1)
    tag_w, tag_h = tw + 14, th + 10
    tag_y = y1 - tag_h - 3 if y1 - tag_h - 3 > 0 else y2 + 3
    draw_rounded_rect(frame, x1, tag_y, tag_w, tag_h, color, alpha=0.7, radius=5)
    cv2.putText(frame, tag_text, (x1 + 7, tag_y + th + 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, C_WHITE, 1, cv2.LINE_AA)

    dot_col = C_NEON_RED if risk_val > 90000 else (C_NEON_YELLOW if risk_val > 60000 else C_NEON_GREEN)
    cv2.circle(frame, (x2 - 6, y1 + 6), 4, dot_col, -1)


# ================== HUD ==================

def draw_dashcam_hud(frame, risk, fps_val, t, fc):
    """Professional HUD overlay for live dashcam."""
    h, w, _ = frame.shape

    # ──── TOP BAR ────
    draw_rounded_rect(frame, 0, 0, w, 50, C_BG_DARK, 0.8, radius=0)

    # Animated accent line
    accent_w = int(w * 0.5)
    bar_x = int((t * 70) % (w + accent_w)) - accent_w
    end_x = min(bar_x + accent_w, w)
    if bar_x < w and end_x > 0:
        overlay = frame.copy()
        cv2.line(overlay, (max(bar_x, 0), 49), (end_x, 49), C_ACCENT_CYAN, 2)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)

    # Title
    cv2.putText(frame, "VISIONDRIVE", (14, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.5, C_ACCENT_CYAN, 1, cv2.LINE_AA)
    cv2.putText(frame, "LIVE DASHCAM", (14, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.35, C_NEON_GREEN, 1, cv2.LINE_AA)

    # Live indicator
    if fc % 40 < 28:
        cv2.circle(frame, (w - 28, 18), 5, C_NEON_RED, -1)
        cv2.putText(frame, "LIVE", (w - 62, 23), cv2.FONT_HERSHEY_SIMPLEX, 0.35, C_NEON_RED, 1, cv2.LINE_AA)

    # FPS
    cv2.putText(frame, f"FPS: {int(fps_val)}", (w - 100, 43),
                cv2.FONT_HERSHEY_SIMPLEX, 0.35, C_WHITE_DIM, 1, cv2.LINE_AA)

    # Timestamp
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    cv2.putText(frame, ts, (w // 2 - 35, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.4, C_WHITE_DIM, 1, cv2.LINE_AA)

    # ──── RISK PANEL (top-right) ────
    risk_col = C_NEON_RED if risk > 75 else (C_NEON_YELLOW if risk > 40 else C_NEON_GREEN)
    panel_x = w - 180
    draw_rounded_rect(frame, panel_x, 58, 170, 48, C_BG_DARK, 0.7, radius=8)
    draw_rounded_rect_border(frame, panel_x, 58, 170, 48, risk_col, 1, 8)
    cv2.putText(frame, "RISK", (panel_x + 10, 78), cv2.FONT_HERSHEY_SIMPLEX, 0.35, C_WHITE_DIM, 1, cv2.LINE_AA)
    cv2.putText(frame, f"{int(risk)}%", (panel_x + 55, 78), cv2.FONT_HERSHEY_SIMPLEX, 0.4, risk_col, 1, cv2.LINE_AA)

    # Mini risk bar
    bar_x2 = panel_x + 10
    bar_y = 86
    bar_w = 150
    bar_h = 10
    draw_rounded_rect(frame, bar_x2, bar_y, bar_w, bar_h, C_GRID_DIM, 0.7, radius=4)
    fill_w = max(int((risk / 100) * bar_w), 1)
    if fill_w > 3:
        draw_rounded_rect(frame, bar_x2, bar_y, fill_w, bar_h, risk_col, 0.85, radius=4)

    # ──── GUIDANCE PANEL (center) ────
    if risk > 80:
        guidance = "CRITICAL: SLOW DOWN"
    elif risk > 50:
        guidance = "STAY ALERT"
    else:
        guidance = "ALL CLEAR"

    g_col = C_NEON_RED if risk > 80 else (C_NEON_YELLOW if risk > 50 else C_NEON_GREEN)
    gp_w = 280
    gp_x = w // 2 - gp_w // 2
    draw_rounded_rect(frame, gp_x, 58, gp_w, 32, C_BG_DARK, 0.65, radius=8)
    draw_rounded_rect_border(frame, gp_x, 58, gp_w, 32, g_col, 1, 8)
    cv2.putText(frame, guidance, (gp_x + 15, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.45, g_col, 1, cv2.LINE_AA)

    # ──── BOTTOM BAR ────
    draw_rounded_rect(frame, 0, h - 50, w, 50, C_BG_DARK, 0.8, radius=0)
    cv2.line(frame, (0, h - 50), (w, h - 50), C_BORDER, 1)

    # Webcam label
    cv2.putText(frame, "WEBCAM 0", (14, h - 28), cv2.FONT_HERSHEY_SIMPLEX, 0.35, C_WHITE_DIM, 1, cv2.LINE_AA)
    cv2.putText(frame, f"{DISPLAY_W}x{DISPLAY_H}", (14, h - 12), cv2.FONT_HERSHEY_SIMPLEX, 0.3, C_GRID_DIM, 1, cv2.LINE_AA)

    # Animated bars (bottom-right)
    for i in range(5):
        bar_h_anim = int(6 + abs(math.sin(t * 5 + i * 1.2)) * 12)
        bx = w - 28 + i * 6
        by = h - 12
        cv2.line(frame, (bx, by), (bx, by - bar_h_anim), C_ACCENT_CYAN, 2)

    # Crosshair center marker
    cx, cy = w // 2, h // 2
    cross_len = 12
    cv2.line(frame, (cx - cross_len, cy), (cx + cross_len, cy), C_GRID_DIM, 1)
    cv2.line(frame, (cx, cy - cross_len), (cx, cy + cross_len), C_GRID_DIM, 1)
    cv2.circle(frame, (cx, cy), 5, C_GRID_DIM, 1)


# ================== FRAME GENERATOR ==================

def generate_frames():
    """Capture webcam, run YOLO + HUD, yield JPEG frames."""
    global current_fps, is_active, shutdown_flag

    print("[DASHCAM] Loading YOLOv8 model...")
    model = YOLO("yolov8n.pt")

    print(f"[DASHCAM] Opening webcam {WEBCAM_INDEX}...")
    cap = cv2.VideoCapture(WEBCAM_INDEX)

    if not cap.isOpened():
        print("[DASHCAM] ERROR: Cannot open webcam!")
        is_active = False
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, DISPLAY_W)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, DISPLAY_H)

    is_active = True
    frame_count = 0
    prev_time = time.time()
    smoothed_risk = 0
    SMOOTH_ALPHA = 0.2
    RISK_SCALE = 150000

    print(f"[DASHCAM] Streaming at {DISPLAY_W}x{DISPLAY_H}...")

    while not shutdown_flag:
        ret, frame = cap.read()
        if not ret:
            time.sleep(0.01)
            continue

        frame = cv2.resize(frame, (DISPLAY_W, DISPLAY_H))
        curr_time = time.time()
        frame_count += 1

        # ─── Detection ───
        h_f, w_f, _ = frame.shape
        HOOD_Y_LIMIT = int(h_f * 0.85)
        max_w_area = 0
        detected = []

        results = model(frame, stream=True, verbose=False)
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                label = model.names[int(box.cls[0])]
                if float(box.conf[0]) < 0.4 or y2 > HOOD_Y_LIMIT:
                    continue
                w_area = ((x2 - x1) * (y2 - y1)) * PRIORITY.get(label, 1.0)
                max_w_area = max(max_w_area, w_area)
                col = C_NEON_RED if w_area > 90000 else (C_NEON_YELLOW if w_area > 60000 else C_ACCENT_CYAN)
                detected.append({"coords": (x1, y1, x2, y2), "label": label, "col": col, "risk": w_area})

        raw_risk = min(100, int((max_w_area / RISK_SCALE) * 100))
        smoothed_risk = int(SMOOTH_ALPHA * raw_risk + (1 - SMOOTH_ALPHA) * smoothed_risk)

        # ─── Draw detections ───
        detected.sort(key=lambda x: x["risk"], reverse=True)
        for obj in detected[:5]:
            x1, y1, x2, y2 = obj["coords"]
            draw_detection_box(frame, x1, y1, x2, y2, obj["label"], obj["col"], obj["risk"], curr_time)

        # ─── FPS ───
        dt = curr_time - prev_time
        if dt > 0:
            current_fps = 0.8 * current_fps + 0.2 * (1.0 / dt)
        prev_time = curr_time

        # ─── HUD ───
        draw_dashcam_hud(frame, smoothed_risk, current_fps, curr_time, frame_count)

        # ─── Encode and yield as MJPEG ───
        _, jpeg = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY])
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

    cap.release()
    is_active = False
    print("[DASHCAM] Stream stopped.")


# ================== FLASK SERVER ==================

app = Flask(__name__)

@app.route('/feed')
def video_feed():
    """MJPEG streaming endpoint."""
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route('/status')
def status():
    """Return dashcam status as JSON."""
    return jsonify({
        "active": is_active,
        "fps": round(current_fps, 1),
        "resolution": f"{DISPLAY_W}x{DISPLAY_H}"
    })

@app.route('/stop')
def stop():
    """Gracefully shutdown the dashcam server."""
    global shutdown_flag
    shutdown_flag = True
    func = threading.Timer(1.0, lambda: os._exit(0))
    func.daemon = True
    func.start()
    return jsonify({"status": "stopping"})


def signal_handler(sig, frame):
    global shutdown_flag
    shutdown_flag = True
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == '__main__':
    import os
    print("=" * 50)
    print("  VisionDrive Live Dashcam Server")
    print(f"  Stream:  http://localhost:8001/feed")
    print(f"  Status:  http://localhost:8001/status")
    print("=" * 50)
    app.run(host='0.0.0.0', port=8001, threaded=True)
