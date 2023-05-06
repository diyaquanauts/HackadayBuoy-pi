const request = require("request");
const { exec } = require('child_process');
const os = require('os');

const BASE_URL = 'Deployment Endpoint';
const API_KEY = 'CORS KEY';

function updateDatabase() {
  exec('./status.sh', (error, stdout, stderr) => {
    if (error) {
      console.error(`Error running status.sh: ${error}`);
      return;
    }

    const output = stdout.trim();
    const regex = /●\s(.*?)\s-\s(.*?)\sLoaded:\s(.*?)\sActive:\s(.*?)\ssince\s(.*)/;

    if (regex.test(output)) {
      const [, name, description, loaded, active, status, since] = output.match(regex);

      const data = {
        deviceName: os.hostname(),
        serviceName: name,
        description: description,
        loaded: loaded,
        active: active,
        status: status,
        since: since,
	extra: "",
      };

      checkDatabaseForRecord(data)
        .then((record) => {
          if (record) {
            updateRecordInDatabase(record._id, data);
          } else {
            createRecordInDatabase(data);
          }
        })
        .catch((error) => {
          console.error(error);
        });
    } else {
      console.error('Error parsing output from status.sh');
    }
  });
}

function checkDatabaseForRecord(data) {
  const query = {
    $and: [
      { deviceName: data.deviceName },
      { serviceName: data.serviceName }
    ]
  };
  const options = {
    method: 'GET',
    url: BASE_URL,
    headers: {
      'cache-control': 'no-cache',
      'x-apikey': API_KEY,
      'content-type': 'application/json'
    },
    qs: { q: JSON.stringify(query) },
    json: true
  };
  return new Promise((resolve, reject) => {
    request(options, (error, response, body) => {
      if (error) {
        reject(error);
      } else {
        const records = body.filter(record =>
          record.deviceName === data.deviceName &&
          record.serviceName === data.serviceName);
        const record = records.length > 0 ? records[0] : null;
        resolve(record);
      }
    });
  });
}

function createRecordInDatabase(data) {
  const options = {
    method: 'POST',
    url: BASE_URL,
    headers: {
      'cache-control': 'no-cache',
      'x-apikey': API_KEY,
      'content-type': 'application/json'
    },
    body: data,
    json: true
  };
  request(options, (error, response, body) => {
    if (error) {
      console.error(`Error creating record in database: ${error}`);
    } else {
      console.log(`Record created in database for ${data.serviceName}`);
    }
  });
}

function updateRecordInDatabase(id, data) {
  const options = {
    method: 'PUT',
    url: `${BASE_URL}/${id}`,
    headers: {
      'cache-control': 'no-cache',
      'x-apikey': API_KEY,
      'content-type': 'application/json'
    },
    body: data,
    json: true
  };
  request(options, (error, response, body) => {
    if (error) {
      console.error(`Error updating record in database: ${error}`);
    } else {
      console.log(`Record updated in database for ${data.serviceName}`);
    }
  });
}

updateDatabase()
