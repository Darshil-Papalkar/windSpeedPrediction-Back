const axios = require("axios");
const request = require('request-promise');

const rawData = require('./response.json');

module.exports.getLocation = async (req, res, next) => {
    try {
        console.log("Starting Data Processing");
        const location = req.query.location;
        const result = await axios.get(`https://api.weatherbit.io/v2.0/history/daily?city=${location}&country=India&start_date=2021-10-10&end_date=2022-10-08&key=${process.env.WEATHER_API}`);

        // console.log(result);

        const windOptions = {
            method: 'POST',
            uri: 'http://127.0.0.1:5001/windPrediction',
            body: result,
            json: true
        };

        const tempOptions = {
            method: 'POST',
            uri: 'http://127.0.0.1:5001/tempPrediction',
            body: result,
            json: true
        };

        const sendWindReq = await request(windOptions)
            .then((response) => {
                if (response && response?.result === 'ok') {
                    return response;
                }
            })
            .catch(err => {
                console.log(err);
                next(err);
            });

        const sendTempReq = await request(tempOptions)
            .then((response) => {
                if (response && response?.result === 'ok') {
                    return response;
                }
            })
            .catch(err => {
                console.log(err);
                next(err);
            });

        console.log("Ending Data Processing");
        return res.json({
            windStatus: sendWindReq && sendWindReq.data ? true : false,
            tempStatus: sendTempReq && sendTempReq.data ? true : false,
            windData: sendWindReq?.data,
            tempData: sendTempReq?.data,
            development: false,
            location
        });
    }
    catch (err) {
        console.error("Processing Terminated");
        console.error(err.message);

        if (err?.response?.status === 429) {
            res.redirect('development');
        }
        else {
            next(err);
        }
    }
};

module.exports.development = async (req, res, next) => {
    try {
        console.log("Development Starting Data Processing")
        const windOptions = {
            method: 'POST',
            uri: 'http://127.0.0.1:5001/windPrediction',
            body: rawData,
            json: true
        };

        const tempOptions = {
            method: 'POST',
            uri: 'http://127.0.0.1:5001/tempPrediction',
            body: rawData,
            json: true
        };

        const sendWindReq = await request(windOptions).then((r) => {
            return r;
        })
            .catch(err => {
                console.log(err);
                next(err);
            });

        const sendTempReq = await request(tempOptions).then((r) => {
            return r;
        })
            .catch(err => {
                console.log(err);
                next(err);
            });

        console.log("Development Ending Data Processing");
        return res.json({
            windStatus: sendWindReq && sendWindReq.data ? true : false,
            tempStatus: sendTempReq && sendTempReq.data ? true : false,
            windData: sendWindReq?.data,
            tempData: sendTempReq?.data,
            development: true,
            location: 'chennai'
        });

    }
    catch (err) {
        console.error("Processing Terminated");
        console.error(err.message);
        next(err);
    }
};