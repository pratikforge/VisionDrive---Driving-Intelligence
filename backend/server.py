from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List
import uuid
from datetime import datetime, timezone
import subprocess
import glob

# ============================================================
# 📁 PATH SETUP
# ============================================================
ROOT_DIR = Path(__file__).parent
PROJECT_ROOT = ROOT_DIR.parent

load_dotenv(ROOT_DIR / ".env")

# ============================================================
# 🧾 LOGGING
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ============================================================
# 🗄 DATABASE (Mongo)
# ============================================================
mongo_url = os.environ["MONGO_URL"]
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ["DB_NAME"]]

# ============================================================
# 🚀 FASTAPI APP
# ============================================================
app = FastAPI()
api_router = APIRouter(prefix="/api")

# ⭐ STATIC VIDEO FOLDER (THIS IS THE REAL FIX)
app.mount(
    "/blackbox",
    StaticFiles(directory=PROJECT_ROOT / "blackbox_data"),
    name="blackbox"
)

# ============================================================
# 📦 MODELS
# ============================================================
class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class StatusCheckCreate(BaseModel):
    client_name: str

# ============================================================
# 🌐 BASIC ROUTES
# ============================================================
@api_router.get("/")
async def root():
    return {"message": "Hello World"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)

    doc = status_obj.model_dump()
    doc["timestamp"] = doc["timestamp"].isoformat()

    await db.status_checks.insert_one(doc)
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find({}, {"_id": 0}).to_list(1000)

    for check in status_checks:
        if isinstance(check["timestamp"], str):
            check["timestamp"] = datetime.fromisoformat(check["timestamp"])

    return status_checks

# ============================================================
# 🚀 VISIONDRIVE ENGINE LAUNCH
# ============================================================
@api_router.post("/launch-engine")
async def launch_engine():
    try:
        visiondrive_path = PROJECT_ROOT / "visiondrive.py"

        if not visiondrive_path.exists():
            raise HTTPException(status_code=404, detail="VisionDrive engine not found")

        subprocess.Popen(
            ["python", str(visiondrive_path)],
            start_new_session=True
        )

        logger.info("VisionDrive engine launched successfully")

        return {
            "status": "success",
            "message": "VisionDrive AR engine launched."
        }

    except Exception as e:
        logger.error(f"Failed to launch VisionDrive engine: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================
# 📹 BLACKBOX VIDEO LIST API
# ============================================================
@api_router.get("/blackbox-videos")
async def get_blackbox_videos():
    try:
        blackbox_folder = PROJECT_ROOT / "blackbox_data"

        if not blackbox_folder.exists():
            return []

        video_files = glob.glob(str(blackbox_folder / "*.mp4"))
        video_files.sort(reverse=True)

        videos = []
        for video_path in video_files:
            video_file = Path(video_path)
            stat = video_file.stat()

            videos.append({
                "filename": video_file.name,
                # ⭐ IMPORTANT: static URL exposed above
                "path": f"/blackbox/{video_file.name}",
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
            })

        logger.info(f"Found {len(videos)} black box recordings")
        return videos

    except Exception as e:
        logger.error(f"Failed to retrieve black box videos: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================
# 🚨 EMERGENCY CALL LOG
# ============================================================
@api_router.post("/emergency-call")
async def log_emergency_call(payload: dict):
    """Log an emergency call event (airbag deployment → 112 dial)."""
    doc = {
        "id": str(uuid.uuid4()),
        "event": payload.get("event", "unknown"),
        "number": payload.get("number", "112"),
        "timestamp": payload.get("timestamp", datetime.now(timezone.utc).isoformat()),
        "status": "triggered"
    }
    await db.emergency_calls.insert_one(doc)
    logger.info(f"🚨 EMERGENCY CALL LOGGED: {doc}")
    return {"status": "logged", "id": doc["id"]}

# ============================================================
# 📹 LIVE DASHCAM CONTROL
# ============================================================
dashcam_process = None

@api_router.post("/launch-dashcam")
async def launch_dashcam():
    """Launch the dashcam MJPEG streaming server."""
    global dashcam_process
    try:
        # Check if already running
        if dashcam_process and dashcam_process.poll() is None:
            return {"status": "already_running", "message": "Dashcam is already streaming."}

        dashcam_path = PROJECT_ROOT / "dashcam_live.py"
        if not dashcam_path.exists():
            raise HTTPException(status_code=404, detail="dashcam_live.py not found")

        dashcam_process = subprocess.Popen(
            ["python", str(dashcam_path)],
            start_new_session=True
        )
        logger.info("📹 Dashcam streaming server launched")
        return {"status": "success", "message": "Live dashcam started. Stream will be available in a few seconds."}
    except Exception as e:
        logger.error(f"Failed to launch dashcam: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/stop-dashcam")
async def stop_dashcam():
    """Stop the dashcam streaming server."""
    global dashcam_process
    try:
        if dashcam_process and dashcam_process.poll() is None:
            dashcam_process.terminate()
            dashcam_process.wait(timeout=5)
            dashcam_process = None
            logger.info("📹 Dashcam stopped")
            return {"status": "stopped", "message": "Dashcam stream stopped."}
        else:
            dashcam_process = None
            return {"status": "not_running", "message": "Dashcam was not running."}
    except Exception as e:
        logger.error(f"Failed to stop dashcam: {str(e)}")
        # Force kill
        if dashcam_process:
            dashcam_process.kill()
            dashcam_process = None
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/dashcam-status")
async def get_dashcam_status():
    """Check if the dashcam process is running."""
    running = dashcam_process is not None and dashcam_process.poll() is None
    return {"running": running}

# ============================================================
# 🔗 REGISTER ROUTER
# ============================================================
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get("CORS_ORIGINS", "*").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()