const Datastore = require('PowerPCB/PowerMonitor/nedb/nedb');

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

const deleteRecords = () => {
 db.remove({}, { multi: true }, (err, numRemoved) => {
    if (err) {
      console.error(err);
      return;
    } else {
      console.log(`${numRemoved} records deleted from database`);
    }
  });
};

deleteRecords();
