# 🧠 Bayesian Classification API with FastAPI

Welcome to the **Bayesian Classification** project — a modular system for training and predicting with a Naive Bayes model over CSV files, using a clean REST API powered by **FastAPI** and a structured client-server architecture.

---

## 🚀 Features

✅ Load local CSV files  
✅ Train a Naive Bayes classifier  
✅ Make predictions via REST API  
✅ Automatic handling of missing values  
✅ Layered architecture (DAL, logic, model, utils, UI)  
✅ CLI-based interactive client  
✅ Modular API with separated endpoints (training & classification)  
✅ Docker-ready

---

## 📁 Project Structure

```
Bayesian_classification/
├── client/                                  # CLI-based user interface
│   ├── managers/
│   │   └── manager.py                       # Manages the full client-side workflow
│   ├── ui/
│   │   └── menu.py                          # Displays interactive menu and gets user input
│   ├── main.py                              # Entry point to launch the CLI app
│   └── Dockerfile                           # Docker config for client container

├── classifier_server/                       # Classification microservice (independent API)
│   ├── app_classification/
│   │   ├── app.py                           # Initializes FastAPI app for classifier
│   │   └── classifier_endpoints.py          # Endpoints for classification logic (predict, sync, health)
│   ├── logics_classification/
│   │   ├── models/
│   │   │   └── classifier.py                # Loads trained model and performs classification
│   │   └── controller.py                    # Controller layer for classification logic
│   ├── run_classifier_server.py             # Script to launch the classifier API server
│   └── Dockerfile                           # Docker config for classification server

├── server/                                  # Training and data-prep backend
│   ├── app/
│   │   ├── app.py                           # Initializes FastAPI app for training server
│   │   └── server_endpoints.py              # Endpoints for model training, data loading, cleanup
│   ├── data/                                # Directory to store CSV files
│   ├── logics/                              # Application logic layer
│   │   ├── dal/
│   │   │   └── dal.py                       # Data access layer — loads/parses CSVs
│   │   ├── models/
│   │   │   ├── classifier.py                # Stores the trained model and associated metadata
│   │   │   └── naive_bayes.py               # Core implementation of Naive Bayes logic
│   │   ├── tests/
│   │   │   └── test.py                      # Unit tests for the training and prediction pipeline
│   │   ├── utils/
│   │   │   ├── cleaner.py                   # Cleans data, handles missing values
│   │   │   ├── extract_keys.py              # Extracts unique keys for label encoding
│   │   │   └── service.py                   # Supporting service functions for training
│   │   └── controller.py                    # Coordinates between endpoints and logic
│   ├── run_server.py                        # Script to run the training API server
│   └── Dockerfile                           # Docker config for training server

├── requirements.txt                         # Shared Python dependencies for all components
├── .gitignore                               # Git exclusions for venv, pycache, etc.
├── building_the_tocker.txt                  # Notes or script for building Docker images (typo?)
└── README.md                                # Project documentation (you are here)

```

---

## ⚙️ Installation

```bash
git clone https://github.com/AviGoldshtein/Bayesian_classification.git
cd Bayesian_classification
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🏁 Run the Servers

### Main training server:

```bash
cd server
python run_server.py
```

### Classifier server:

```bash
cd classifier_server
python run_classifier_server.py
```

### Client side:

```bash
cd client
python main.py
```

---

## 📡 API Endpoints Overview

### 🧩 server_endpoints.py (Training Server)

| Method | Path                        | Description                          |
|--------|-----------------------------|--------------------------------------|
| GET    | `/`                         | Health check                         |
| GET    | `/get_files_list`           | List available CSV files             |
| GET    | `/load_data/{chosen_file}`  | Load selected CSV file               |
| GET    | `/get_columns_list`         | Get list of columns for removal      |
| POST   | `/drop_requested_columns`   | Drop selected columns from dataset   |
| GET    | `/clean_and_train_model`    | Train model and return accuracy      |
| GET    | `/get_model_metadata`       | Return features, values, and model   |


---

### 🎯 classifier_endpoints.py (Classification Server)

| Method | Path                              | Description                                 |
|--------|-----------------------------------|---------------------------------------------|
| GET    | `/`                               | Health check                                |
| GET    | `/get_features_and_unique_keys`   | Get model features and their unique values  |
| GET    | `/sync_model_from_main_server`    | Sync model from the training server         |
| POST   | `/classify`                       | Classify given input feature values         |


---

## 🧪 Sending a DataFrame

```python
import pandas as pd
import requests

df = pd.read_csv("data.csv")

response = requests.post(
    "http://127.0.0.1:8000/train_model",
    json=df.to_dict(orient="records")
)

print(response.json())
```

---

## 🧠 Model Logic

Custom Naive Bayes implementation using categorical probability and Laplace smoothing.  
The target column is assumed to be the **last column** in the DataFrame.

---

## 📤 Example Output

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

## 🐳 Docker

Each server module has its own Dockerfile.

```bash
# Build the main training server image
cd server
docker build -t avigoldshtein/baesyan_server:v1.0 .

# Build the classification server image
cd classifier_server
docker build -t classifier_server .

# Build the client image
cd client
docker build -t avigoldshtein/baesyan_client:v1.0 .

```
```bash
# Create a shared Docker network
docker network create bayesian_network

# Run the training server
docker run -d \
  --name baesyan_server_con \
  --network bayesian_network \
  -p 8000:8000 \
  avigoldshtein/baesyan_server:v1.0

# Run the classification server
docker run -d \
  --name classification_server_con \
  --network bayesian_network \
  -p 8001:8001 \
  classifier_server

# Run the CLI client interactively
docker run -it \
  --name baesyan_client \
  --network bayesian_network \
  avigoldshtein/baesyan_client:v1.0

```

---

## 🤝 Contributing

Pull requests are welcome.  
For major changes, please open an issue first to discuss your ideas.
