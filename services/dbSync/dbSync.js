const axios = require('axios');
var request = require("request");
const dns = require('dns');
const fs = require('fs');
const csv = require('fast-csv');
const moment = require('moment');

// Cache to store the last processed data
const lastProcessedData = {};

// Function to group data by date
function groupDataByDate(data) {
  const groupedData = {};

  data.forEach(item => {
    const date = moment(item.gps.time).format('YYYY-MM-DD');
    if (!groupedData[date]) {
      groupedData[date] = [];
    }
    groupedData[date].push(item);
  });

  return groupedData;
}

// Function to sort data
function sortData(data) {
  return data.sort((a, b) => {
    if (a.gps.time === b.gps.time) {
      return a.runtime - b.runtime;
    }
    return new Date(a.gps.time) - new Date(b.gps.time);
  });
}

// Function to save data to CSV
function saveDataToCSV(date, data) {
  const csvFilePath = `csv/${date}.csv`;
  const flattenedData = flattenGpsObject(data);

  // Check if the CSV file already exists
  if (fs.existsSync(csvFilePath)) {
    // Append new data to the existing CSV file
    const ws = fs.createWriteStream(csvFilePath, { flags: 'a' });
    csv
      .write(flattenedData, { headers: false })
      .pipe(ws)
      .on('finish', () => {
        console.log(`Data appended to CSV: ${csvFilePath}`);
      });
  } else {
    // Create a new CSV file and write the data
    const ws = fs.createWriteStream(csvFilePath);
    csv
      .write(flattenedData, { headers: true })
      .pipe(ws)
      .on('finish', () => {
        console.log(`Data saved to CSV: ${csvFilePath}`);
      });
  }
}

// Flatten the 'gps' object
function flattenGpsObject(data) {
  return data.map(item => {
    const { gps, ...rest } = item;
    return { ...rest, ...gps };
  });
}

// Process data received from the server
function processData(data) {
  const groupedData = groupDataByDate(data);

  for (const date in groupedData) {
    const sortedData = sortData(groupedData[date]);

    // Check if the new data is different from the last processed data
    if (
      !lastProcessedData[date] ||
      JSON.stringify(sortedData) !== JSON.stringify(lastProcessedData[date])
    ) {
      lastProcessedData[date] = sortedData;
      saveDataToCSV(date, sortedData);
    }
  }
}

async function checkInternetConnection() {
  return new Promise((resolve, reject) => {
    dns.lookup('google.com', (err) => {
      if (err && err.code === 'ENOTFOUND') {
        reject(false);
      } else {
        resolve(true);
      }
    });
  });
}

async function updateUploadedStatus (recordIds){
  try {
    const response = await axios.post('http://localhost:6666/updateUploadedStatus', { ids: recordIds });
    console.log('Uploaded status updated:', response.data);
  } catch (error) {
    console.error('Error updating uploaded status:', error);
  }
};

async function syncRestDb() {
  try {
    const isConnected = await checkInternetConnection();
    if (!isConnected) return;
    const response = await axios.get('http://localhost:6666/fetchNotUploaded');

    if (!response.data.length) {
      console.log('No data to upload');
      return;
    }

    const postData = response.data.map(record => {
      return ({
        sessionId: record.sessionId,
        recordIndex : record.recordIndex,
        datetime: record.gps.time,
        lat: record.gps.lat,
        lon: record.gps.lon,
        sats: record.gps.sats,
        fix: record.gps.fix,
        pressure: record.pressure,
        temperature: record.temperature,
        light: record.light,
        ph: record.ph,
        do: record.do,
        debug: record.debug,
        runtime: record.runtime
      });
    });

    console.log('Data fetched:', response.data);

    // Process the fetched data and save it to a CSV file
    //rocessData(response.data);

    var options = {
      method: 'POST',
      url: 'RESTDB END POINT',
      headers: {
        'cache-control': 'no-cache',
        'x-apikey': 'YOUR CORS API KEY',
        'content-type': 'application/json'
      },
      body: postData,
      json: true
    };

    request(options, async function (error, response, body) {
      if (error) throw new Error(error);

      console.log(body);

      // Update the "uploaded" status of the records in NeDB
      const recordIds = postData.map(record => record._id);
      await updateUploadedStatus(recordIds);
    });
  } catch (error) {
    console.error('Error fetching data:', error);
  }
}

syncRestDb();
setInterval(syncRestDb, 60000);


