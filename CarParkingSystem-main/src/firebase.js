import { initializeApp } from "firebase/app";
import { getDatabase } from "firebase/database";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDE_AIIZtrzMDieckqkE7Ng7upt_UI36AI",
  authDomain: "indoor-car-park-management.firebaseapp.com",
  databaseURL: "https://indoor-car-park-management-default-rtdb.firebaseio.com",
  projectId: "indoor-car-park-management",
  storageBucket: "indoor-car-park-management.appspot.com",
  messagingSenderId: "1039322398918",
  appId: "1:1039322398918:web:cbbc3b11af07070ffe57c7",
  measurementId: "G-DLGH57QFPY"
};


// Initialize Firebase app and database
const app = initializeApp(firebaseConfig);
const database = getDatabase(app);

// Export the database object
export const databaseRef = database;