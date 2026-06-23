import streamlit as st
import json
import math
import requests
import time
import os
import tempfile
from datetime import datetime
import streamlit.components.v1 as components
from groq import Groq
import re
import pytz

# ========== OPTIONAL: Object detection from uploaded images ==========
def run_object_detection(image_bytes):
    try:
        from ultralytics import YOLO
        import cv2
        model = YOLO("yolov8n.pt")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(image_bytes)
            tmp_path = tmp.name
        results = model(tmp_path)
        os.unlink(tmp_path)
        img = cv2.imread(tmp_path)
        if img is None:
            return None, [{"error": "Could not read image"}]
        detections = []
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                    conf = float(box.conf[0])
                    cls_id = int(box.cls[0])
                    label = model.names[cls_id]
                    detections.append({"label": label, "confidence": f"{conf:.2f}", "bbox": (x1, y1, x2, y2)})
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(img, f"{label} {conf:.2f}", (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img_rgb, detections
    except ImportError as e:
        return None, [{"error": f"Missing dependencies: {e}"}]
    except Exception as e:
        return None, [{"error": str(e)}]

# ========== CONFIGURATION ==========
st.set_page_config(
    page_title="GlobalInternet.py | Surveillance Portal",
    layout="wide",
    page_icon="🌐"
)

# ========== CUSTOM CSS – LEOPARD BLACK THEME ==========
st.markdown("""
<style>
    .stApp {
        background: #0a0a0f;
        background-image: 
            radial-gradient(circle at 20% 30%, rgba(60, 40, 20, 0.15) 0%, transparent 25%),
            radial-gradient(circle at 70% 60%, rgba(60, 40, 20, 0.10) 0%, transparent 35%),
            radial-gradient(circle at 40% 80%, rgba(80, 50, 25, 0.12) 0%, transparent 30%),
            radial-gradient(circle at 85% 20%, rgba(40, 30, 15, 0.08) 0%, transparent 40%);
        color: #e0d5c8;
    }
    [data-testid="stSidebar"] {
        background: #0d0d12;
        background-image: 
            radial-gradient(circle at 30% 40%, rgba(70, 50, 30, 0.12) 0%, transparent 30%),
            radial-gradient(circle at 70% 70%, rgba(50, 35, 20, 0.08) 0%, transparent 35%);
        border-right: 1px solid #2a1f14;
    }
    .stButton>button {
        background: linear-gradient(135deg, #1a120a, #2a1f14) !important;
        color: #e8ddd0 !important;
        border:
