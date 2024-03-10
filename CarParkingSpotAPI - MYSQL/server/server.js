// this  server.js code
const express = require("express");
const http = require("http");
const { Server } = require("socket.io");
const connectDB = require("./config/db");
const { updateParkingStatus ,getParkingStatus} = require("./controllers/ParkingController");


const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    
    origin: ["http://127.0.0.1:5000", "http://localhost:3000"],
    methods: ["GET", "POST"],
  },
});



// Authentication middleware
io.use((socket, next) => {
  const token = socket.handshake.auth.token;

  // Your authentication logic here (check token, validate user, etc.)
  if (isValidToken(token)) {
    return next();
  }

  // If authentication fails, disconnect the socket
  return next(new Error("Authentication failed"));
});




io.on("connection", (socket) => {
  console.log("A user connected:", socket.id);
  const sendInitialParkingStatus = async () => {
    try {
      const parkingStatus = await getParkingStatus();
      console.log(parkingStatus)
      io.to(socket.id).emit("initialParkingStatus", parkingStatus);
    } catch (error) {
      console.error("Error sending initial parking status:", error.message);
    }
  };

  sendInitialParkingStatus()

  socket.on("parkingStatus", async (data) => {
    try {
      await updateParkingStatus(data.spaceId, data.availability);
      io.emit("parkingStatus", {
        spaceId: data.spaceId,
        availability: data.availability,
      });

      // If you want to refresh the initial parking status after a parking status update,
      // you can call sendInitialParkingStatus() here
      sendInitialParkingStatus();
    } catch (error) {
      console.error("Error updating parking status:", error.message);
    }
  });

  socket.on("disconnect", () => {
    console.log("User disconnected:", socket.id);
  });
});

server.listen(5000, () => {
  console.log("Server listening on *:3000");
});

// Example function to validate the token (replace with your actual logic)
function isValidToken(token) {
  // Implement your token validation logic here
  return token === "your_secret_token";
}
