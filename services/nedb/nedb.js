const http = require('http');
const express = require('express');
const socketio = require('socket.io');
const Datastore = require('nedb');
const app = express();
const server = http.createServer(app);
const io = socketio(server);
const port = 6666;

const db = new Datastore({
  filename: 'dreamDB',
  autoload: true,
  schema: {
    sessionId: { type: String, required: true },
    recordIndex: { type: String, required: true },
    uploaded: { type: Boolean, required: true, default: false },
    gps: {
      time:{ type: String,format: "date-time",required: true,default: () => new Date().toISOString()},
      lat: { type: Number, required: true, default:0 },
      lon: { type: Number, required: true, default:0 },
      sats: { type: Number, required: true, default:-1 },
      fix: { type: Number, required: true, default:-1 },
    },
    pressure: { type: Number, required: true, default: 0 },
    temperature: { type: Number, required: true, default: 0 },
    light: { type: Number, required: true, default: 0 },
    do: { type: Number, required: true, default: 0 },
    ph: { type: Number, required: true, default: 0 },
    runtime: { type: Number, required: true, default: 0 },
    message: { type: String, required: false, default: '' }, 
  }
});

app.use(express.json());
app.use(express.static('public'));
app.use((req, res, next) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
    res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
  next();
});
app.set('view engine', 'ejs');

app.post('/store', (req, res) => {
  const data = req.body;
  
  db.insert(data, (err, newDoc) => {
    if (err) {
      console.error(err);
      res.status(500).send({ message: 'Error storing data' });
    } else {
      console.log(`Data stored in database: ${JSON.stringify(newDoc)}`);
      res.status(200).send({ message: 'Data stored successfully' });
    }
  });
});

app.post('/fetch', (req, res) => {
  const query = req.body;

  db.find(query, (err, docs) => {
    if (err) {
      console.error(err);
      res.status(500).send({ message: 'Error fetching data' });
    } else {
      //console.log(`Data fetched from database: ${JSON.stringify(docs)}`);
      res.status(200).send(docs);
    }
  });
});

app.post('/updateUploadedStatus', (req, res) => {
  const recordIds = req.body.ids;

  db.update({ _id: { $in: recordIds } }, { $set: { uploaded: true } }, { multi: true }, (err, numAffected) => {
    if (err) {
      console.error(err);
      res.status(500).send({ message: 'Error updating uploaded status' });
    } else {
      console.log(`${numAffected} records updated in database`);
      res.status(200).send({ message: `${numAffected} records updated successfully` });
    }
  });
});

app.delete('/delete', (req, res) => {
  const query = { runtime: { $exists: false } };

  db.remove(query, { multi: true }, (err, numRemoved) => {
    if (err) {
      console.error(err);
      res.status(500).send({ message: 'Error deleting data' });
    } else {
      console.log(`${numRemoved} records deleted from database`);
      res.status(200).send({ message: `${numRemoved} records deleted successfully` });
    }
  });
});

app.get('/fetchNotUploaded', (req, res) => {
  const query = { uploaded: false };

  db.find(query, (err, docs) => {
    if (err) {
      console.error(err);
      res.status(500).send({ message: 'Error fetching data' });
    } else {
      console.log(`Data fetched from database: ${JSON.stringify(docs)}`);
      res.status(200).send(docs);
    }
  });
});

io.on('connection', socket => {
  console.log(`Client connected: ${socket.id}`);
  
  socket.on('store', data => {
    db.insert(data, (err, newDoc) => {
      if (err) {
        console.error(err);
      } else {
        console.log(`Data stored in database: ${JSON.stringify(newDoc)}`);
      }
    });
  });
  
  socket.on('fetch', query => {
    db.find(query, (err, docs) => {
      if (err) {
        console.error(err);
      } else {
        console.log(`Data fetched from database: ${JSON.stringify(docs)}`);
        socket.emit('fetched', docs);
      }
    });
  });
});

server.listen(port, () => {
  console.log(`Server started on port ${port}`);
});
