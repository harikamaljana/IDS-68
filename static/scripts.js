function goBack(model) {
    document.querySelectorAll(".input-fields").forEach(function (el) {
        el.classList.remove("active");
    });
    document.querySelector(".model-options").classList.add("active");
    document.querySelector(".back-arrow").style.display = "none"; // Hide back arrow
    document.querySelector("h1").innerText = "Intrusion Detective System"; // Set header back to IDS
    document.querySelector(".model-options").style.display = "flex"; // Show model options
    document.getElementById(model + "-run-button").style.display = "none"; // Hide run button
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
    var coll, docu;

    switch (model) {
        case "lccde":
            coll = {
                model_name: model,
                version: '1.0',
                implementation: 'code goes here',
                description: 'description here',
            };
            docu = {
                algorithm_name: getElementValue(model + "-algorithm"),
                model_name: model,
                version: '1.0',
                algo_input_list: 'JSON DATA HERE',
                algo_output_list: 'JSON DATA HERE',
                run_count: 'number goes here',
                results: 'JSON DATA HERE',
                datetime: 'datetime type goes here',
                dataset: getElementValue(model + "-dataset"),
                verbose: getElementValue(model + "-verbose"),
                boosting_type: getElementValue(model + "-boosting"),
                epochs: getElementValue(model + "-epochs"),
                idx: model + "." + getElementValue(model + "-algorithm") + "." + getElementValue(model + "-verbose"),

            }
            console.log("hi")
            break;
        case "tree":
            coll = {
                model_name: model,
                version: '1.0',
                implementation: 'code goes here',
                description: 'description here',
            };
            docu = {
                algorithm_name: getElementValue(model + "-algorithm"),
                model_name: model,
                version: '1.0',
                algo_input_list: 'JSON DATA HERE',
                algo_output_list: 'JSON DATA HERE',
                run_count: 'number goes here',
                results: 'JSON DATA HERE',
                datetime: 'datetime type goes here',
                dataset: getElementValue(model + "-dataset"),
                nestimator: getElementValue(model + "-n-estimator"),
                randomstate: getElementValue(model + "-random-state"),
                epochs: getElementValue(model + "-epochs"),
                idx: model + "." + getElementValue(model + "-algorithm") + "." + getElementValue(model + "-verbose"),
            }
            break;
        case "mth":
            coll = {
                model_name: model,
                version: '1.0',
                implementation: 'code goes here',
                description: 'description here',
            };
            docu = {
                algorithm_name: getElementValue(model + "-algorithm"),
                model_name: model,
                version: '1.0',
                algo_input_list: 'JSON DATA HERE',
                algo_output_list: 'JSON DATA HERE',
                run_count: 'number goes here',
                results: 'JSON DATA HERE',
                datetime: 'datetime type goes here',
                dataset: getElementValue(model + "-dataset"),
                randomstate: getElementValue(model + "-random-state"),
                nestimator: getElementValue(model + "-n-estimator"),
                maxfeature: getElementValue(model + "-max-feature"),
                maxdepth: getElementValue(model + "-max-depth"),
                learningrate: getElementValue(model + "-learning-rate"),
                minsamplessplit: getElementValue(model + "-min-samples-split"),
                minsamplesleaf: getElementValue(model + "-min-samples-leaf"),
                epochs: getElementValue(model + "-epochs"),
                idx: model + "." + getElementValue(model + "-algorithm") + "." + getElementValue(model + "-verbose"),
            }
            break;
        default:
            coll = { idx: 'invalid_data' };
            docu = { idx: 'invalid_data' };
            break;
    }
    let data = { collect: coll, dc: docu }
    alert("Inputs Saved to Database");
    return data;
    // saveMessages(data);
    // console.log(data); // TODO: remove after testing

}

// used by frontend.html to extract elements from form
const getElementValue = (id) => {
    return document.getElementById(id).value;
};

function storeData(model) {
    console.log("EXECUTED SUCCESSFULLY!!! YO MODEL NAME IS:" + JSON.stringify(getData(model)));
}

function modifyOutput(output) {
    let startIndex = output.indexOf('precision');
    let modifiedOutput = output.substring(startIndex);
    return modifiedOutput;
}