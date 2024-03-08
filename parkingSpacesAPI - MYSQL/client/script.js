// const socket = io("http://localhost:3000");

// document.getElementById("form").addEventListener("submit", function (event) {
//   event.preventDefault();

//   const spaceId = document.getElementById("spaceId").value;
//   const availability = document.getElementById("availability").checked;

//   socket.emit("parkingStatus", { spaceId, availability });

//   document.getElementById("spaceId").value = "";
//   document.getElementById("availability").checked = false;

//   return false;
// });

// socket.on("connect", function () {
//   console.log("Connected to server");
// });

// socket.on("disconnect", function () {
//   console.log("Disconnected from server");
// });

// socket.on("parkingStatus", function (data) {
//   const messages = document.getElementById("messages");
//   const listItem = document.createElement("li");
//   listItem.appendChild(
//     document.createTextNode(
//       `Parking space ID: ${data.spaceId}, Availability: ${data.availability}`
//     )
//   );
//   messages.appendChild(listItem);
// });

// client.js
const authToken = "your_secret_token"; // Replace with your actual token
const socket = io("http://localhost:3000", {
  auth: {
    token: authToken,
  },
});

document.getElementById("form").addEventListener("submit", function (event) {
  event.preventDefault();

  const spaceId = document.getElementById("spaceId").value;
  const availability = document.getElementById("availability").checked;

  socket.emit("parkingStatus", { spaceId, availability });

  document.getElementById("spaceId").value = "";
  document.getElementById("availability").checked = false;

  return false;
});

socket.on("connect", function () {
  console.log("Connected to server");
});

socket.on("disconnect", function () {
  console.log("Disconnected from server");
});

socket.on("parkingStatus", function (data) {
  const messages = document.getElementById("messages");
  const listItem = document.createElement("li");
  listItem.appendChild(
    document.createTextNode(
      `Parking space ID: ${data.spaceId}, Availability: ${data.availability}`
    )
  );
  messages.appendChild(listItem);
});
