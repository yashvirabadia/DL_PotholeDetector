import streamlit as st
import os
import sys
import tempfile
from PIL import Image

sys.path.append(os.path.dirname(__file__))
from inference import load_model, detect_potholes
from utils import log_prediction, get_severity_summary

st.set_page_config(
    page_title="RoadScan AI — Pothole Detection",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🛣️"
)

# ── Theme state ───────────────────────────────────────────────────────────────
# if "dark_mode" not in st.session_state:
#     st.session_state.dark_mode = False  # default: light

# ── Theme tokens ──────────────────────────────────────────────────────────────
def get_theme():
    return {
        "bg":          "#0D0F14",
        "surface":     "#161A24",
        "surface2":    "#1E2336",
        "border":      "#2A3050",
        "text":        "#E8EAF0",
        "text_muted":  "#8892AA",
        "accent":      "#4F8EF7",
        "success":     "#22C97A",
        "warning":     "#F5A623",
        "danger":      "#F25C5C",
        "sidebar_bg":  "#0F1219",
        "card_shadow": "0 2px 12px rgba(0,0,0,0.4)",
    }

t = get_theme()

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after {{ box-sizing: border-box; }}

.stApp {{
    background: {t["bg"]} !important;
    font-family: 'Inter', sans-serif;
    color: {t["text"]};
}}
.main .block-container {{
    padding: 2rem 2.5rem 3rem;
    max-width: 1100px;
}}
[data-testid="stSidebar"] {{
    background: {t["sidebar_bg"]} !important;
    border-right: 1px solid {t["border"]};

    min-width: 260px !important;
    max-width: 260px !important;
    width: 260px !important;
}}


[data-testid="stSidebar"] .block-container {{
    padding: 1.2rem 1rem;
}}
#MainMenu {{ visibility: hidden; }}
footer {{ visibility: hidden; }}
[data-testid="stDecoration"] {{ display: none; }}

h1, h2, h3, h4 {{ color: {t["text"]}; font-family: 'Inter', sans-serif; }}

.logo-wrap {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0.4rem 0 1.2rem;
    border-bottom: 1px solid {t["border"]};
    margin-bottom: 1rem;
}}
.logo-icon {{
    width: 34px;
    height: 34px;
    background: {t["accent"]};
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
    color: white;
    font-weight: 700;
    font-family: 'Inter', sans-serif;
}}
.logo-name {{
    font-size: 1.05rem;
    font-weight: 700;
    color: {t["text"]};
    line-height: 1.15;
}}
.logo-sub {{
    font-size: 0.65rem;
    color: {t["text_muted"]};
    text-transform: uppercase;
    letter-spacing: 0.08em;
}}



.nav-label {{
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: {t["text_muted"]};
    padding: 0.5rem 0.2rem 0.3rem;
}}

.info-chip {{
    background: {t["surface"]};
    border: 1px solid {t["border"]};
    border-radius: 7px;
    padding: 0.4rem 0.75rem;
    margin-bottom: 0.3rem;
    font-size: 0.78rem;
    color: {t["text_muted"]};
}}
.info-chip strong {{ color: {t["text"]}; font-weight: 600; }}

.divider {{
    height: 1px;
    background: {t["border"]};
    margin: 1rem 0;
    border: none;
}}

.page-eyebrow {{
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: {t["accent"]};
    margin-bottom: 0.25rem;
}}
.page-title {{
    font-size: 1.9rem;
    font-weight: 700;
    color: {t["text"]};
    margin-bottom: 0.3rem;
    line-height: 1.15;
}}
.page-sub {{
    color: {t["text_muted"]};
    font-size: 0.88rem;
    margin-bottom: 1.4rem;
}}

.stat-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin: 1.4rem 0;
}}
.stat-card {{
    background: {t["surface"]};
    border: 1px solid {t["border"]};
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    box-shadow: {t["card_shadow"]};
    border-left: 3px solid {t["accent"]};
}}
.stat-value {{
    font-size: 1.55rem;
    font-weight: 700;
    color: {t["accent"]};
    margin-bottom: 0.2rem;
}}
.stat-label {{
    font-size: 0.78rem;
    color: {t["text_muted"]};
    line-height: 1.4;
}}

.steps-grid {{
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 0.75rem;
    margin: 1.2rem 0;
}}
.step-card {{
    background: {t["surface"]};
    border: 1px solid {t["border"]};
    border-radius: 10px;
    padding: 1rem 0.8rem;
    text-align: center;
    box-shadow: {t["card_shadow"]};
}}
.step-num {{
    width: 26px;
    height: 26px;
    background: {t["accent"]};
    border-radius: 50%;
    color: white;
    font-size: 0.72rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 0.6rem;
}}
.step-text {{ font-size: 0.76rem; color: {t["text_muted"]}; line-height: 1.45; }}

.section-title {{
    font-size: 1rem;
    font-weight: 700;
    color: {t["text"]};
    margin-bottom: 0.8rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid {t["border"]};
}}

.img-label {{
    font-size: 0.73rem;
    font-weight: 600;
    color: {t["text_muted"]};
    text-transform: uppercase;
    letter-spacing: 0.08em;
    background: {t["surface2"]};
    border: 1px solid {t["border"]};
    border-bottom: none;
    border-radius: 8px 8px 0 0;
    padding: 0.45rem 0.9rem;
}}

.metric-row {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.75rem;
    margin: 1.2rem 0;
}}
.metric-card {{
    background: {t["surface"]};
    border: 1px solid {t["border"]};
    border-radius: 10px;
    padding: 1rem 1.2rem;
    text-align: center;
    box-shadow: {t["card_shadow"]};
}}
.metric-num {{
    font-size: 1.75rem;
    font-weight: 700;
    color: {t["accent"]};
    line-height: 1;
}}
.metric-lab {{
    font-size: 0.72rem;
    color: {t["text_muted"]};
    margin-top: 0.25rem;
    font-weight: 500;
}}
.metric-card.danger  .metric-num {{ color: {t["danger"]}; }}
.metric-card.warning .metric-num {{ color: {t["warning"]}; }}
.metric-card.success .metric-num {{ color: {t["success"]}; }}

.det-table {{
    width: 100%;
    border-collapse: collapse;
    background: {t["surface"]};
    border: 1px solid {t["border"]};
    border-radius: 10px;
    overflow: hidden;
    box-shadow: {t["card_shadow"]};
    margin-top: 1rem;
    font-size: 0.83rem;
}}
.det-table th {{
    background: {t["surface2"]};
    color: {t["text_muted"]};
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.65rem 1rem;
    text-align: left;
    border-bottom: 1px solid {t["border"]};
}}
.det-table td {{
    padding: 0.65rem 1rem;
    border-bottom: 1px solid {t["border"]};
    color: {t["text"]};
    vertical-align: middle;
}}
.det-table tr:last-child td {{ border-bottom: none; }}
.det-table tr:hover td {{ background: {t["surface2"]}; }}
.mono {{ font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: {t["text_muted"]}; }}
.badge {{
    display: inline-block;
    padding: 0.18rem 0.55rem;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 600;
}}
.badge-low     {{ background: {t["success"]}22; color: {t["success"]}; }}
.badge-medium  {{ background: {t["warning"]}22; color: {t["warning"]}; }}
.badge-high    {{ background: {t["danger"]}22;  color: {t["danger"]}; }}

.tech-table {{
    background: {t["surface"]};
    border: 1px solid {t["border"]};
    border-radius: 10px;
    overflow: hidden;
    box-shadow: {t["card_shadow"]};
}}
.tech-row {{
    display: flex;
    justify-content: space-between;
    padding: 0.75rem 1.2rem;
    border-bottom: 1px solid {t["border"]};
    font-size: 0.85rem;
    align-items: center;
}}
.tech-row:last-child {{ border-bottom: none; }}
.tech-key {{ color: {t["text_muted"]}; font-weight: 500; }}
.tech-val {{
    font-weight: 600;
    color: {t["text"]};
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    background: {t["surface2"]};
    padding: 0.18rem 0.55rem;
    border-radius: 5px;
}}

.sev-item {{
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.78rem;
    color: {t["text_muted"]};
    padding: 0.4rem 0.6rem;
    background: {t["surface"]};
    border-radius: 6px;
    border: 1px solid {t["border"]};
    margin-bottom: 0.3rem;
}}
.sev-dot {{ width: 9px; height: 9px; border-radius: 50%; flex-shrink: 0; }}

.upload-area {{
    background: {t["surface"]};
    border: 2px dashed {t["border"]};
    border-radius: 12px;
    padding: 3rem 2rem;
    text-align: center;
    margin-top: 0.5rem;
}}
.upload-title {{ font-size: 1rem; font-weight: 600; color: {t["text"]}; margin-bottom: 0.3rem; }}
.upload-sub {{ font-size: 0.83rem; color: {t["text_muted"]}; }}

.obj-list {{
    background: {t["surface"]};
    border: 1px solid {t["border"]};
    border-radius: 10px;
    overflow: hidden;
    box-shadow: {t["card_shadow"]};
}}
.obj-item {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0.65rem 1.2rem;
    border-bottom: 1px solid {t["border"]};
    font-size: 0.82rem;
    color: {t["text_muted"]};
}}
.obj-item:last-child {{ border-bottom: none; }}
.obj-num {{
    font-weight: 700;
    color: {t["accent"]};
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    min-width: 20px;
}}

[data-testid="stSlider"] label {{ color: {t["text"]} !important; font-size: 0.82rem !important; font-weight: 600 !important; }}
[data-testid="stSlider"] p {{ color: {t["text"]} !important; }}
.stRadio label {{ color: {t["text"]} !important; font-size: 0.85rem !important; }}
.stButton > button {{
    background: {t["accent"]} !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.2rem !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
}}
</style>

""", unsafe_allow_html=True)


MODEL_PATH = os.path.join(os.path.dirname(__file__), "Pothole_v1", "weights", "best1.pt")

@st.cache_resource
def get_model():
    if not os.path.exists(MODEL_PATH):
        st.error(f"Model not found at `{MODEL_PATH}`. Please train the model first.")
        st.stop()
    return load_model(MODEL_PATH)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""<div class="logo-wrap">
<div class="logo-icon">R</div>
<div>
<div class="logo-name">RoadScan AI</div>
<div class="logo-sub">Pothole Detection</div>
</div>
</div>""", unsafe_allow_html=True)



    st.markdown('<div class="nav-label">Navigation</div>', unsafe_allow_html=True)
    selected = st.radio("nav", ["Home", "Detect Potholes", "About Project"], label_visibility="collapsed")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Detection settings — always visible in sidebar
    st.markdown('<div class="nav-label">Detection Settings</div>', unsafe_allow_html=True)
    conf_thresh = st.slider("Confidence Threshold", 0.1, 0.9, 0.4, 0.05)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="nav-label">Severity Guide</div>', unsafe_allow_html=True)
    st.markdown(f"""<div class="sev-item">
<div class="sev-dot" style="background:{t['success']}"></div>
<span><strong style="color:{t['text']}">Low</strong> — box &lt; 1% of image</span>
</div>
<div class="sev-item">
<div class="sev-dot" style="background:{t['warning']}"></div>
<span><strong style="color:{t['text']}">Medium</strong> — 1% to 5%</span>
</div>
<div class="sev-item">
<div class="sev-dot" style="background:{t['danger']}"></div>
<span><strong style="color:{t['text']}">High</strong> — area &gt; 5%</span>
</div>""", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="nav-label">System Info</div>', unsafe_allow_html=True)
    st.markdown(f"""<div class="info-chip"><strong>Model:</strong>&nbsp; YOLOv8s</div>
<div class="info-chip"><strong>Dataset:</strong>&nbsp; Bharat Pothole</div>
<div class="info-chip"><strong>Framework:</strong>&nbsp; PyTorch</div>""", unsafe_allow_html=True)


# ── Pages ─────────────────────────────────────────────────────────────────────

def home_page():
    st.markdown(f"""<div class="page-eyebrow">AI-Powered Road Safety</div>
<div class="page-title">Pothole Detection System</div>
<div class="page-sub">Upload a road image and let YOLOv8 detect, classify, and score every pothole instantly.</div>""",
        unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown(f"""<div class="stat-grid">
<div class="stat-card">
<div class="stat-value">YOLOv8</div>
<div class="stat-label">State-of-the-art real-time object detection model</div>
</div>
<div class="stat-card">
<div class="stat-value">Real-time</div>
<div class="stat-label">Near-instant inference on standard hardware</div>
</div>
<div class="stat-card">
<div class="stat-value">3-Level</div>
<div class="stat-label">Low / Medium / High severity grading per detection</div>
</div>
</div>""", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">How It Works</div>', unsafe_allow_html=True)

    st.markdown(f"""<div class="steps-grid">
<div class="step-card"><div class="step-num">1</div><div class="step-text">Upload a road image on the Detect page</div></div>
<div class="step-card"><div class="step-num">2</div><div class="step-text">YOLOv8 processes the image in real-time</div></div>
<div class="step-card"><div class="step-num">3</div><div class="step-text">Detected potholes are marked with bounding boxes</div></div>
<div class="step-card"><div class="step-num">4</div><div class="step-text">Severity is estimated from box-to-image ratio</div></div>
<div class="step-card"><div class="step-num">5</div><div class="step-text">Results are automatically logged for records</div></div>
</div>""", unsafe_allow_html=True)


def detect_page():
    st.markdown(f"""<div class="page-eyebrow">Detection Engine</div>
<div class="page-title">Detect Potholes</div>
<div class="page-sub">Upload a road image and get instant AI-powered pothole analysis.</div>""",
        unsafe_allow_html=True)

    model = get_model()
    uploaded = st.file_uploader("Choose a road image", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

    if not uploaded:
        st.markdown(f"""<div class="upload-area">
<div style="font-size:2rem;margin-bottom:0.7rem">📷</div>
<div class="upload-title">Drop your road image here</div>
<div class="upload-sub">Supports JPG, JPEG, PNG &nbsp;·&nbsp; Drag and drop or click to browse</div>
</div>""", unsafe_allow_html=True)
        return

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.markdown('<div class="img-label">Original Image</div>', unsafe_allow_html=True)
        original = Image.open(uploaded)
        st.image(original, use_container_width=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(uploaded.getvalue())
        tmp_path = tmp.name

    with st.spinner("Scanning for potholes..."):
        detections, result_path = detect_potholes(model, tmp_path, conf=conf_thresh)
        log_prediction(uploaded.name, len(detections), detections)

    with col2:
        st.markdown('<div class="img-label">Detection Result</div>', unsafe_allow_html=True)
        result_img = Image.open(result_path)
        st.image(result_img, use_container_width=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Detection Summary</div>', unsafe_allow_html=True)

    summary  = get_severity_summary(detections)
    avg_conf = round(sum(d["confidence"] for d in detections) / len(detections), 3) if detections else 0

    st.markdown(f"""<div class="metric-row">
<div class="metric-card"><div class="metric-num">{len(detections)}</div><div class="metric-lab">Potholes Found</div></div>
<div class="metric-card"><div class="metric-num">{avg_conf}</div><div class="metric-lab">Avg Confidence</div></div>
<div class="metric-card danger"><div class="metric-num">{summary['High']}</div><div class="metric-lab">High Severity</div></div>
<div class="metric-card success"><div class="metric-num">{summary['Low'] + summary['Medium']}</div><div class="metric-lab">Low + Medium</div></div>
</div>""", unsafe_allow_html=True)

    if detections:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Per-Detection Details</div>', unsafe_allow_html=True)

        # Build rows — must NOT have leading whitespace (avoids Markdown code-block bug)
        rows = ""
        for i, d in enumerate(detections, 1):
            sev = d["severity"]
            badge_cls = {"Low": "badge-low", "Medium": "badge-medium", "High": "badge-high"}[sev]
            x1, y1, x2, y2 = d["bbox"]
            rows += (
                f'<tr>'
                f'<td class="mono">#{i}</td>'
                f'<td class="mono">{d["confidence"]}</td>'
                f'<td><span class="badge {badge_cls}">{sev}</span></td>'
                f'<td class="mono">{d["area"]:,} px\u00b2</td>'
                f'<td class="mono">{x1},{y1} \u2192 {x2},{y2}</td>'
                f'</tr>'
            )

        st.markdown(
            '<table class="det-table">'
            '<thead><tr>'
            '<th>#</th><th>Confidence</th><th>Severity</th><th>Area</th><th>Bounding Box</th>'
            '</tr></thead>'
            f'<tbody>{rows}</tbody>'
            '</table>',
            unsafe_allow_html=True
        )

    os.unlink(tmp_path)


def about_page():
    st.markdown(f"""<div class="page-eyebrow">Documentation</div>
<div class="page-title">About This Project</div>
<div class="page-sub">Built at Darshan University as part of the ML &amp; DL curriculum — using YOLOv8 for automated road damage detection.</div>""",
        unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown('<div class="section-title">Tech Stack</div>', unsafe_allow_html=True)
        st.markdown(f"""<div class="tech-table">
<div class="tech-row"><span class="tech-key">Detection Model</span><span class="tech-val">YOLOv8s</span></div>
<div class="tech-row"><span class="tech-key">Framework</span><span class="tech-val">PyTorch</span></div>
<div class="tech-row"><span class="tech-key">Frontend</span><span class="tech-val">Streamlit</span></div>
<div class="tech-row"><span class="tech-key">Image Processing</span><span class="tech-val">OpenCV + PIL</span></div>
<div class="tech-row"><span class="tech-key">Dataset</span><span class="tech-val">Bharat Pothole</span></div>
</div>""", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-title">Project Objectives</div>', unsafe_allow_html=True)
        objectives = [
            ("1", "Problem Definition & Dataset Acquisition"),
            ("2", "Data Preprocessing & Augmentation"),
            ("3", "Model Architecture Design & Training"),
            ("4", "Evaluation & Hyperparameter Tuning"),
            ("5", "Application Interface (Frontend)"),
            ("6", "Transfer Learning with YOLOv8"),
            ("7", "Backend Integration & Deployment"),
        ]
        items_html = "".join(
            f'<div class="obj-item"><span class="obj-num">{n}.</span>{txt}</div>'
            for n, txt in objectives
        )
        st.markdown(f'<div class="obj-list">{items_html}</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Severity Estimation Logic</div>', unsafe_allow_html=True)
    st.markdown(f"""<div class="metric-row">
<div class="metric-card success"><div class="metric-num">&lt;1%</div><div class="metric-lab">Low Severity</div></div>
<div class="metric-card warning"><div class="metric-num">1-5%</div><div class="metric-lab">Medium Severity</div></div>
<div class="metric-card danger"><div class="metric-num">&gt;5%</div><div class="metric-lab">High Severity</div></div>
<div class="metric-card"><div class="metric-num">px2</div><div class="metric-lab">Relative to Image Area</div></div>
</div>""", unsafe_allow_html=True)


# ── Route ─────────────────────────────────────────────────────────────────────
if selected == "Home":
    home_page()
elif selected == "Detect Potholes":
    detect_page()
elif selected == "About Project":
    about_page()
