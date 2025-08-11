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
│   ├── manegers/
│   │   └── maneger.py                       # Manages the full client-side workflow
│   ├── ui/
│   │   └── menu.py                          # Displays interactive menu and gets user input
│   ├── utiles/
│   │   └── http_helpers.py                  # Helpers for HTTP responses
│   ├── main.py                              # Entry point to launch the CLI app
│   ├── requirements.txt                     # Client dependencies
│   └── Dockerfile                           # Docker config for client container

├── classifier_server/                       # Classification microservice (independent API)
│   ├── app_classification/
│   │   ├── app.py                           # Initializes FastAPI app for classifier
│   │   └── classifier_endpoints.py          # Endpoints for classification logic (predict, sync, health)
│   ├── logics_classification/
│   │   ├── controller.py                    # Controller layer for classification logic
│   │   └── models/
│   │       └── classifier.py                # Loads trained model and performs classification
│   ├── requirements.txt                     # Classification server dependencies
│   ├── run_classifier_server.py             # Script to launch the classifier API server
│   └── Dockerfile                           # Docker config for classification server

├── server/                                  # Training and data-prep backend + HTML UI
│   ├── app/
│   │   ├── app.py                           # Initializes FastAPI app and serves index.html
│   │   ├── error_handler.py                 # Error handlers
│   │   └── server_endpoints.py              # Endpoints for model training, data loading, cleanup
│   ├── data/                                # Directory to store CSV files
│   ├── logics/                              # Application logic layer
│   │   ├── controller.py                    # Coordinates between endpoints and logic
│   │   ├── dal/
│   │   │   └── dal.py                       # Data access layer — loads/parses CSVs
│   │   ├── models/
│   │   │   ├── classifier.py                # Prediction helper for accuracy testing
│   │   │   └── naive_bayes.py               # Core implementation of Naive Bayes logic
│   │   ├── tests/
│   │   │   └── test.py                      # Accuracy evaluation for the trained model
│   │   └── utils/
│   │       ├── cleaner.py                   # Cleans data, handles missing values
│   │       ├── extract_keys.py              # Extracts unique values per feature
│   │       └── service.py                   # NumPy → Python conversion utilities
│   ├── requirements.txt                     # Training server dependencies
│   ├── run_server.py                        # Script to run the training API server
│   ├── static/
│   │   ├── images/
│   │   ├── scripts/
│   │   │   └── script.js
│   │   └── styles/
│   │       └── style.css
│   ├── templates/
│   │   └── index.html
│   └── Dockerfile                           # Docker config for training server

├── .gitignore                               # Git exclusions for venv, pycache, etc.
├── building_the_tocker.txt                  # Docker run commands (typo kept for filename)
└── README.md                                # Project documentation (you are here)

```

---

## ⚙️ Installation

```bash
git clone https://github.com/AviGoldshtein/Bayesian_classification.git
cd Bayesian_classification
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install per-module dependencies
pip install -r server/requirements.txt
pip install -r classifier_server/requirements.txt
pip install -r client/requirements.txt
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

## 🖥️ HTML Web UI

An interactive HTML page is bundled into the training server and served at the root path. It lets you load a CSV, train the model, sync it to the classifier server, pick feature values, and get a live prediction.

### How to use (local)
1. Start both servers as shown above:
   - Training server on `http://127.0.0.1:8000`
   - Classifier server on `http://127.0.0.1:8001`
2. Open your browser at `http://127.0.0.1:8000/`.
3. In the page:
   - Select a CSV file from the dropdown and click "Load File".
   - The page will automatically: load the file → clean and train the model → sync the trained model to the classifier server → fetch the features and their unique values.
   - Choose one value for each feature and click "Start Prediction".
   - A modal popup will show the predicted class (and the page also displays the trained model accuracy).

The page assets are served via:
- Static files: `/static/styles/style.css`, `/static/scripts/script.js`, icons under `/static/images/`
- Template: `server/templates/index.html`

The classifier server enables CORS for the training UI origin (`http://127.0.0.1:8000`, `http://localhost:8000`).

### Endpoints used by the page
- Training server (port 8000):
  - `GET /files_list` — list available CSV files in `server/data`
  - `GET /load_data/{file_name}` — load the selected CSV
  - `GET /clean_and_train_model` — clean data and train the model
  - `GET /model_metadata` — used indirectly by the classifier server for syncing
- Classifier server (port 8001):
  - `GET /sync_model_from_main_server` — pull latest model from the training server
  - `GET /get_features_and_unique_keys` — return features and their unique values
  - `POST /classify` — classify the selected feature values

Note: The target column is assumed to be the last column in the CSV.

### Docker usage
If you prefer Docker, build and run the containers as shown below (see full Docker section). Then open `http://localhost:8000` in your browser. The page will talk to the classifier server on port 8001.

```bash
# Create a shared Docker network
docker network create bayesian_network

# Run the training server (exposes 8000)
docker run -d --name baesyan_server_con --network bayesian_network -p 8000:8000 avigoldshtein/baesyan_server:v1.0

# Run the classifier server (exposes 8001)
docker run -d --name classification_server_con --network bayesian_network -p 8001:8001 classifier_server

# Open http://localhost:8000
```

### Troubleshooting
- Empty file list: ensure CSVs exist under `server/data/` and are readable by the server.
- Sync failed: verify the classifier server is running on `http://127.0.0.1:8001` and reachable from your browser.
- 500 errors during classification: make sure you trained and synced a model, and that you selected values that appear in the model features returned by the page.

---

## 📡 API Endpoints Overview

### 🧩 server_endpoints.py (Training Server)

| Method | Path                       | Description                          |
|--------|----------------------------|--------------------------------------|
| GET    | `/`                        | HTML Web UI (index.html)             |
| GET    | `/health`                  | Health check                         |
| GET    | `/files_list`              | List available CSV files             |
| GET    | `/load_data/{file_name}`   | Load selected CSV file               |
| GET    | `/deletable_columns`       | Get list of columns for removal      |
| POST   | `/drop_columns`            | Drop selected columns from dataset   |
| GET    | `/clean_and_train_model`   | Train model and return accuracy      |
| GET    | `/model_metadata`          | Return features, values, and model   |


---

### 🎯 classifier_endpoints.py (Classification Server)

| Method | Path                              | Description                                 |
|--------|-----------------------------------|---------------------------------------------|
| GET    | `/`                               | Health check                                |
| GET    | `/get_features_and_unique_keys`   | Get model features and their unique values  |
| GET    | `/sync_model_from_main_server`    | Sync model from the training server         |
| POST   | `/classify`                       | Classify given input feature values         |


---

## 🧪 Example: Train and Classify via API

```python
import requests

TRAINER = "http://127.0.0.1:8000"
CLASSIFIER = "http://127.0.0.1:8001"

# 1) List available CSVs
files = requests.get(f"{TRAINER}/files_list").json()["files_list"]
print("files:", files)

# 2) Load one CSV
file_name = files[0]
requests.get(f"{TRAINER}/load_data/{file_name}").raise_for_status()

# 3) (Optional) get deletable columns and drop some
deletable = requests.get(f"{TRAINER}/deletable_columns").json()["deletable_columns"]
print("deletable:", deletable)
# requests.post(f"{TRAINER}/drop_columns", json={"columns_to_drop": ["colA", "colB"]}).raise_for_status()

# 4) Clean + train
accuracy = requests.get(f"{TRAINER}/clean_and_train_model").json()["accuracy"]
print("accuracy:", accuracy)

# 5) Sync model to classifier server
requests.get(f"{CLASSIFIER}/sync_model_from_main_server").raise_for_status()

# 6) Get features and unique values from classifier server
features = requests.get(f"{CLASSIFIER}/get_features_and_unique_keys").json()["features_and_unique_keys"]
print("features:", features)

# 7) Classify using a dict of feature -> chosen value
#    Make sure to choose values that exist in the unique keys for each feature
example = {feature: options[0] for feature, options in features.items()}
pred = requests.post(f"{CLASSIFIER}/classify", json=example).json()
print("prediction:", pred)
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
