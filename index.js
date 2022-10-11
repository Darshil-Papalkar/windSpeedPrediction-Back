const express = require('express');
const cors = require('cors');

const getLocationInfo = require("./routes/locationRoutes");

require('dotenv').config();

const app = express();

app.use(cors());
app.use(express.json());

app.use("/api/auth", getLocationInfo);

app.listen(process.env.PORT, () => {
    console.log(`Server started on port ${process.env.PORT}`);
});