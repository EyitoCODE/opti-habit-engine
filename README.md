# Opti-Habit Engine: CV-Verified Momentum Algorithm

An algorithmic continuous improvement tracking system built with Python, FastAPI, and OpenCV. This system replaces standard binary habit tracking with an Exponential Moving Average (EMA) decay model, verifying physical task completion through automated computer vision.

## Engineering Challenge

**The Problem:** Traditional continuous improvement tools rely on manual, unverified user input and fail to mathematically quantify the compounding nature of daily improvement or the decay of missed intervals. 

**The Solution:** 1. **Algorithmic State Management:** Developed a custom mathematical engine in Python utilizing an EMA decay algorithm. Tasks are assigned specific weights; consistent execution compounds the user's score, while missed days apply a rigid exponential decay penalty to the system's momentum state.
2. **Computer Vision Verification:** Engineered an optional proof-of-work module using OpenCV. Rather than clicking a checkbox, users verify physical tasks (e.g., reading a physical textbook, assembling a circuit) by presenting the object to the system camera. The system utilizes contour detection and object recognition to authenticate completion before updating the SQLite database.
3. **Lightweight API Architecture:** Designed a RESTful API using FastAPI to handle asynchronous requests between the vanilla JavaScript client-side interface and the Python processing engine, ensuring less than 200ms latency for CV verification calls.

## Technology Stack
* **Backend Engine:** Python 3.10, FastAPI, Uvicorn
* **Computer Vision:** OpenCV, NumPy
* **Database:** SQLite, SQLAlchemy (ORM)
* **Frontend:** HTML5, CSS3, JavaScript (Fetch API)

  
## Demos
![Demo](opti_habit_demo.gif)



## Installation & Deployment

```bash
# Clone repository
git clone https://github.com/EyitoCODE/opti-habit-engine.git

# Initialize virtual environment
cd opti-habit-engine/backend
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Boot the FastAPI server
uvicorn api.main:app --reload
