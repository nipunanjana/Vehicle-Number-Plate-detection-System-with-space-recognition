// db.js

const { Sequelize } = require("sequelize");

const sequelize = new Sequelize({
  dialect: "mysql",
  host: "localhost",
  username: "root",
  password: "12345",
  database: "parkingSpaces",
});

const testConnection = async () => {
  try {
    await sequelize.authenticate();
    console.log("Connection has been established successfully.");
  } catch (error) {
    console.error("Unable to connect to the database:", error);
  }
};

module.exports = { sequelize, testConnection };
