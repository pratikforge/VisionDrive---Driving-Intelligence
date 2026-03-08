import cv2
import numpy as np
from ultralytics import YOLO
import time
import os
import datetime
import glob
import webbrowser
import threading
import requests
import math
from collections import deque
from staticmap import StaticMap, CircleMarker
from io import BytesIO

# ================== CONFIGURATION ==================
VIDEO_SOURCE = "video.mp4"   # or 0 for webcam
DISPLAY_W, DISPLAY_H = 1280, 720

# Black Box Settings
BB_FOLDER = os.path.join(os.path.dirname(__file__), "blackbox_data")
CHUNK_DURATION = 10
MAX_HISTORY = 5

# ─── Premium Color Palette ───
C_BG_DARK     = (15, 15, 20)
C_BG_PANEL    = (25, 25, 35)
C_ACCENT_CYAN = (230, 216, 0)      # Neon cyan (BGR)
C_ACCENT_BLUE = (255, 160, 50)     # Electric blue
C_NEON_GREEN  = (100, 255, 120)
C_NEON_YELLOW = (50, 230, 255)
C_NEON_RED    = (60, 60, 255)
C_NEON_ORANGE = (50, 140, 255)
C_WHITE       = (255, 255, 255)
C_WHITE_DIM   = (180, 180, 190)
C_BLACK       = (0, 0, 0)
C_GRID_DIM    = (40, 40, 55)
C_BORDER      = (70, 70, 90)
C_MAP_ACCENT  = (255, 100, 50)
C_PURPLE      = (200, 50, 160)

# Map Settings (Thakur Shyamnarayan Engineering College, Mumbai)
MAP_LAT = 19.2094
MAP_LNG = 72.8727
MAP_ZOOM = 16
MAP_W, MAP_H = 300, 300

# ================== BLACK BOX ENGINE ==================
class BlackBoxSystem:
    def __init__(self, folder_path, max_files=5):
        self.folder = folder_path
        self.max_files = max_files
        self.file_queue = deque()
        self.writer = None
        self.current_filename = None
        self.start_time = 0
        self.is_recording = False
        self.locked = False

        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

        existing = sorted(glob.glob(os.path.join(self.folder, "rec_*.mp4")))
        for f in existing[-max_files:]:
            self.file_queue.append(f)

    def start_new_chunk(self, frame_size, fps):
        if self.locked:
            return
        if self.writer:
            self.writer.release()

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.current_filename = os.path.join(
            self.folder, f"rec_{timestamp}.mp4"
        )

        fourcc = cv2.VideoWriter_fourcc(*"avc1")
        self.writer = cv2.VideoWriter(
            self.current_filename, fourcc, fps, frame_size
        )

        self.file_queue.append(self.current_filename)

        while len(self.file_queue) > self.max_files:
            old = self.file_queue.popleft()
            if os.path.exists(old):
                try:
                    os.remove(old)
                except:
                    pass

        self.start_time = time.time()
        self.is_recording = True

    def update(self, frame, speed, risk):
        if not self.is_recording or self.locked:
            return
        if self.writer:
            self.writer.write(frame)
        if time.time() - self.start_time > CHUNK_DURATION:
            h, w, _ = frame.shape
            self.start_new_chunk((w, h), 24.0)

    def emergency_lock(self):
        if self.locked:
            return
        self.locked = True
        self.is_recording = False
        if self.writer:
            self.writer.release()
            self.writer = None
        print("\n[BLACK BOX] 🛑 AIRBAG DEPLOYED. SYSTEM FROZEN. 🛑")

    def release(self):
        if self.writer:
            self.writer.release()

# ================== NAVIGATION STATE ==================
nav_state = "STRAIGHT"
dist_to_turn = 200

# ================== SETUP ==================
print("Booting VisionDrive AR System...")
model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(VIDEO_SOURCE)

black_box = BlackBoxSystem(BB_FOLDER, max_files=MAX_HISTORY)
black_box.start_new_chunk((DISPLAY_W, DISPLAY_H), 24.0)

prev_time = 0
smoothed_risk = 0
SMOOTH_ALPHA = 0.2
RISK_SCALE = 150000

system_status = "NORMAL"
airbag_deployed = False
emergency_call_sent = False
frame_count = 0  # Global frame counter for animations

BACKEND_URL = "http://localhost:8000"

PRIORITY = {
    "motorbike": 4.0, "bicycle": 4.0, "person": 3.0,
    "car": 2.5, "truck": 2.0, "bus": 2.0
}

# ================== EMERGENCY CALL ==================
def trigger_emergency_call():
    """Open tel:112 via OS handler (Phone Link) and log to backend."""
    global emergency_call_sent
    try:
        webbrowser.open("tel:112")
        print("\n[EMERGENCY] ☎️  DIALING 112 via Phone Link...")
    except Exception as e:
        print(f"[EMERGENCY] Failed to open tel: handler: {e}")

    try:
        requests.post(
            f"{BACKEND_URL}/api/emergency-call",
            json={
                "event": "airbag_deployed",
                "number": "112",
                "timestamp": datetime.datetime.now().isoformat()
            },
            timeout=3
        )
        print("[EMERGENCY] Backend notified.")
    except Exception as e:
        print(f"[EMERGENCY] Backend notification failed: {e}")

    emergency_call_sent = True

# ================================================================
#                      DRAWING UTILITIES
# ================================================================

def draw_transparent_rect(frame, x, y, w, h, color, alpha=0.5):
    """Draw a semi-transparent filled rectangle."""
    overlay = frame.copy()
    cv2.rectangle(overlay, (x, y), (x + w, y + h), color, -1)
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)


def draw_rounded_rect(frame, x, y, w, h, color, alpha=0.5, radius=12):
    """Draw a semi-transparent rounded rectangle with smooth corners."""
    overlay = frame.copy()
    # Clamp radius
    r = min(radius, w // 2, h // 2)
    # Draw the 4 corner circles and the rectangles to form the rounded shape
    cv2.rectangle(overlay, (x + r, y), (x + w - r, y + h), color, -1)
    cv2.rectangle(overlay, (x, y + r), (x + w, y + h - r), color, -1)
    cv2.circle(overlay, (x + r, y + r), r, color, -1)
    cv2.circle(overlay, (x + w - r, y + r), r, color, -1)
    cv2.circle(overlay, (x + r, y + h - r), r, color, -1)
    cv2.circle(overlay, (x + w - r, y + h - r), r, color, -1)
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)


def draw_rounded_rect_border(frame, x, y, w, h, color, thickness=1, radius=12):
    """Draw a rounded rectangle border (outline only)."""
    r = min(radius, w // 2, h // 2)
    # Top, bottom lines
    cv2.line(frame, (x + r, y), (x + w - r, y), color, thickness)
    cv2.line(frame, (x + r, y + h), (x + w - r, y + h), color, thickness)
    # Left, right lines
    cv2.line(frame, (x, y + r), (x, y + h - r), color, thickness)
    cv2.line(frame, (x + w, y + r), (x + w, y + h - r), color, thickness)
    # Corner arcs
    cv2.ellipse(frame, (x + r, y + r), (r, r), 180, 0, 90, color, thickness)
    cv2.ellipse(frame, (x + w - r, y + r), (r, r), 270, 0, 90, color, thickness)
    cv2.ellipse(frame, (x + r, y + h - r), (r, r), 90, 0, 90, color, thickness)
    cv2.ellipse(frame, (x + w - r, y + h - r), (r, r), 0, 0, 90, color, thickness)


def draw_glow_line(frame, pt1, pt2, color, thickness=2, glow_size=8, glow_alpha=0.15):
    """Draw a line with a soft glow effect around it."""
    overlay = frame.copy()
    cv2.line(overlay, pt1, pt2, color, thickness + glow_size)
    cv2.addWeighted(overlay, glow_alpha, frame, 1 - glow_alpha, 0, frame)
    cv2.line(frame, pt1, pt2, color, thickness)


def draw_corner_brackets(frame, x1, y1, x2, y2, color, thickness=2, length=20, gap=3):
    """Draw modern corner brackets with a gap for a cleaner look."""
    # Top-left
    cv2.line(frame, (x1, y1 + gap), (x1, y1 + length), color, thickness)
    cv2.line(frame, (x1 + gap, y1), (x1 + length, y1), color, thickness)
    # Top-right
    cv2.line(frame, (x2, y1 + gap), (x2, y1 + length), color, thickness)
    cv2.line(frame, (x2 - gap, y1), (x2 - length, y1), color, thickness)
    # Bottom-left
    cv2.line(frame, (x1, y2 - gap), (x1, y2 - length), color, thickness)
    cv2.line(frame, (x1 + gap, y2), (x1 + length, y2), color, thickness)
    # Bottom-right
    cv2.line(frame, (x2, y2 - gap), (x2, y2 - length), color, thickness)
    cv2.line(frame, (x2 - gap, y2), (x2 - length, y2), color, thickness)


def draw_scan_line(frame, x1, y1, x2, y2, color, t):
    """Draw an animated scanning line that moves vertically through a bounding box."""
    box_h = y2 - y1
    scan_y = y1 + int((t * 60) % box_h)
    overlay = frame.copy()
    cv2.line(overlay, (x1, scan_y), (x2, scan_y), color, 1)
    cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)


def draw_detection_box(frame, x1, y1, x2, y2, label, color, risk_val, t):
    """Professional detection box with corner brackets, label tag, and scan line."""
    # Subtle filled background
    draw_transparent_rect(frame, x1, y1, x2 - x1, y2 - y1, color, 0.08)

    # Corner brackets
    draw_corner_brackets(frame, x1, y1, x2, y2, color, thickness=2, length=22)

    # Scan line animation
    draw_scan_line(frame, x1, y1, x2, y2, color, t)

    # Label tag with rounded background
    tag_text = label.upper()
    (tw, th), _ = cv2.getTextSize(tag_text, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)
    tag_w = tw + 16
    tag_h = th + 12
    tag_x = x1
    tag_y = y1 - tag_h - 4
    if tag_y < 0:
        tag_y = y2 + 4

    draw_rounded_rect(frame, tag_x, tag_y, tag_w, tag_h, color, alpha=0.7, radius=6)
    cv2.putText(frame, tag_text, (tag_x + 8, tag_y + th + 6),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, C_WHITE, 1, cv2.LINE_AA)

    # Tiny risk indicator dot
    dot_x = x2 - 6
    dot_y = y1 + 6
    dot_col = C_NEON_RED if risk_val > 90000 else (C_NEON_YELLOW if risk_val > 60000 else C_NEON_GREEN)
    cv2.circle(frame, (dot_x, dot_y), 4, dot_col, -1)


def draw_ar_arrow(frame, lane_left, lane_right, direction="LEFT"):
    """Draw animated AR arrow with glow effect."""
    h, w, _ = frame.shape
    center_x = (lane_left + lane_right) // 2
    color = C_ACCENT_CYAN
    pts = []
    if direction == "LEFT":
        pts = np.array([[center_x, h - 50], [center_x - 40, h - 100], [center_x - 20, h - 100],
                         [center_x - 60, h - 180], [center_x + 20, h - 100], [center_x + 40, h - 100],
                         [center_x + 80, h - 50]])
    elif direction == "RIGHT":
        pts = np.array([[center_x, h - 50], [center_x - 40, h - 100], [center_x - 20, h - 100],
                         [center_x + 60, h - 180], [center_x + 20, h - 100], [center_x + 40, h - 100],
                         [center_x + 80, h - 50]])

    if len(pts) > 0:
        # Glow layer
        glow = frame.copy()
        cv2.fillPoly(glow, [pts], color)
        pulse = 0.3 + abs(math.sin(time.time() * 4)) * 0.25
        cv2.addWeighted(glow, pulse, frame, 1 - pulse, 0, frame)
        # Edge lines
        cv2.polylines(frame, [pts], True, C_WHITE, 1, cv2.LINE_AA)

# ================================================================
#                      MAP OVERLAY
# ================================================================

def fetch_map_image():
    """Fetch a static map image from OpenStreetMap (called once at startup)."""
    try:
        print("[MAP] Fetching OpenStreetMap tile...")
        m = StaticMap(MAP_W, MAP_H, url_template='https://tile.openstreetmap.org/{z}/{x}/{y}.png')
        marker = CircleMarker((MAP_LNG, MAP_LAT), 'red', 12)
        m.add_marker(marker)
        pil_img = m.render(zoom=MAP_ZOOM, center=(MAP_LNG, MAP_LAT))
        img_array = np.array(pil_img)
        map_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        print("[MAP] Map loaded successfully.")
        return map_cv
    except Exception as e:
        print(f"[MAP] Failed to fetch map: {e}")
        fallback = np.zeros((MAP_H, MAP_W, 3), dtype=np.uint8)
        fallback[:] = (30, 30, 30)
        cv2.putText(fallback, "MAP UNAVAILABLE", (30, MAP_H // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, C_WHITE, 1)
        return fallback


def generate_map_frame():
    """Return the cached map with a styled HUD overlay."""
    display = cached_map.copy()

    # Darken top bar
    draw_rounded_rect(display, 4, 4, MAP_W - 8, 50, C_BG_DARK, alpha=0.75, radius=8)

    # Title
    cv2.putText(display, "LIVE MAP", (14, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.45, C_ACCENT_CYAN, 1, cv2.LINE_AA)

    # Nav info
    cv2.putText(display, f"{int(dist_to_turn)}m", (14, 48), cv2.FONT_HERSHEY_DUPLEX, 0.5, C_WHITE, 1, cv2.LINE_AA)
    cv2.putText(display, nav_state, (80, 48), cv2.FONT_HERSHEY_SIMPLEX, 0.45, C_NEON_GREEN, 1, cv2.LINE_AA)

    # Animated pulse dot (current location indicator)
    pulse_r = int(6 + abs(math.sin(time.time() * 3)) * 4)
    cv2.circle(display, (MAP_W - 30, 30), pulse_r, C_NEON_GREEN, -1)
    cv2.circle(display, (MAP_W - 30, 30), pulse_r + 4, C_NEON_GREEN, 1)

    # Bottom info bar
    draw_rounded_rect(display, 4, MAP_H - 35, MAP_W - 8, 31, C_BG_DARK, alpha=0.7, radius=6)
    now_str = datetime.datetime.now().strftime("%H:%M:%S")
    cv2.putText(display, now_str, (14, MAP_H - 14), cv2.FONT_HERSHEY_SIMPLEX, 0.4, C_WHITE_DIM, 1, cv2.LINE_AA)
    cv2.putText(display, "OSM", (MAP_W - 45, MAP_H - 14), cv2.FONT_HERSHEY_SIMPLEX, 0.35, C_WHITE_DIM, 1, cv2.LINE_AA)

    # Border
    draw_rounded_rect_border(display, 2, 2, MAP_W - 4, MAP_H - 4, C_BORDER, 1, 10)

    return display

# ================================================================
#                   MAIN HUD DRAWING
# ================================================================

def draw_hud(frame, risk, status, t, fc):
    """
    Professional heads-up display with animated elements.
    t  = current time.time()
    fc = frame counter
    """
    h, w, _ = frame.shape

    # ──────────── TOP BAR ────────────
    draw_rounded_rect(frame, 0, 0, w, 54, C_BG_DARK, 0.8, radius=0)

    # Animated border accent
    accent_w = int(w * 0.6)
    bar_x = int((t * 80) % (w + accent_w)) - accent_w
    end_x = min(bar_x + accent_w, w)
    if bar_x < w and end_x > 0:
        draw_x = max(bar_x, 0)
        overlay = frame.copy()
        cv2.line(overlay, (draw_x, 53), (end_x, 53), C_ACCENT_CYAN, 2)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)

    # Title with icon
    cv2.putText(frame, "VISIONDRIVE", (18, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.55, C_ACCENT_CYAN, 1, cv2.LINE_AA)
    cv2.putText(frame, "AR NAV SYSTEM", (18, 44), cv2.FONT_HERSHEY_SIMPLEX, 0.35, C_WHITE_DIM, 1, cv2.LINE_AA)

    # Live recording indicator (blinking)
    if fc % 40 < 28:  # ~70% on
        cv2.circle(frame, (w - 30, 20), 5, C_NEON_RED, -1)
        cv2.putText(frame, "REC", (w - 65, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.35, C_NEON_RED, 1, cv2.LINE_AA)

    # FPS counter
    cv2.putText(frame, f"FPS: {int(1 / max(0.001, t - prev_time))}", (w - 130, 45),
                cv2.FONT_HERSHEY_SIMPLEX, 0.35, C_WHITE_DIM, 1, cv2.LINE_AA)

    # ──────────── GUIDANCE PANEL (NORMAL) ────────────
    if status == "NORMAL":
        # Determine safety message
        if risk > 80:
            safety_act = "CRITICAL: SLOW DOWN"
        elif risk > 50:
            safety_act = "STAY ALERT"
        else:
            safety_act = "CLEAR PATH"

        guidance_text = f"{nav_state}  //  {safety_act}"
        g_col = C_NEON_RED if risk > 80 else (C_NEON_YELLOW if risk > 50 else C_NEON_GREEN)

        panel_w = 520
        panel_x = w // 2 - panel_w // 2
        draw_rounded_rect(frame, panel_x, 62, panel_w, 40, C_BG_DARK, 0.7, radius=10)
        draw_rounded_rect_border(frame, panel_x, 62, panel_w, 40, g_col, 1, 10)
        cv2.putText(frame, guidance_text, (panel_x + 20, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, g_col, 1, cv2.LINE_AA)

        # Direction indicator on right
        dir_icon = "<" if nav_state == "LEFT" else (">" if nav_state == "RIGHT" else "|")
        cv2.putText(frame, dir_icon, (panel_x + panel_w - 30, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, C_WHITE, 2, cv2.LINE_AA)

    # ──────────── EMERGENCY OVERLAY (LOCKED) ────────────
    if status == "LOCKED":
        # Full-screen subtle red vignette
        vignette = frame.copy()
        cv2.rectangle(vignette, (0, 0), (w, h), C_NEON_RED, -1)
        pulse_alpha = 0.05 + abs(math.sin(t * 3)) * 0.08
        cv2.addWeighted(vignette, pulse_alpha, frame, 1 - pulse_alpha, 0, frame)

        # Central panel
        panel_w, panel_h = 500, 200
        px, py = w // 2 - panel_w // 2, h // 2 - panel_h // 2
        draw_rounded_rect(frame, px, py, panel_w, panel_h, C_BG_DARK, 0.92, radius=16)

        # Pulsing red border
        border_col = (60, 60, int(150 + abs(math.sin(t * 4)) * 105))
        draw_rounded_rect_border(frame, px, py, panel_w, panel_h, border_col, 2, 16)

        # Warning icon (triangle)
        tri_cx, tri_cy = w // 2, py + 45
        tri_pts = np.array([[tri_cx, tri_cy - 18], [tri_cx - 16, tri_cy + 12], [tri_cx + 16, tri_cy + 12]])
        cv2.fillPoly(frame, [tri_pts], C_NEON_YELLOW)
        cv2.putText(frame, "!", (tri_cx - 5, tri_cy + 8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, C_BG_DARK, 2, cv2.LINE_AA)

        cv2.putText(frame, "AIRBAG DEPLOYED", (w // 2 - 130, py + 85),
                    cv2.FONT_HERSHEY_DUPLEX, 0.9, C_WHITE, 2, cv2.LINE_AA)
        cv2.putText(frame, "SYSTEM FROZEN - ALL DATA LOCKED", (w // 2 - 170, py + 115),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, C_WHITE_DIM, 1, cv2.LINE_AA)

        # Flashing 112 text with phone icon
        call_text = "CALLING 112..."
        if int(t * 3) % 2 == 0:
            cv2.putText(frame, call_text, (w // 2 - 100, py + 160),
                        cv2.FONT_HERSHEY_DUPLEX, 0.75, C_NEON_YELLOW, 2, cv2.LINE_AA)
        else:
            cv2.putText(frame, call_text, (w // 2 - 100, py + 160),
                        cv2.FONT_HERSHEY_DUPLEX, 0.75, C_NEON_RED, 2, cv2.LINE_AA)

    # ──────────── BOTTOM DASHBOARD ────────────
    draw_rounded_rect(frame, 0, h - 85, w, 85, C_BG_DARK, 0.85, radius=0)

    # Top edge accent line
    cv2.line(frame, (0, h - 85), (w, h - 85), C_BORDER, 1)

    # ─ Risk Meter ─
    meter_x, meter_y = 24, h - 55
    meter_w, meter_h = 250, 16
    r_col = C_NEON_RED if risk > 75 else (C_NEON_YELLOW if risk > 40 else C_NEON_GREEN)

    cv2.putText(frame, "RISK", (meter_x, meter_y - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.4, C_WHITE_DIM, 1, cv2.LINE_AA)
    cv2.putText(frame, f"{int(risk)}%", (meter_x + 45, meter_y - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.4, r_col, 1, cv2.LINE_AA)

    # Background bar
    draw_rounded_rect(frame, meter_x, meter_y, meter_w, meter_h, C_GRID_DIM, 0.8, radius=5)
    # Filled bar with animated gradient segments
    fill_w = int((risk / 100) * meter_w)
    if fill_w > 4:
        draw_rounded_rect(frame, meter_x, meter_y, fill_w, meter_h, r_col, 0.9, radius=5)
        # Animated shimmer on filled bar
        shimmer_x = int((t * 120) % fill_w) + meter_x
        if shimmer_x < meter_x + fill_w - 10:
            overlay = frame.copy()
            cv2.rectangle(overlay, (shimmer_x, meter_y), (shimmer_x + 20, meter_y + meter_h), C_WHITE, -1)
            cv2.addWeighted(overlay, 0.15, frame, 0.85, 0, frame)

    # ─ Navigation Info ─
    nav_x = 310
    cv2.putText(frame, "NAV", (nav_x, h - 61), cv2.FONT_HERSHEY_SIMPLEX, 0.35, C_WHITE_DIM, 1, cv2.LINE_AA)
    cv2.putText(frame, nav_state, (nav_x + 40, h - 61), cv2.FONT_HERSHEY_SIMPLEX, 0.45, C_ACCENT_CYAN, 1, cv2.LINE_AA)
    cv2.putText(frame, f"{int(dist_to_turn)}m to next turn", (nav_x, h - 38),
                cv2.FONT_HERSHEY_SIMPLEX, 0.35, C_WHITE_DIM, 1, cv2.LINE_AA)

    # ─ Black Box Status ─
    bb_x = 530
    cv2.putText(frame, "BLACK BOX", (bb_x, h - 61), cv2.FONT_HERSHEY_SIMPLEX, 0.35, C_WHITE_DIM, 1, cv2.LINE_AA)
    if black_box.locked:
        cv2.putText(frame, "LOCKED", (bb_x + 90, h - 61), cv2.FONT_HERSHEY_SIMPLEX, 0.4, C_NEON_RED, 1, cv2.LINE_AA)
    else:
        cv2.putText(frame, "RECORDING", (bb_x + 90, h - 61), cv2.FONT_HERSHEY_SIMPLEX, 0.4, C_NEON_GREEN, 1, cv2.LINE_AA)
        # Animated recording bar
        rec_elapsed = time.time() - black_box.start_time
        rec_pct = min(rec_elapsed / CHUNK_DURATION, 1.0)
        bar_w = 160
        draw_rounded_rect(frame, bb_x, h - 45, bar_w, 8, C_GRID_DIM, 0.6, radius=4)
        draw_rounded_rect(frame, bb_x, h - 45, int(rec_pct * bar_w), 8, C_NEON_GREEN, 0.8, radius=4)
        cv2.putText(frame, f"{int(rec_elapsed)}s / {CHUNK_DURATION}s", (bb_x, h - 28),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.3, C_WHITE_DIM, 1, cv2.LINE_AA)

    # ─ System Status ─
    status_x = w - 180
    cv2.putText(frame, "STATUS", (status_x, h - 61), cv2.FONT_HERSHEY_SIMPLEX, 0.35, C_WHITE_DIM, 1, cv2.LINE_AA)
    s_col = C_NEON_RED if status == "LOCKED" else C_NEON_GREEN
    s_txt = "EMERGENCY" if status == "LOCKED" else "NORMAL"
    cv2.putText(frame, s_txt, (status_x, h - 38), cv2.FONT_HERSHEY_SIMPLEX, 0.5, s_col, 1, cv2.LINE_AA)

    # ──────────── CORNER DECORATIONS ────────────
    # Top-right: subtle grid crosshair
    cr_x, cr_y = w - 80, 70
    cv2.line(frame, (cr_x - 12, cr_y), (cr_x + 12, cr_y), C_GRID_DIM, 1)
    cv2.line(frame, (cr_x, cr_y - 12), (cr_x, cr_y + 12), C_GRID_DIM, 1)
    cv2.circle(frame, (cr_x, cr_y), 6, C_GRID_DIM, 1)

    # Bottom-right: tiny animated bars (audio-meter style)
    for i in range(5):
        bar_h_anim = int(8 + abs(math.sin(t * 5 + i * 1.2)) * 14)
        bx = w - 30 + i * 6
        by = h - 20
        cv2.line(frame, (bx, by), (bx, by - bar_h_anim), C_ACCENT_CYAN, 2)


def draw_lane_overlay(frame, risk, t):
    """Draw the lane detection trapezoid with animated edge pulses."""
    h, w, _ = frame.shape
    lane_left, lane_right = int(w * 0.25), int(w * 0.75)

    t_col = C_NEON_RED if risk > 70 else (C_NEON_YELLOW if risk > 40 else C_NEON_GREEN)

    # Lane fill
    pts = np.array([[lane_left, h], [int(w * 0.42), h // 2 + 50],
                     [int(w * 0.58), h // 2 + 50], [lane_right, h]], np.int32)
    overlay = frame.copy()
    cv2.fillPoly(overlay, [pts], t_col)
    cv2.addWeighted(overlay, 0.15, frame, 0.85, 0, frame)

    # Lane edge lines with glow
    draw_glow_line(frame, (lane_left, h), (int(w * 0.42), h // 2 + 50), t_col, 2, 6, 0.12)
    draw_glow_line(frame, (lane_right, h), (int(w * 0.58), h // 2 + 50), t_col, 2, 6, 0.12)

    # Animated dashes along lane edges
    dash_count = 8
    for i in range(dash_count):
        frac = (i / dash_count + (t * 0.3) % 1) % 1
        alpha = 1.0 - frac  # Fade as they move up
        # Left edge
        lx = int(lane_left + (int(w * 0.42) - lane_left) * frac)
        ly = int(h + (h // 2 + 50 - h) * frac)
        col_faded = tuple(int(c * alpha) for c in t_col)
        cv2.circle(frame, (lx, ly), 3, col_faded, -1)
        # Right edge
        rx = int(lane_right + (int(w * 0.58) - lane_right) * frac)
        cv2.circle(frame, (rx, ly), 3, col_faded, -1)

    return lane_left, lane_right


# ================================================================
#                          MAIN LOOP
# ================================================================
cached_map = fetch_map_image()

while True:
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    frame = cv2.resize(frame, (DISPLAY_W, DISPLAY_H))
    curr_time = time.time()
    frame_count += 1

    # --- 1. DETECTION & RISK ---
    results = model(frame, stream=True, verbose=False)
    h, w, _ = frame.shape
    HOOD_Y_LIMIT = int(h * 0.80)
    lane_left, lane_right = int(w * 0.25), int(w * 0.75)
    max_w_area = 0
    detected = []

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

    # --- 2. NAVIGATION & ACCIDENT LOGIC ---
    if dist_to_turn > 0:
        dist_to_turn -= 0.5
    else:
        dist_to_turn = 0

    # --- 3. DRAWING ---
    if system_status == "NORMAL":
        lane_left, lane_right = draw_lane_overlay(frame, smoothed_risk, curr_time)
        if nav_state != "STRAIGHT":
            draw_ar_arrow(frame, lane_left, lane_right, nav_state)

    # Detection boxes
    detected.sort(key=lambda x: x["risk"], reverse=True)
    for obj in detected[:4]:
        x1, y1, x2, y2 = obj["coords"]
        draw_detection_box(frame, x1, y1, x2, y2, obj["label"], obj["col"], obj["risk"], curr_time)

    # HUD overlay
    draw_hud(frame, smoothed_risk, system_status, curr_time, frame_count)

    # --- 4. OUTPUT & CONTROLS ---
    cv2.imshow("VisionDrive Maps", generate_map_frame())
    cv2.imshow("VisionDrive AR Main", frame)
    black_box.update(frame, 0, smoothed_risk)

    prev_time = curr_time

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('b') and not airbag_deployed:
        airbag_deployed = True
        system_status = "LOCKED"
        black_box.emergency_lock()
        threading.Thread(target=trigger_emergency_call, daemon=True).start()
    elif key == ord('w'):
        nav_state = "STRAIGHT"; dist_to_turn = 200
    elif key == ord('a'):
        nav_state = "LEFT"; dist_to_turn = 200
    elif key == ord('d'):
        nav_state = "RIGHT"; dist_to_turn = 200

black_box.release()
cap.release()
cv2.destroyAllWindows()