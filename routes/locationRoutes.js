const { getLocation, development } = require("../controllers/locationController");

const router = require("express").Router();

router.get("/getLocationInfo", getLocation);
router.get("/development", development);

module.exports = router;