# 🧠 Bayesian Classification API with FastAPI

Welcome to the **Bayesian Classifier** project!  
This project lets you load a CSV, train a Naive Bayes model on it, and make predictions — all through a clean REST API built with **FastAPI**.

---

## 🚀 Features

✅ Load local CSV files  
✅ Train a Naive Bayes classifier  
✅ Make predictions via REST API  
✅ Automatic handling of missing values  
✅ Organized client-server architecture

---

## 📁 Project Structure

```
Bayesian_classification/
├── client/                            # Client-side interface (CLI-based)
│   ├── managers/
│   │   └── manager.py                # Manages client flow and communication with server
│   ├── ui/
│   │   └── menu.py                   # Handles user interaction and menu display
│   ├── utiles/
│   │   ├── cleaner.py                # Cleans data before sending to server
│   │   └── extract_keyes.py          # Utility to extract keys and lables from the DataFrame
│   └── main.py                       # Entry point for the client
├── server/                            # Server-side FastAPI application
│   ├── app/
│   │   ├── app.py                    # Initializes FastAPI app and includes routers
│   │   └── endpoints.py              # All API endpoints (routes)
│   ├── data/                         # Directory for CSV files to load and analyze
│   ├── logics/
│   │   ├── dal/
│   │   │   └── dal.py                # Data Access Layer — loads and manages raw data
│   │   ├── models/
│   │   │   ├── classifier.py         # High-level classifier wrapper
│   │   │   └── naive_bayes.py        # Core Naive Bayes algorithm logic
│   │   ├── tests/
│   │   │   └── test.py               # Basic tests for model accuracy
│   │   └── utiles/
│   │       └── servise.py            # Helper functions for model training/processing
│   └── run_server.py                 # Entry point to run the FastAPI server
└── README.md                         # Project documentation (you are here)
```

---

## ⚙️ Installation

```bash
git clone https://github.com/AviGoldshtein/Bayesian_classification.git
cd bayesian-classification
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🏁 Run the Server

```bash
uvicorn app.app:app --reload
```

Access docs at: [http://localhost:8000/](http://localhost:8000/)

---

## 🧪 API Endpoints

| Method | Path                     | Description                         |
|--------|--------------------------|-------------------------------------|
| GET    | `/`                      | Health check                        |
| GET    | `/get_files_list`        | List available CSV files            |
| GET    | `/load_data/{filename}`  | Load and return CSV as JSON         |
| POST   | `/train_model`           | Train model with JSON DataFrame     |
| POST   | `/check_accuracy`        | Check Accuracy of the trained model |

---

## 📤 Sending a DataFrame

To send a DataFrame from the client to the server:

```python
import pandas as pd
import requests

df = pd.read_csv("data.csv")

response = requests.post(
    "http://localhost:8000/train_model",
    json=df.to_dict(orient="records")
)

print(response.json())
```

---

## 🔍 Example Output

```json
{
  "sum": {
    "total_cases": 20,
    "yes": 12,
    "no": 8
  },
  "yes": {
    "humidity": {
      "high": 0.25,
      "low": 0.75
    }
  }
}
```

---

## 🧠 Model Logic

Uses **Laplace smoothing** and categorical statistics to estimate probabilities.  
Target column is assumed to be the **last column** in the DataFrame.

---

## 🤝 Contributing

Pull requests are welcome!  
For major changes, please open an issue first to discuss what you'd like to change.
