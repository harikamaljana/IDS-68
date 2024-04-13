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
var dbReference = firebase.database().ref('idst68');

const saveMessages = (data) => {
    var dataSend = dbReference.push();
    dataSend.set(data);
}