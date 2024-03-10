// ParkingSpace.js
const { DataTypes } = require("sequelize");
const { sequelize } = require("../config/db");

const ParkingSpace = sequelize.define(
  "ParkingSpace", // Model name (singular)
  {
    spaceId: {
      type: DataTypes.STRING,
      allowNull: false,
      unique: true,
    },
    availability: {
      type: DataTypes.BOOLEAN,
      allowNull: false,
    },
  },
  {
    //tableName: "parking_spaces",
    //tableName: "parkingspaces",
    tableName: "parkingspacesip",
    timestamps: false,
    // Table name in the database (plural)
  }
);

// Synchronize the model with the database
ParkingSpace.sync().then(() => {
  console.log("ParkingSpace table created (if not existed)");
});

module.exports = ParkingSpace;
