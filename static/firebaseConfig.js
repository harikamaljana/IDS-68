// Import the functions you need from the SDKs you need
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

async function runModel(model) {
    // Make an AJAX request to the Flask server endpoint
    fetch("/run-model", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ model: 2 }), // You can pass any data needed by the Python script here
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
                let modifiedOutput = modifyOutput(data.output);
                document.getElementById(model + '-output-container').innerText = modifiedOutput;
                document.getElementById(model + '-output-container').style.display = 'block'; // Display text output container
                document.getElementById(model + '-image-output-container').style.display = 'block'; // Display image output container
                alert("Model " + model + " executed successfully");

                // Display images
                displayImages(model, data.images);
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

    const jsonData = getData(model);
    storeData(model, jsonData);

    console.log('logging json data: ' + JSON.stringify(jsonData));

    var ref = doc(db, "Model", jsonData.dc.idx);
    let docRef = await setDoc(ref, jsonData.collect)
        .then(() => {
            alert("data added successfully to model table");
        })
        .catch((error) => {
            alert("Unsuccessful operation, error: " + error);
        });

    var ref = doc(db, "Algorithm", jsonData.dc.idx);
    docRef = await setDoc(ref, jsonData.dc)
        .then(() => {
            alert("data added successfully to algorithm table");
        })
        .catch((error) => {
            alert("Unsuccessful operation, error: " + error);
        });

}


function displayImages(model, images) {
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



export { runModel };










