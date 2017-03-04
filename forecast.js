
var express = require('express')
var pythonShell = require('python-shell')
var events = require('events');
var eventEmitter = new events.EventEmitter();

const config = require ('./config.js')
const utils = require ('./utils.js')
const downloads = require ('./downloads.js')

pythonShell.defaultOptions = { scriptPath: './scripts' };

var router = express.Router();
var app = express()

var dataFiles = {
  lastDate: ""
}

// TODO just for development
app.set('json spaces', 10);

// -- middleware - authorisation? ----------------------------------------------
router.use(function(req,res,next) {
  next();
});


// -----------------------------------------------------------------------------
router.get("/trend",function(req,res){

    var lat = req.param('lat');
    var lon = req.param('lon');

    console.log(lat, lon);

    var options = {
      args: [config.dataPath + 'mars0.grib', '20.5', '0.5']
    };

    // pythonShell.run('trend.py' , options, function(err, results){
    //   if(err) throw err;
    //   // console.log('results: %j', results);;
    //   res.json(results);
    // })

    res.json(utils.generateFakeData());
});

// -----------------------------------------------------------------------------
router.get("/hourly",function(req,res){

    // var lat = req.param('lat');
    // var lon = req.param('lon');

    var options = {
      // args: [config.dataPath + 'era5_test_2016-01-01to2016-01-05_hourly.grib', '20.5', '0.5']
      args: [config.dataPath + 'mars0.grib', '20.5', '0.5']
    };

    pythonShell.run('test.py' , options, function(err, results){
      if(err) throw err;
      // console.log('results: %j', results);;
      res.json(results);
    })
});

// -- point forecast -----------------------------------------------------------
router.get("/weather",function(req,res){

    var lat = req.param('lat');
    var lon = req.param('lon');

    pythonShell.run('getPointForecast.py', function(err, results){
      if(err) throw err;
      // console.log('results: %j', results);;
      res.json(results);
    })
    var ret = {
      "Status": "Waiting ..."
    };
    res.json(ret);
    res.sendStatus(200);
});

router.get("/",function(req,res){
  var ret = {
  "REST API": "ECWMF",
    "version": "0.01",
    "latestData": dataFiles.lastDate
  };
  res.json(ret);
});

app.use("/api",router);

app.use("*",function(req,res){
  res.status(404).send("Ops, wrong request!");
});

app.listen(5199, function(){
  console.log('forecast server is waiting on port 5199')
})

// finally schedule actualization of forecast data
//downloads.setDataRefreshFrequency(config.refreshInterval, eventEmitter);

eventEmitter.on('dataReady', function(result){
    console.log(utils.getDateString() + ' New dataset is ready for requests! lastDate=' + result.lastDate);
    if(result.lastError)
      console.log(utils.getDateString() + '!Errror! ' + result.lastError);
});
