const { exec } = require('child_process');
const request = require('request');

const deviceName = require('os').hostname();
const apiUrl = 'endpoint';
const apiKey = 'key';

function updateTmateSession() {
  exec('sudo tmate -S /tmp/tmate.sock display -p \'#{tmate_ssh}\'', (error, stdout, stderr) => {
    if (error) {
      console.error(`Error running tmate: ${error}`);
      return;
    }

    const session_id = stdout.trim();

    const query = {
    $and: [
    	{ deviceName: deviceName },
        { serviceName: 'tmateSessionID' }
    ]};

    const options = {
      method: 'GET',
      url: apiUrl,
      headers: {
        'cache-control': 'no-cache',
        'x-apikey': apiKey,
        'content-type': 'application/json'
      },
      qs: { q: JSON.stringify(query) },
      json: true
    };

    request(options, (error, response, body) => {
      if (error) {
        console.error(`Error getting record from database: ${error}`);
        return;
      }

      if (body.length > 0) {
	console.log(body)
        const record_id = body[0]._id;
        const update_data = {
          extra: session_id
        };

        const options = {
          method: 'PUT',
          url: `${apiUrl}/${record_id}`,
          headers: {
            'cache-control': 'no-cache',
            'x-apikey': apiKey,
            'content-type': 'application/json'
          },
          body: update_data,
          json: true
        };

        request(options, (error, response, body) => {
          if (error) {
            console.error(`Error updating record in database: ${error}`);
          } else {
            console.log(`Record updated in database for tmateSessionID`);
          }
        });
      } else {
        const data = {
          deviceName: deviceName,
          serviceName: 'tmateSessionID',
          extra: session_id
        };

        const options = {
          method: 'POST',
          url: apiUrl,
          headers: {
            'cache-control': 'no-cache',
            'x-apikey': apiKey,
            'content-type': 'application/json'
          },
          body: data,
          json: true
        };

        request(options, (error, response, body) => {
          if (error) {
            console.error(`Error creating record in database: ${error}`);
          } else {
            console.log(`Record created in database for tmateSessionID`);
          }
        });
      }
    });
  });
}

// Run the updateTmateSession function every 5 minutes
updateTmateSession()
setInterval(updateTmateSession,10*60*1000)
