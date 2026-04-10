#Pothole Detection System

A deep learning project that detects potholes in road images using YOLOv8.  
Built as part of the ML & DL curriculum at Darshan University.


---

## Training (use Google Colab(Recommended) or Kaggle(for more GPU hours) )

1. Enable GPU: Runtime → Change Runtime Type → T4 GPU
2. Follow the cells from top to bottom
3. Download `best.pt` after training completes

---

## Run the Web App

```bash
streamlit run app/app.py
```

Visit `http://localhost:8501` in your browser.

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


