function showInputFields(model) {
    document.querySelectorAll(".input-fields").forEach(function (el) {
        el.classList.remove("active");
    });
    document.getElementById(model + "-inputs").classList.add("active");
    document.querySelector(".back-arrow").style.display = "block"; // Show back arrow
    let modelName = "";
    switch (model) {
        case "lccde":
            modelName = "LCCDE Model";
            break;
        case "tree":
            modelName = "Tree Based Model";
            break;
        case "mth":
            modelName = "MTH Model";
            break;
        default:
            modelName = "";
    }
    document.querySelector("h1").innerText = modelName; // Set model name in h1
    document.querySelector("h1").style.display = "block"; // Show IDS
    document.querySelector(".model-options").style.display = "none"; // Hide model options
    document.getElementById(model + "-run-button").style.display = "block"; // Show run button
}

function goBack() {
    document.querySelectorAll(".input-fields").forEach(function (el) {
        el.classList.remove("active");
    });
    document.querySelector(".model-options").classList.add("active");
    document.querySelector(".back-arrow").style.display = "none"; // Hide back arrow
    document.querySelector("h1").innerText = "Intrusion Detective System"; // Set header back to IDS
    document.querySelector("h1").style.display = "block"; // Show IDS
    document.querySelector(".model-options").style.display = "flex"; // Show model options
    // document.getElementsByClassName("run-button").style.display = "none"; // Hide run button
}

function runModel(model) {
    // Implement model running logic here
    var data;
    switch (model) {
        case "lccde":
            data = {
                algorithm: getElementValue(model + "-algorithm"),
                dataset: getElementValue(model + "-dataset"),
                verbose: getElementValue(model + "-verbose"),
                boosting_type: getElementValue(model + "-boosting"),
                epochs: getElementValue(model + "-epochs"),
            };
            break;
        case "tree":
            data = {
                algorithm: getElementValue(model + "-algorithm"),
                dataset: getElementValue(model + "-dataset"),
                nestimator: getElementValue(model + "-n-estimator"),
                randomstate: getElementValue(model + "-random-state"),
                epochs: getElementValue(model + "-epochs"),
            };
            break;
        case "mth":
            data = {
                algorithm: getElementValue(model + "-algorithm"),
                dataset: getElementValue(model + "-dataset"),
                randomstate: getElementValue(model + "-random-state"),
                nestimator: getElementValue(model + "-n-estimator"),
                maxfeature: getElementValue(model + "-max-feature"),
                maxdepth: getElementValue(model + "-max-depth"),
                learningrate: getElementValue(model + "-learning-rate"),
                minsamplessplit: getElementValue(model + "-min-samples-split"),
                minsamplesleaf: getElementValue(model + "-min-samples-leaf"),
                epochs: getElementValue(model + "-epochs"),
            };
            break;
    }

    console.log(data); // TODO: remove after testing
    // alert("Model is running!");
}

// used by frontend.html to extract elements from form
const getElementValue = (id) => {
    return document.getElementById(id).value;
};