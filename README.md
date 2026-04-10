# 🕳️ Pothole Detection System

A deep learning project that detects potholes in road images using YOLOv8.  
Built as part of the ML & DL curriculum at Darshan University.

---

## Project Structure

```
pothole-detection/
│
├── dataset/                    # Place your dataset here
│   ├── images/
│   │   ├── train/
│   │   ├── val/
│   │   └── test/
│   └── labels/
│       ├── train/
│       ├── val/
│       └── test/
│
├── models/                     # Saved model weights after training
│
├── notebooks/
│   └── train_colab.ipynb       # Google Colab training notebook
│
├── app/
│   ├── app.py                  # Streamlit web application
│   ├── inference.py            # Detection logic
│   └── utils.py                # Logging and helper functions
│
├── training/
│   ├── train.py                # Training script (run locally)
│   └── dataset.yaml            # Dataset configuration for YOLOv8
│
├── outputs/                    # Prediction images and logs saved here
├── requirements.txt
└── README.md
```

---

## Setup (Local)

```bash
git clone https://github.com/yourusername/pothole-detection.git
cd pothole-detection
pip install -r requirements.txt
```

---

## Training (Google Colab — Recommended)

1. Open `notebooks/train_colab.ipynb` in Google Colab
2. Enable GPU: Runtime → Change Runtime Type → T4 GPU
3. Follow the cells from top to bottom
4. Download `best.pt` after training completes
5. Place it at `models/pothole_v1/weights/best.pt`

---

## Run the Web App

```bash
streamlit run app/app.py
```

Visit `http://localhost:8501` in your browser.

---

## Deploy on HuggingFace Spaces

1. Create a free account at [huggingface.co](https://huggingface.co)
2. Click **New Space** → choose **Streamlit** as SDK
3. Upload all files from the `app/` folder plus `requirements.txt`
4. Also upload your trained `best.pt` model file
5. In Space settings, make sure entry point is `app.py`
6. The app will build and go live automatically

> **Tip:** Upload `best.pt` to HuggingFace Model Hub separately and load it via URL if the file is too large.

---

## Evaluation Metrics

| Metric | Value (example) |
|--------|----------------|
| mAP50 | ~0.78 |
| Precision | ~0.81 |
| Recall | ~0.74 |
| Inference Time | ~15ms/image |

---

## Severity Grading

| Severity | Condition |
|----------|-----------|
| 🟢 Low | Box area < 1% of image |
| 🟡 Medium | Box area 1–5% of image |
| 🔴 High | Box area > 5% of image |

---

## Dataset

- **Name:** Bharat Pothole Dataset
- **Type:** Vision / Object Detection
- **Format:** YOLO (images + .txt label files)
- **Classes:** 1 (pothole)

---

*Developed by a 3rd Year CSE Student | Darshan University*
