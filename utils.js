var utils = {

  minMax: [
    { min: 0, max: 12},    // synny hours per day or
    { min: 0, max: 35},    // temperature
    { min: 0, max: 200},   // precipitation
    { min: 0, max: 28},    // sea
    { min: 0, max: 200},   // snow depth mm
    { min: 1, max: 3},     // season
    { min: 100, max: 300}, // flight price
  ],

   highSeasons: [22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39],
   midSeasons: [18,19,20,21,40,41,42,43],

   randomIntFromInterval: function(min,max){
       return Math.floor(Math.random()*(max-min+1)+min);
   },

  generateFakeData: function(){

      let weekData = [];
      for( var i = 1; i < 53; i++){
        let season = 1;
        if(this.highSeasons.indexOf(i) !== -1 )
          season = 3;
        else if(this.midSeasons.indexOf(i) !== -1 ) season = 2;

        weekData.push( {
          'week': i,
          'sunnydays': this.randomIntFromInterval(this.minMax[0].min,this.minMax[0].max), // pts
          'temp': this.randomIntFromInterval(this.minMax[1].min,this.minMax[1].max),      // ast
          'precip': this.randomIntFromInterval(this.minMax[2].min,this.minMax[2].max),    // reb
          'water': this.randomIntFromInterval(this.minMax[3].min,this.minMax[3].max),     // stl
          'snow': this.randomIntFromInterval(this.minMax[4].min,this.minMax[4].max),      // blk
          'season': season,                                                               // tov
          'flight': this.randomIntFromInterval(this.minMax[6].min,this.minMax[6].max),    // min
        });
      }
      return weekData;
  },

  log: function(){
    console.log();
  },
  getDateString: function(date){

    if(!date)
      date = new Date();

    return date.toISOString().
              replace(/T/, ' ').      // replace T with a space
              replace(/\..+/, '')     // delete the dot and everything after
  },

  runCmd:
    function run_cmd(cmd, args, callBack ) {
      var spawn = require('child_process').spawn;
      var child = spawn(cmd, args);
      var resp = "";

      child.stdout.on('data', function (buffer) { resp += buffer.toString() });
      child.stdout.on('end', function() { callBack (resp) });
  } ,// ()

};

module.exports = utils;
