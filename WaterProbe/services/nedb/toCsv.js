const fs = require('fs');
const csv = require('fast-csv');
const moment = require('moment');
const axios = require('axios');

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
  const ws = fs.createWriteStream(`csv/${date}.csv`);
  const flattenedData = flattenGpsObject(data);
  csv
    .write(flattenedData, { headers: true })
    .pipe(ws)
    .on('finish', () => {
      console.log(`Data saved to CSV: csv/${date}.csv`);
    });
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

// Fetch data from the server
axios
  .post('http://localhost:6666/fetch')
  .then(response => {
    processData(response.data);
  })
  .catch(error => {
    console.error(`Error fetching data: ${error.message}`);
  });

