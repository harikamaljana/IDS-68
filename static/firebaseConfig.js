import { initializeApp } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-app.js";

// import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-analytics.js";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyA90YRqnEPXJa5NRwpxKawNR6xU1Q2bnS8",
    authDomain: "idst68.firebaseapp.com",
    databaseURL: "https://idst68-default-rtdb.firebaseio.com",
    projectId: "idst68",
    storageBucket: "idst68.appspot.com",
    messagingSenderId: "25041131733",
    appId: "1:25041131733:web:17e923d98ec0fe8cf6aa5c",
    measurementId: "G-K245LCCKFX",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
// const analytics = getAnalytics(app);

import {
    getFirestore,
    doc,
    getDoc,
    setDoc,
    collection,
    addDoc,
    updateDoc,
    deleteDoc,
    deleteField,
} from "https://www.gstatic.com/firebasejs/10.11.0/firebase-firestore.js";

const db = getFirestore();

// get references of boxes - already done when clicked on run buttons

function runModel(model) {
    // Make an AJAX request to the Flask server endpoint
    // console.log("we're in the function of " + model);
    console.trace("run model is executing the current model: " + model);
    document.getElementById(model + '-output-container').innerText = "";

    const jsonData = getData(model);
    fetch("/run-model/" + model, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(jsonData)
        // JSON.stringify({ model: 2 }), // You can pass any data needed by the Python script here
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then((data) => {
            // Handle the response from the server
            if (data.error) {
                console.error("Error:", data.error);
                alert("Error executing model");
            } else {
                console.log("Output:", data.output);
                let modifiedOutput = modifyOutput(data.output, model);
                document.getElementById(model + '-output-container').innerText = "";
                document.getElementById(model + '-output-container').innerText = modifiedOutput;
                document.getElementById(model + '-output-container').style.display = 'block'; // Display text output container
                document.getElementById(model + '-image-output-container').style.display = 'block'; // Display image output container
                alert("Model " + model + " executed successfully");

                // Display images
                displayImages(data.images, model)
            }
        })
        .catch((error) => {
            console.error(
                "There was a problem with the fetch operation:",
                error
            );
            alert("Error executing model");
            return;
        });

    // storeData(model, jsonData);

    console.log('logging json data: ' + JSON.stringify(jsonData));

    // var id = JSON.parse(jsonData.dc);
    // id["id"] = model+"."+ 'timeafterexecution'
    // .toLocaleString('en-US', {
    //     year: 'numeric',
    //     month: 'short',
    //     day: 'numeric',
    //     hour: '2-digit',
    //     minute: '2-digit',
    //     second: '2-digit',
    //     timeZoneName: 'short'
    // })

    // jsonData.dc = JSON.stringify(jsonData.dc)

    // var ref = doc(db, model, jsonData.dc['id']);
    // let docRef = await setDoc(ref, jsonData.collect)
    //     .then(() => {
    //         alert("data added successfully to " + model + " table");
    //     })
    //     .catch((error) => {
    //         alert("Unsuccessful operation, error: " + error);
    //     });
}

// async function runTree(model) {
//     // Make an AJAX request to the Flask server endpoint
//     // console.log("we're in the function of " + model);
//     console.trace("run model is executing the current model: " + model);
//     fetch("/run-Tree", {
//         method: "POST",
//         headers: {
//             "Content-Type": "application/json",
//         },
//         body: JSON.stringify(jsonData)
//         // JSON.stringify({ model: 2 }), // You can pass any data needed by the Python script here
//     })
//         .then((response) => {
//             if (!response.ok) {
//                 throw new Error("Network response was not ok");
//             }
//             return response.json();
//         })
//         .then((data) => {
//             // Handle the response from the server
//             if (data.error) {
//                 console.error("Error:", data.error);
//                 alert("Error executing model");
//             } else {
//                 console.log("Output:", data.output);
//                 let modifiedOutput = modifyOutput(data.output);
//                 document.getElementById(model + '-output-container').innerText = modifiedOutput;
//                 alert("Model " + model + " executed successfully");

//                 // Display images
//                 displayImages(data.images, model);
//             }
//         })
//         .catch((error) => {
//             console.error(
//                 "There was a problem with the fetch operation:",
//                 error
//             );
//             alert("Error executing model");
//             return;
//         });

//     storeData(model, jsonData);

//     console.log('logging json data: ' + JSON.stringify(jsonData));

//     var ref = doc(db, "Model", jsonData.dc.idx);
//     let docRef = await setDoc(ref, jsonData.collect)
//         .then(() => {
//             alert("data added successfully to model table");
//         })
//         .catch((error) => {
//             alert("Unsuccessful operation, error: " + error);
//         });

//     var ref = doc(db, "Algorithm", jsonData.dc.idx);
//     docRef = await setDoc(ref, jsonData.dc)
//         .then(() => {
//             alert("data added successfully to algorithm table");
//         })
//         .catch((error) => {
//             alert("Unsuccessful operation, error: " + error);
//         });

// }

// possbly wonky!!!!
// async function runTree(model) {
//     // Make an AJAX request to the Flask server endpoint
//     // console.log("we're in the function of " + model);
//     console.trace("run model is executing the current model: " + model);
//     fetch("/run-Tree", {
//         method: "POST",
//         headers: {
//             "Content-Type": "application/json",
//         },
//         body: JSON.stringify({ model: 2 }), // You can pass any data needed by the Python script here
//     })
//         .then((response) => {
//             if (!response.ok) {
//                 throw new Error("Network response was not ok");
//             }
//             return response.json();
//         })
//         .then((data) => {
//             // Handle the response from the server
//             if (data.error) {
//                 console.error("Error:", data.error);
//                 alert("Error executing model");
//             } else {
//                 console.log("Output:", data.output);
//                 let modifiedOutput = modifyOutput(data.output);
//                 document.getElementById(model + '-output-container').innerText = modifiedOutput;
//                 alert("Model " + model + " executed successfully");

//                 // Display images
//                 displayImages(data.images, model);
//             }
//         })
//         .catch((error) => {
//             console.error(
//                 "There was a problem with the fetch operation:",
//                 error
//             );
//             alert("Error executing model");
//             return;
//         });

//     const jsonData = getData(model);
//     storeData(model, jsonData);

//     console.log('logging json data: ' + JSON.stringify(jsonData));

//     var ref = doc(db, "Model", jsonData.dc.idx);
//     let docRef = await setDoc(ref, jsonData.collect)
//         .then(() => {
//             alert("data added successfully to model table");
//         })
//         .catch((error) => {
//             alert("Unsuccessful operation, error: " + error);
//         });

//     var ref = doc(db, "Algorithm", jsonData.dc.idx);
//     docRef = await setDoc(ref, jsonData.dc)
//         .then(() => {
//             alert("data added successfully to algorithm table");
//         })
//         .catch((error) => {
//             alert("Unsuccessful operation, error: " + error);
//         });

// }


// Fetch timestamps for a given model
function fetchTimestamps(model) {
    console.log('fetching data for ' + model)
    fetch(`/fetch-timestamps/${model}`)
        .then(response => response.json())
        .then(data => {
            const dropdown1 = document.getElementById(`${model}-dropdown-content-left`);
            const dropdown2 = document.getElementById(`${model}-dropdown-content-right`);
            dropdown1.innerHTML = ''; // Clear existing options
            dropdown2.innerHTML = ''; // Clear existing options
            const timestamps = data.timestamps;
            timestamps.forEach(timestamp => {
                // Create a new option element for each timestamp
                const left_option = document.createElement('a');
                left_option.href = '#';
                left_option.innerHTML = new Date(timestamp * 1000).toLocaleString('en-US', { timeZone: 'America/Chicago' }) + "<br>";
                left_option.classList.add('timestamp-link');
                left_option.addEventListener('click', async () => {
                    const requestId = Date.now(); // Unique identifier for this request
                    fetch('/fetch-output-data/' + model + '/' + timestamp)
                        .then(xd => {
                            if (!xd.ok) {
                                throw new Error('Network response was not ok');
                            }
                            return xd.json();
                        })
                        .then(data => {
                            var container = document.getElementById(`${model}-output-left`);
                            container.style.width = '100%';
                            container.style.height = '100vh';
                            // Handle the data or return it
                            console.log(data);
                            console.log("printing value: " + data['dataset']);

                            container.innerHTML = '';

                            var inputheader = document.createElement("h1");
                            var inputOutputString = "<b>Inputs: </b>";
                            inputheader.innerHTML = inputOutputString;
                            container.appendChild(inputheader);

                            data['input_list'].forEach(input_param => {
                                var inputoutput = document.createElement("h3");
                                var dataoutput = document.createElement("p");
                                inputoutput.innerHTML = input_param + ": ";
                                dataoutput.innerHTML = data[input_param] + "<br>";
                                container.appendChild(inputoutput);
                                container.appendChild(dataoutput);
                            });

                            var outputheader = document.createElement("h1");
                            var outputOutputString = "<b>Outputs: </b>";
                            outputheader.innerHTML = outputOutputString;
                            container.appendChild(outputheader);
                            container.scrollTop = container.scrollHeight;
                            var outputtext = document.createElement("p");
                            // outputtext.textContent = "done<?\tdone";
                            outputtext.textContent = data['output'];
                            // outputtext.style.width = outputtext.offsetWidth + 'px';
                            // outputtext.style.height = outputtext.offsetHeight + 'px';
                            container.appendChild(outputtext);

                            Object.keys(data['images']).forEach(function (fileName) {
                                var fileHeader = document.createElement("h3");
                                fileHeader.innerHTML = "fileName";

                                // Extract the base64-encoded image data
                                var imageData = data.images[fileName];

                                // Create an <img> element
                                var img = new Image();

                                // Set the src attribute to a data URL representing the PNG image data
                                img.src = 'data:image/png;base64,' + imageData;

                                // Append the image to the container
                                container.appendChild(img);
                            });

                        })

                        .catch(error => {
                            // Handle errors
                            console.error('Error fetching data:', error);
                            throw error; // Rethrow the error if necessary
                        });


                    // // console.log(document.getElementById(model+'-dropdown-content-left'))
                    // document.querySelector(`#${model}-dropdown-content-left`).style.display = "none";
                    // // document.getElementById(`#${model}-output`).style.display = "flex";
                    // var outputdata = getrunbyID(model, timestamp);
                    // console.log("output to CONSOLE" + outputdata)
                    // document.getElementById(`${model}-output`).value = outputdata;

                    // document.getElementById(`${model}-dropdown-content-left`)= 
                    // Set the selected timestamp in the input field or perform any other action
                    // Example: document.getElementById('timestamp-input').value = timestamp;
                });
                // Create a new option element for each timestamp
                const right_option = document.createElement('a');
                right_option.href = '#';
                right_option.innerHTML = new Date(timestamp * 1000).toLocaleString('en-US', { timeZone: 'America/Chicago' }) + "<br>";
                right_option.classList.add('timestamp-link');
                right_option.addEventListener('click', () => {
                    fetch('/fetch-output-data/' + model + '/' + timestamp)
                        .then(xd => {
                            if (!xd.ok) {
                                throw new Error('Network response was not ok');
                            }
                            // console.log(xd.json())
                            return xd.json();
                        })
                        .then(data => {
                            const requestId = Date.now(); // Unique identifier for this request
                            var container = document.getElementById(`${model}-output-right`);
                            container.style.width = '100%';
                            container.style.height = '100vh';
                            // Handle the data or return it
                            console.log(data);
                            console.log("printing value: " + data['dataset']);

                            container.innerHTML = '';

                            var inputheader = document.createElement("h1");
                            var inputOutputString = "<b>Inputs: </b>";
                            inputheader.innerHTML = inputOutputString;
                            container.appendChild(inputheader);

                            data['input_list'].forEach(input_param => {
                                var inputoutput = document.createElement("h3");
                                var dataoutput = document.createElement("p");
                                inputoutput.innerHTML = input_param + ": ";
                                dataoutput.innerHTML = data[input_param] + "<br>";
                                container.appendChild(inputoutput);
                                container.appendChild(dataoutput);
                            });

                            var outputheader = document.createElement("h1");
                            var outputOutputString = "<b>Outputs: </b>";
                            outputheader.innerHTML = outputOutputString;
                            container.appendChild(outputheader);
                            container.scrollTop = container.scrollHeight;
                            var outputtext = document.createElement("p");
                            outputtext.textContent = data['output'];
                            container.appendChild(outputtext);

                            Object.keys(data['images']).forEach(function (fileName) {
                                var fileHeader = document.createElement("h3");
                                fileHeader.innerHTML = "fileName";

                                // Extract the base64-encoded image data
                                var imageData = data.images[fileName];

                                // Create an <img> element
                                var img = new Image();

                                // Set the src attribute to a data URL representing the PNG image data
                                img.src = 'data:image/png;base64,' + imageData;

                                // Append the image to the container
                                container.appendChild(img);
                            });

                        })
                        .catch(error => {
                            // Handle errors
                            console.error('Error fetching data:', error);
                            throw error; // Rethrow the error if necessary
                        });

                });
                // Append the option to both dropdown menus
                dropdown1.appendChild(left_option);
                dropdown2.appendChild(right_option);
            });
        })
        .catch(error => {
            console.error('Error fetching timestamps:', error);
        });
}

// async function getrunbyID(model, option_id) {
//     var value;
//     fetch('/fetch-output-data/' + model + '/' + option_id)
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Network response was not ok');
//             }
//             console.log(response.json())
//             return response.json();
//         })
//         // .then(data => {
//         //     // Handle the data or return it
//         //     value = data;
//         //     console.log(data)
//         //     console.log("printing value: " + data)
//         //     // return data;
//         // })
//         .catch(error => {
//             // Handle errors
//             console.error('Error fetching data:', error);
//             throw error; // Rethrow the error if necessary
//         });

//     // return value;
// }

function displayImages(images, model) {
    const container = document.getElementById(model + '-image-output-container');
    container.innerHTML = ''; // Clear previous images

    for (let filename in images) {
        const imageUrl = images[filename];
        const img = document.createElement('img');
        img.src = imageUrl;
        img.alt = filename;
        container.appendChild(img);
    }
}

export { runModel, fetchTimestamps };

