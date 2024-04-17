// // const firebaseConfig = {
// //     apiKey: "AIzaSyA90YRqnEPXJa5NRwpxKawNR6xU1Q2bnS8",
// //     authDomain: "idst68.firebaseapp.com",
// //     databaseURL: "https://idst68-default-rtdb.firebaseio.com",
// //     projectId: "idst68",
// //     storageBucket: "idst68.appspot.com",
// //     messagingSenderId: "25041131733",
// //     appId: "1:25041131733:web:17e923d98ec0fe8cf6aa5c",
// //     measurementId: "G-K245LCCKFX"
// // };

// // // initialize firebase
// // firebase.initializeApp(firebaseConfig);

// // // reference db
// // var dbReference = firebase.database().ref('idst68');

// // const saveMessages = (data) => {
// //     var dataSend = dbReference.push();
// //     dataSend.set(data);
// // }

// import { getData } from "./scripts";
// // Import the functions you need from the SDKs you need
// import { initializeApp } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-app.js";
// // import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-analytics.js";
// // TODO: Add SDKs for Firebase products that you want to use
// // https://firebase.google.com/docs/web/setup#available-libraries

// // Your web app's Firebase configuration
// // For Firebase JS SDK v7.20.0 and later, measurementId is optional
// const firebaseConfig = {
//     apiKey: "AIzaSyA90YRqnEPXJa5NRwpxKawNR6xU1Q2bnS8",
//     authDomain: "idst68.firebaseapp.com",
//     databaseURL: "https://idst68-default-rtdb.firebaseio.com",
//     projectId: "idst68",
//     storageBucket: "idst68.appspot.com",
//     messagingSenderId: "25041131733",
//     appId: "1:25041131733:web:17e923d98ec0fe8cf6aa5c",
//     measurementId: "G-K245LCCKFX",
// };

// // Initialize Firebase
// const app = initializeApp(firebaseConfig);
// // const analytics = getAnalytics(app);

// import {
//     getFirestore,
//     doc,
//     getDoc,
//     setDoc,
//     collection,
//     addDoc,
//     updateDoc,
//     deleteDoc,
//     deleteField,
// } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-firestore.js";

// const db = getFirestore();


// // get references of boxes - already done when clicked on run buttons

// async function AddDocument_AutoID() {
//     var ref = collection(db, "TheStudentsList");
//     const docRef = await addDoc(ref, getData('lccde')).then(() => {
//         alert('data added successfully');
//     }).catch((error) => {
//         alert('Unsuccessful operation, error: ' + error);
//     });
// }



// async function runModel(model) {
//     console.log("run model is executing the current model: " + model);
// }

// // TRASH

// // async function AddDocument_AutoID() {
// //     var ref = collection(db, "TheStudentsList");
// //     const docRef = await addDoc(ref, getData('lccde')).then(() => {
// //         alert('data added successfully');
// //     }).catch((error) => {
// //         alert('Unsuccessful operation, error: ' + error);
// //     });
// // }

// // async function runModel(model) {

// //     // Make an AJAX request to the Flask server endpoint
// //     console.log("we're in the function of " + model);
// //     fetch("/run-model", {
// //         method: "POST",
// //         headers: {
// //             "Content-Type": "application/json",
// //         },
// //         body: JSON.stringify({ model: 2 }), // You can pass any data needed by the Python script here
// //     })
// //         .then((response) => {
// //             if (!response.ok) {
// //                 throw new Error("Network response was not ok");
// //             }
// //             return response.json();
// //         })
// //         .then((data) => {
// //             // Handle the response from the server
// //             if (data.error) {
// //                 console.error("Error:", data.error);
// //                 alert("Error executing model");
// //             } else {
// //                 console.log("Output:", data.output);
// //                 alert("Model executed successfully");

// //                 const jsonData = getData(model);

// //             }
// //         })
// //         .catch((error) => {
// //             console.error(
// //                 "There was a problem with the fetch operation:",
// //                 error
// //             );
// //             alert("Error executing model");
// //         });

// //     var ref = collection(db, "TheStudentsList");
// //     const docRef = await addDoc(ref, getData('lccde')).then(() => {
// //         alert('data added successfully');
// //     }).catch((error) => {
// //         alert('Unsuccessful operation, error: ' + error);
// //     });
// // }

// // async function runModel(model) {
// //     console.log("run model is executing the current model: " + model);
// // }












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
    // console.log("we're in the function of " + model);
    console.log("run model is executing the current model: " + model);
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
                alert("Model " + model + "executed successfully");
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
    // let index = jsonData['epochs'];
    storeData(model);


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

export { runModel };










