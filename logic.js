const util = require('./util');
const axios = require('axios');

module.exports = {
     fetchspecs(system){
        const endpoint = 'https://86.169.43.163/api/monitoring/host/specs';
        const url = endpoint
        console.log(url); // in case you want to try the query in a web browser

        var config = {
            timeout: 6500, // timeout api call before we reach Alexa's 8 sec timeout, or set globally via axios.defaults.timeout
            headers: {'Accept': 'application/json'}
        };

        async function getJsonResponse(url, config){
            const res = await axios.get(url, config);
            return res.data;
        }

        return getJsonResponse(url, config).then((result) => {
            return result;
        }).catch((error) => {
            return null;
        });
    },
};