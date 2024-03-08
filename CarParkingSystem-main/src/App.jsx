import Slot from "./components/slot";
import { useEffect, useState } from "react";
import io from "socket.io-client";



const SERVER_URL = "http://localhost:5000"; // Change this to your server URL
const AUTH_TOKEN = "your_secret_token"; 
const App = () => {
  const [allParkingStatus, setAllParkingStatus] = useState([]);

  useEffect(() => {
    const socket = io(SERVER_URL, {
      auth: {
        token: AUTH_TOKEN
      }
    });

    socket.on("connect_error", (error) => {
      console.error("Connection error:", error.message);
    });

    socket.on("initialParkingStatus", (parkingStatus) => {
      setAllParkingStatus(parkingStatus);
    });

    // Listen for parking status updates from the server
    socket.on("parkingStatus", (updatedStatus) => {
      setAllParkingStatus((prevStatus) => {
        // Update the parking status based on the received data
        return prevStatus.map((status) =>
          status.spaceId === updatedStatus.spaceId
            ? { ...status, availability: updatedStatus.availability }
            : status
        );
      });
    });

    // Clean up the socket connection when the component unmounts
    return () => {
      socket.disconnect();
    };
  }, []); 
  console.log(allParkingStatus)
  return (
    <>
      <div className="text-center mt-5 pb-3">
        <h3>SLT - Car Park System</h3>
      </div>

      <div className="my-5">
        {/* <ul>
          {messages.length !== 0
            ? messages.map((message, index) => <li key={index}>{message}</li>)
            : "No messages"}
        </ul> */}
      </div>

      <div className="col-12 col-xl-6 mx-auto d-flex flex-wrap">
        {allParkingStatus.map((plot) => (
          <Slot key={plot.id} slotId={plot.spaceId} slotStatus={plot.availability} />
        ))}
      </div>
    </>
  );
}

export default App;
