// parkingController.js

const ParkingSpace = require("../models/ParkingSpace");
const { testConnection } = require("../config/db");

const updateParkingStatus = async (spaceId, availability) => {
  try {
    await testConnection(); // Test the connection before updating

    let [parkingSpace] = await ParkingSpace.findOrCreate({
      where: { spaceId },
      defaults: {
        availability,
      },
    });

    if (!parkingSpace) {
      parkingSpace = new ParkingSpace({
        spaceId,
        availability,
      });
    } else {
      parkingSpace.availability = availability;
    }

    await parkingSpace.save();

    console.log(
      `Parking space ID: ${spaceId}, Availability: ${availability} - Updated in the database`
    );
  } catch (error) {
    console.error("Error updating parking status:", error.message);
  }
};


const getParkingStatus = async () => {
  try {
    await testConnection(); // Test the connection before querying

    // Find all parking spaces
    const parkingSpaces = await ParkingSpace.findAll();

    // Map the parking spaces to an array of space IDs and availabilities
    const parkingStatus = parkingSpaces.map((space) => ({
      spaceId: space.spaceId,
      availability: space.availability,
    }));

    return parkingStatus;
  } catch (error) {
    console.error("Error getting parking status:", error.message);
    return null;
  }
};

module.exports = { updateParkingStatus,getParkingStatus };
