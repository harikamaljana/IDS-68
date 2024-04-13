const firebaseConfig = {
    apiKey: "AIzaSyA90YRqnEPXJa5NRwpxKawNR6xU1Q2bnS8",
    authDomain: "idst68.firebaseapp.com",
    databaseURL: "https://idst68-default-rtdb.firebaseio.com",
    projectId: "idst68",
    storageBucket: "idst68.appspot.com",
    messagingSenderId: "25041131733",
    appId: "1:25041131733:web:17e923d98ec0fe8cf6aa5c",
    measurementId: "G-K245LCCKFX"
};

// initialize firebase
firebase.initializeApp(firebaseConfig);

// reference db
var idsFormDB = firebase.database().ref('idst68');
// console.log('howdy');
// document.getElementById('lccde-inputs').addEventListener('run-button', submitlccde);

function submitlccde(event) {
    event.preventDefault(); // prevents from refreshing the page

    var algorithm = getElementValue('lccde-algorithm');
    var dataset = getElementValue('lccde-dataset');
    var verbose = getElementValue('lccde-verbose');
    var boosting_type = getElementValue('lccde-boosting');
    var epochs = getElementValue('lccde-epochs');
    console.log('called');
    console.log(algorithm, dataset, verbose, boosting_type, epochs);
}

const getElementValue = (id) => {
    return document.getElementById(id).value;
};