const axios = require("axios");
const request = require('request-promise');

const rawData = require('./response.json');

module.exports.getLocation = async (req, res, next) => {
    try {
        const location = req.query.location;
        const result = await axios.get(`https://api.weatherbit.io/v2.0/history/daily?city=${location}&country=India&start_date=2021-10-10&end_date=2022-10-08&key=${process.env.WEATHER_API}`);
    
        // console.log(result);
    
        const options = {
            method: 'POST',
            uri: 'http://127.0.0.1:5001/windPrediction',
            body: result,
            json: true
        };

        const sendReq = await request(options)
                                .then((response) => {
                                    if(response && response?.result === 'ok'){
                                        return response;
                                    }
                                })
                                .catch(err => {
                                    console.log(err);
                                    next(err);
                                });

        return res.json({ status: sendReq && sendReq.data ? true : false, data: sendReq?.data, development: false });
    }
    catch (err) {
        if(err?.response?.status === 429) {
            res.redirect('development');
        }
        else
            next(err);
    }
};

module.exports.development = async (req, res, next) => {
    try{
        const options = {
            method: 'POST',
            uri: 'http://127.0.0.1:5001/windPrediction',
            body: rawData,
            json: true
        };

        const sendReq = await request(options).then((r) => {
            // console.log(r);
            return res.json({
                ...r, development: true
            });
        })
        .catch(err => {
            console.log(err);
            next(err);
        });
    }
    catch (err) {
        console.log(err);
        next(err);
    }
};