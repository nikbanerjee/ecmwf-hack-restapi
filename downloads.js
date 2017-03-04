var Q = require('q');

const pythonShell = require('python-shell');
const utils = require('./utils.js');
const config = require ('./config.js')

var downloads = {

  timerId: null,
  busy: false,
  prevDate: "none",

  setDataRefreshFrequency:

    function(hours, emiter) {

      this.emitter = emiter;
      console.log(utils.getDateString() + ' start');
      if(this.timerId) clearTimeout(this.timerId);
      if(hours>0)
        this.timerId = setInterval(this.getNewDataset.bind(this),hours);
    },

    getNewDataset: function(){

      if(!this.busy) {
        var self = this;

        console.log(utils.getDateString() + " Trying to connect to FTP and download new files ...");
        this.busy = true;
        var options = {
          scriptPath: './scripts',
          args: [config.dataPath, this.prevDate]
        };

        pythonShell.run('downloadFTP.py' , options, function(err, results){
          if(err) throw err;
          // console.log('results: %j', results);;
          //res.json(results);
          self.busy = false;
          if(self.emitter)
            self.emitter.emit('dataReady', {lastDate: results, lastError: err});
        })
      }
    },

};

module.exports = downloads;
