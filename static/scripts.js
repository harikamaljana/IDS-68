function goBack(model) {
    document.querySelectorAll(".input-fields").forEach(function (el) {
        el.classList.remove("active");
    });
    document.querySelector(".model-options").classList.add("active");
    document.querySelector(".back-arrow").style.display = "none"; // Hide back arrow
    document.querySelector("h1").innerText = "Intrusion Detective System"; // Set header back to IDS
    document.querySelector(".model-options").style.display = "flex"; // Show model options
    // document.getElementById(model + "-run-button").style.display = "none"; // Hide run button
    document.querySelector("#compare-models-container").style.display =
        "none";
    document.querySelectorAll(".run-button").forEach(function (el) {
        el.style.display = "none"; // Hide run buttons for comparison models
    });
}

function showInputFields(model, column = "") {
    document.querySelectorAll(".input-fields").forEach(function (el) {
        el.classList.remove("active");
    });

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

    if (column === "") {
        // Display input fields in the main section
        document.getElementById(model + "-inputs").classList.add("active");
        document.querySelector(".back-arrow").style.display = "block"; // Show back arrow
        document.querySelector("h1").innerText = modelName; // Set model name in h1
        document.querySelector(".model-options").style.display = "none"; // Hide model options
        document.getElementById(model + "-run-button").style.display = "block"; // Show run button
    } else {
        // Display input fields in the comparison container
        document.getElementById(`model${column}-inputs`).innerHTML =
            document.getElementById(model + "-inputs").innerHTML;
        document
            .getElementById(`model${column}-inputs`)
            .classList.add("active"); // Show input fields
        document.getElementById(`run-button-model${column}`).style.display =
            "block"; // Show run button for the selected model
    }
}

function showCompareModels() {
    document.querySelectorAll(".input-fields").forEach(function (el) {
        el.classList.remove("active");
    });

    document.querySelector(".model-options").style.display = "none"; // Hide model options
    document.querySelector(".back-arrow").style.display = "block"; // Show back arrow
    document.querySelector("h1").innerText = "Compare Models"; // Update header text
    document.querySelector("#compare-models-container").style.display =
        "flex"; // Show comparison interface

    // Reset input fields for both models
    document.getElementById("model1-inputs").innerHTML = "";
    document.getElementById("model2-inputs").innerHTML = "";
}

function getData(model) {
    // Implement model running logic here
    var docu;
    // console.log("WORKING" + TrackEvent)
    switch (model) {
        case "lccde":
            docu = {
                model_name: model,
                input_list: ['verbose', 'boosting_type', 'dataset', 'learning_rate', 'random_state'],
                dataset: getElementValue(model + "-dataset"),
                verbose: getElementValue(model + "-verbose"),
                boosting_type: getElementValue(model + "-boosting"),
                learning_rate: getElementValue(model + "-learning-rate"),
                random_state: getElementValue(model + "-random-state"),
            }
            console.trace("hi" + "\tTraced");
            break;
        case "tree":
            docu = {
                model_name: model,
                input_list: ['dataset', 'random_state', 'learning_rate', 'n_estimator', 'max_feature', 'max_depth', 'min_samples_split', 'min_samples_leaf'],
                dataset: getElementValue(model + "-dataset"),
                random_state: getElementValue(model + "-random-state"),
                learning_rate: getElementValue(model + "-learning-rate"),
                n_estimator: getElementValue(model + "-n-estimator"),
                max_feature: getElementValue(model + "-max-feature"),
                max_depth: getElementValue(model + "-max-depth"),
                min_samples_split: getElementValue(model + "-min-samples-split"),
                min_samples_leaf: getElementValue(model + "-min-samples-leaf"),
            }
            break;
        case "mth":
            docu = {
                model_name: model,
                input_list: ['dataset', 'random_state', 'learning_rate', 'n_estimator', 'max_feature', 'max_depth', 'min_samples_split', 'min_samples_leaf'],
                dataset: getElementValue(model + "-dataset"),
                random_state: getElementValue(model + "-random-state"),
                learning_rate: getElementValue(model + "-learning-rate"),
                n_estimator: getElementValue(model + "-n-estimator"),
                max_feature: getElementValue(model + "-max-feature"),
                max_depth: getElementValue(model + "-max-depth"),
                min_samples_split: getElementValue(model + "-min-samples-split"),
                min_samples_leaf: getElementValue(model + "-min-samples-leaf"),
            }
            break;
        default:
            docu = { idx: 'invalid_data' };
            break;
    }
    let data = docu;
    alert("Inputs Saved to Database");
    return data;
    // saveMessages(data);
    // console.log(data); // TODO: remove after testing

}

// used by frontend.html to extract elements from form
const getElementValue = (id) => {
    return document.getElementById(id).value;
};

function storeData(model, data) {
    console.log("EXECUTED SUCCESSFULLY!!! YO MODEL NAME IS:" + JSON.stringify(data));
}

function modifyOutput(output) {
    let startIndex = output.indexOf('precision');
    let modifiedOutput = output.substring(startIndex);
    return modifiedOutput;
}