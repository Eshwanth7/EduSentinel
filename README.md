# 🛡️ EduSentinel

> **AI-Powered Real-Time Focus & Distraction Monitoring Platform for Students**

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green.svg)](https://opencv.org/)
[![DeepFace](https://img.shields.io/badge/DeepFace-Emotion%20AI-red.svg)](https://github.com/serengil/deepface)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange.svg)](https://tensorflow.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📌 Overview

**EduSentinel** is an intelligent, real-time desktop monitoring sentinel designed to enhance student productivity and focus during self-study sessions. By combining computer vision, audio monitoring, and active browser tab classification, EduSentinel detects digital and environmental distractions, monitors emotional engagement, and dispatches timely interventions to keep learners on track.

---

## ✨ Key Features

- **🧠 Real-Time Emotion & Engagement Engine**: Uses DeepFace and facial emotion recognition to track learner states (`focused`, `active`, `bored`, `passive`, `stressed`, `distracted`) with personalized study advice.
- **📱 Phone Detection**: Detects smartphone usage in the webcam feed using object detection to prevent social media habits during study hours.
- **📚 Intelligent Content Classification**: Analyzes active browser window titles and categorizes activity into **Educational**, **Entertainment**, or **Neutral**.
- **🎤 Ambient Noise Level Monitoring**: Tracks room sound levels (in dB) using `sounddevice` to notify users when their environment is too noisy for effective learning.
- **⏳ Smart Distraction Tracker**: Tracks continuous entertainment browsing, phone usage, or absence from the desk, triggering customizable desktop toasts and alert sounds.
- **🖥️ Modern Dark-Mode GUI**: Built with Python Tkinter, offering a sleek dashboard featuring live metrics, emotion indicators, distraction timers, and alert logs.
- **🔒 Privacy-Focused Architecture**: Operates with an *ephemeral camera pipeline*—webcam frames are processed purely in-memory and immediately destroyed without saving images to disk.

---

## 🏗️ System Architecture

```
                      +-----------------------------+
                      |      EduSentinel Core       |
                      +--------------+--------------+
                                     |
    +------------------+-------------+-------------+------------------+
    |                  |                           |                  |
+---v-----------+  +---v-----------+       +-------v-------+  +-------v-------+
|  Ephemeral    |  |    Screen     |       | Audio Monitor |  | Emotion &     |
|  Camera Feed  |  |    Monitor    |       |  (dB Meter)   |  | Phone Engine  |
+-------+-------+  +-------+-------+       +-------+-------+  +-------+-------+
        |                  |                       |                  |
        +------------------+-----------+-----------+------------------+
                                       |
                         +-------------v-------------+
                         |    Distraction Tracker    |
                         +-------------+-------------+
                                       |
                         +-------------v-------------+
                         | Alert & UI Dispatcher     |
                         | (Tkinter Dashboard)       |
                         +---------------------------+
```

---

## 📂 Project Structure

```
EduSentinel/
├── core/
│   ├── alert_dispatcher.py      # Desktop notifications & alert sounds
│   ├── audio_monitor.py         # Microphone decibel level measuring
│   ├── camera.py                # Ephemeral thread-safe webcam handling
│   ├── content_classifier.py    # Active window title classification
│   ├── distraction_tracker.py   # Distraction timers & threshold rules
│   ├── emotion_engine.py        # Facial emotion & phone detection
│   └── screen_monitor.py        # Windows active window title fetcher
├── ui/
│   └── dashboard.py             # Tkinter real-time dashboard UI
├── config.py                    # Thresholds, keywords & system settings
├── launcher.py                  # Standalone GUI launcher & warm-up controller
├── main.py                      # Core CLI/Dashboard entry point
├── requirements.txt             # Python package dependencies
├── test_all.py                  # Test suite runner
├── test_content.py              # Unit tests for content classifier
├── test_notify.py               # Unit tests for notification system
├── test_phone.py                # Unit tests for phone detector
└── test_start.py                # Unit tests for core startup logic
```

---

## ⚙️ Installation & Setup

### 1. Prerequisites
- **Python 3.9+** installed on Windows
- Web camera and microphone connected

### 2. Clone the Repository
```bash
git clone https://github.com/Eshwanth7/EduSentinel.git
cd EduSentinel
```

### 3. Create a Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run

### Option 1: Desktop Launcher (Recommended)
Launch the graphical user interface with built-in model warm-up:
```bash
python launcher.py
```

### Option 2: Core Platform
Run directly from the main script:
```bash
python main.py
```

---

## ⚙️ Configuration

Custom parameters can be tuned in `config.py`:

| Parameter | Default | Description |
| :--- | :--- | :--- |
| `DISTRACTION_THRESHOLD_SECONDS` | `120` (2 mins) | Duration of entertainment tab browsing before triggering an alert |
| `PHONE_THRESHOLD_SECONDS` | `30` | Seconds of phone detection before triggering buzzer |
| `NOISE_THRESHOLD_DB` | `65` | Ambient noise threshold (dB) for loud environment warning |
| `FRAME_INTERVAL_SECONDS` | `5` | Camera analysis polling frequency |

---

## 🧪 Running Tests

To verify component integrations and dependencies:

```bash
python test_all.py
```

Or test individual modules:
```bash
python test_content.py
python test_phone.py
python test_notify.py
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 👤 Author

**Eshwanth7**  
- GitHub: [@Eshwanth7](https://github.com/Eshwanth7)
