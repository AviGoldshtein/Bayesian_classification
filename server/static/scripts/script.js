// function some() {
//     console.log("This is a message from the script.js file.");
// }

// window.addEventListener("DOMContentLoaded", () => {
//     getFilesList();
// });

// function getFilesList() {
//     console.log("Fetching files list...");

//     fetch('/files_list')
//         .then(response => response.json())
//         .then(data => {
//             console.log("Files list:", data);

//             const container = document.getElementById("select-container");

//             // ננקה את התוכן הקודם
//             container.innerHTML = "";

//             // צור div פנימי שיכיל את הסלקט והכפתור בשורה אחת
//             const inlineWrapper = document.createElement("div");
//             inlineWrapper.style.display = "flex";
//             inlineWrapper.style.alignItems = "center";
//             inlineWrapper.style.gap = "10px";

//             // יצירת select
//             const select = document.createElement("select");
//             select.id = "fileSelect";

//             (data.files_list || []).forEach(fileName => {
//                 const option = document.createElement("option");
//                 option.value = fileName;
//                 option.textContent = fileName;
//                 select.appendChild(option);
//             });

//             // יצירת כפתור
//             const button = document.createElement("button");
//             button.textContent = "Load File";
//             button.className = "file-select-button";
//             button.onclick = manageFlow;

//             // הוספה ל-inlineWrapper ול-container
//             inlineWrapper.appendChild(select);
//             inlineWrapper.appendChild(button);
//             container.appendChild(inlineWrapper);
//         })
//         .catch(error => {
//             console.error("Error fetching files:", error);
//         });
// }

// async function loadFile() {
//     const select = document.getElementById("fileSelect");
//     const selectedFile = select.value;

//     if (!selectedFile) {
//         alert("Please select a file.");
//         return;
//     }

//     console.log("Loading file:", selectedFile);

//     try {
//         const response = await fetch(`/load_data/${encodeURIComponent(selectedFile)}`);
//         const data = await response.json();
//         console.log("File loaded:", data);
//         alert(`File ${selectedFile} loaded successfully!`);
//     } catch (error) {
//         console.error("Error loading file:", error);
//         alert(`Failed to load file ${selectedFile}.`);
//     }
// }

// async function cleanAndTrainModel() {
//     console.log("Cleaning and training model...");

//     try {
//         const response = await fetch('/clean_and_train_model');
//         const data = await response.json();
//         console.log("Model cleaned and trained:", data);
//         alert("Model cleaned and trained successfully!");
//         return data.accuracy;
//     } catch (error) {
//         console.error("Error cleaning and training model:", error);
//         alert("Failed to clean and train model.");
//         return null;
//     }
// }

// async function manageFlow() {
//     console.log("Managing flow...");

//     await loadFile();

//     const accuracy = await cleanAndTrainModel();

//     if (accuracy !== null) {
//         console.log("Accuracy:", accuracy);
//         // תוכל להציג את זה גם על המסך אם תרצה
//     }
// }









function some() {
    console.log("This is a message from the script.js file.");
}

window.addEventListener("DOMContentLoaded", () => {
    getFilesList();
});

function getFilesList() {
    console.log("Fetching files list...");

    fetch('/files_list')
        .then(response => response.json())
        .then(data => {
            console.log("Files list:", data);

            const container = document.getElementById("select-container");

            // ננקה את התוכן הקודם
            container.innerHTML = "";

            // צור div פנימי לשורת select+button
            const inlineWrapper = document.createElement("div");
            inlineWrapper.style.display = "flex";
            inlineWrapper.style.alignItems = "center";
            inlineWrapper.style.gap = "10px";

            // יצירת select
            const select = document.createElement("select");
            select.id = "fileSelect";

            (data.files_list || []).forEach(fileName => {
                const option = document.createElement("option");
                option.value = fileName;
                option.textContent = fileName;
                select.appendChild(option);
            });

            // יצירת כפתור
            const button = document.createElement("button");
            button.textContent = "Load File";
            button.className = "file-select-button";
            button.onclick = manageFlow;

            inlineWrapper.appendChild(select);
            inlineWrapper.appendChild(button);
            container.appendChild(inlineWrapper);

            // יצירת דיב להצגת ה-accuracy
            const accuracyDiv = document.createElement("div");
            accuracyDiv.id = "accuracy-container";
            accuracyDiv.style.marginTop = "10px";
            accuracyDiv.style.fontWeight = "bold";
            container.appendChild(accuracyDiv);
        })
        .catch(error => {
            console.error("Error fetching files:", error);
        });
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

async function manageFlow() {
    console.log("Managing flow...");

    await loadFile();

    const accuracy = await cleanAndTrainModel();

    if (accuracy !== null) {
        console.log("Accuracy:", accuracy);
        const accuracyDiv = document.getElementById("accuracy-container");
        accuracyDiv.textContent = `Traind Model Accuracy: ${accuracy}%`;
    }
}
