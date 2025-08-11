const ClassifierURL = "http://127.0.0.1:8001";
let currentFeaturesDict = {};

window.addEventListener("DOMContentLoaded", () => {
    initialize();
});

async function initialize() {
    console.log("Initializing script...");
    const files = await getFilesList();
    console.log("Files fetched:", files);
    if (files && files.length > 0) {
        showFilesList(files);
    }
}

async function getFilesList() {
    console.log("Fetching files list...");

    try {
        const response = await fetch('/files_list');
        const data = await response.json();
        console.log("Files list:", data);
        return data.files_list || [];
    } catch (error) {
        console.error("Error fetching files:", error);
        return [];
    }
}

function showFilesList(files) {
    console.log("Showing files list...");
    const container = document.getElementById("select-container");

            // ננקה את התוכן הקודם
            container.innerHTML = "";
            const title = document.createElement("h3");
            title.textContent = "Select a File to Load";
            container.appendChild(title);

            // צור div פנימי לשורת select+button
            const inlineWrapper = document.createElement("div");
            inlineWrapper.style.display = "flex";
            inlineWrapper.style.alignItems = "center";
            inlineWrapper.style.gap = "10px";

            // יצירת select
            const select = document.createElement("select");
            select.id = "fileSelect";

            files.forEach(fileName => {
                const option = document.createElement("option");
                option.value = fileName;
                option.textContent = fileName;
                select.appendChild(option);
            });

            // יצירת כפתור
            const button = document.createElement("button");
            button.textContent = "Load File";
            button.className = "file-select-button";
            button.onclick = manageLoadingFlow;

            inlineWrapper.appendChild(select);
            inlineWrapper.appendChild(button);
            container.appendChild(inlineWrapper);

            // יצירת דיב להצגת ה-accuracy
            const accuracyDiv = document.createElement("div");
            accuracyDiv.id = "accuracy-container";
            accuracyDiv.style.marginTop = "10px";
            accuracyDiv.style.fontWeight = "bold";
            container.appendChild(accuracyDiv);
}

async function loadFile() {
    const select = document.getElementById("fileSelect");
    const selectedFile = select.value;

    if (!selectedFile) {
        alert("Please select a file.");
        return;
    }

    console.log("Loading file:", selectedFile);

    try {
        const response = await fetch(`/load_data/${encodeURIComponent(selectedFile)}`);
        const data = await response.json();
        console.log("File loaded:", data);
        alert(`File ${selectedFile} loaded successfully!`);
    } catch (error) {
        console.error("Error loading file:", error);
        alert(`Failed to load file ${selectedFile}.`);
    }
}

async function cleanAndTrainModel() {
    console.log("Cleaning and training model...");

    try {
        const response = await fetch('/clean_and_train_model');
        const data = await response.json();
        console.log("Model cleaned and trained:", data);
        alert("Model cleaned and trained successfully!");
        return data.accuracy;
    } catch (error) {
        console.error("Error cleaning and training model:", error);
        alert("Failed to clean and train model.");
        return null;
    }
}

async function syncModelFromMainServer() {
    console.log("Syncing model from main server...");
    try {
        const response = await fetch(`${ClassifierURL}/sync_model_from_main_server`);
        if (response.ok) {
            console.log("Model synced successfully.");
            alert("Model synced successfully!");
        } else {
            console.error("Failed to sync model:", response.statusText);
            alert("Failed to sync model from main server.");
            return;
        }
    } catch (error) {
        console.error("Error syncing model:", error);
        alert("Failed to sync model from main server.");
    }
}

async function getFeachersAndUniqeKeys() {
    console.log("Fetching features and unique keys...");

    try {
        const response = await fetch(`${ClassifierURL}/get_features_and_unique_keys`);
        const data = await response.json();
        if (data.exists) {
            console.log("Features and unique keys:", data.features_and_unique_keys);
            return data.features_and_unique_keys;
        }
        console.log("No features and unique keys found.");
    } catch (error) {
        console.error("Error fetching features and unique keys:", error);
        return null;
    }
}

function createFeatureSelects(featuresDict) {
    currentFeaturesDict = featuresDict; // שמור את המילון הגלובלי
    const container = document.getElementById('features-container');

    // ננקה קודם את התוכן הקיים
    container.innerHTML = '';
    const title = document.createElement('h3');
    title.textContent = "Select Features";
    container.appendChild(title);

    for (const [feature, options] of Object.entries(featuresDict)) {
        // צור אלמנט wrapper לכל פיצ'ר (לסדר)
        const featureDiv = document.createElement('div');
        featureDiv.classList.add('feature-select'); // אופציונלי: למחלקת CSS

        // צור label
        const label = document.createElement('label');
        label.setAttribute('for', `${feature}_id`);
        label.textContent = `${feature}: `;
        featureDiv.appendChild(label);

        // צור select
        const select = document.createElement('select');
        select.id = `${feature}_id`;
        select.name = feature;

        // הוסף אפשרויות
        for (const option of options) {
            const opt = document.createElement('option');
            opt.value = option;
            opt.textContent = option;
            select.appendChild(opt);
        }

        featureDiv.appendChild(select);
        container.appendChild(featureDiv);
    }
    const collectButton = document.createElement('button');
    collectButton.textContent = "Start Prediction";
    collectButton.onclick = managePredictionFlow;
    container.appendChild(collectButton);
}

function collectFeatureValues() {
    const result = {};

    for (const feature of Object.keys(currentFeaturesDict)) {
        const select = document.getElementById(`${feature}_id`);
        if (select) {
            result[feature] = select.value;
        } else {
            console.warn(`No select found for feature '${feature}'`);
        }
    }

    return result;
}

function showPredictionPopup(predictionText) {
    const modal = document.getElementById("predictionModal");
    const text = document.getElementById("predictionText");
    const closeBtn = document.getElementById("closeModal");

    text.innerHTML = `<strong>${predictionText}</strong>`;

    modal.style.display = "block";

    closeBtn.onclick = () => {
        modal.style.display = "none";
    };

    // גם סגירה בלחיצה מחוץ למודל
    window.onclick = (event) => {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    };
}

async function manageLoadingFlow() {
    console.log("Managing flow...");

    await loadFile();

    const accuracy = await cleanAndTrainModel();

    if (accuracy !== null) {
        console.log("Accuracy:", accuracy);
        const accuracyDiv = document.getElementById("accuracy-container");
        accuracyDiv.textContent = `Trained Model Accuracy: ${accuracy}%`;
    }
    await syncModelFromMainServer();
    const featuresAndUniqueKeys = await getFeachersAndUniqeKeys();
    createFeatureSelects(featuresAndUniqueKeys);
}

async function managePredictionFlow() {
    console.log("Managing prediction flow...");

    const featureValues = collectFeatureValues();
    console.log("Collected Feature Values for Prediction:", featureValues);

    try {
        const response = await fetch(`${ClassifierURL}/classify`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(featureValues)
        });

        if (response.ok) {
            const prediction = await response.json();
            console.log("Prediction Result:", prediction);

            // הצג את התוצאה בחלון פופאפ
            showPredictionPopup(prediction.classification);

        } else {
            console.error("Prediction failed:", response.statusText);
            alert("Prediction failed. Check console for details.");
        }
    } catch (error) {
        console.error("Error during prediction:", error);
        alert("Error during prediction. Check console for details.");
    }
}

