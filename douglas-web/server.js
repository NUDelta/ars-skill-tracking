const wordDb = require('./WordDB.json');
const guruWords = require('./guru-words.json')
const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const GoogleSpreadsheet = require('google-spreadsheet');
const async = require('async');

const app = express();

app.use(express.static(path.join(__dirname, 'client/build')));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
    extended: true
}));

/*
app.use(express.static(path.join(__dirname, 'client/build')));
*/

var sheetKey = '1uF8K1LMLqv-El1_41j8u029bTFuC4x1WAyMbpBJC8DU';
var doc = new GoogleSpreadsheet(sheetKey);
var sheet;

requestData = {};

async.series([
  function getInfo(step) {
    doc.getInfo(function(err, info) {
      console.log('loaded doc: ' + info.title)
      sheet = info.worksheets[2];
      console.log(sheet.title)
      step();
    })
  },
  function updateRequestData(step) {
    sheet.getCells({
      'min-row': 33,
      'max-row': 60,
      'min-col': 1,
      'max-col': 5,
    }, function(err, cells) {
      for (var i = 0; i < cells.length; i+=3){
        requestData[cells[i].value] = (cells[i+1].numericValue + cells[i+2].numericValue);
      }
    });
  }
]);

setInterval(function() {
  if (sheet === undefined) return;
  sheet.getCells({
    'min-row': 33,
    'max-row': 60,
    'min-col': 1,
    'max-col': 5,
  }, function(err, cells) {
    console.log("Updating request data");
    for (var i = 0; i < cells.length; i+=3){
      requestData[cells[i].value] = (cells[i+1].numericValue + cells[i+2].numericValue);
    }
  });
}, 1500);


app.get('/api/ping', function (req, res) {
  console.log(parsePhrase('brainstorm'))
  console.log(parsePhrase('debug my meteor app brainstorm'))
  return res.send('pong');
});

app.get('/api/requestData', function(req, res) {
  res.send(requestData);
});

app.post('/api/helpers', function (req, res) {
  var phraseCategories = parsePhrase(req.body.task)
  return res.send(phraseCategories)
});

app.get('/api/getHelpers/:spreadsheetId/:task', function(req, res) {
  var sheetId = req.params.spreadsheetId;
  var task = req.params.task;

  var categories = parsePhrase(task);
  
  console.log(`${sheetId} needs help with: '${task}'`);
  console.log(`The categories are: '${categories}'`);

  var names = [];
  namesDict = guruWords['categories'];

  for (var category in categories){
    names = names.concat(namesDict[category]);
  }

  console.log(`People who can help: ${names}`)

  return res.send(names);
});

app.get('/api/:name', function (req, res) {
  console.log(`${req.params.name} has logged in`)
  return res.send('ok');
});

app.get('/api/:name/:category', function (req, res) {
  console.log(`${req.params.name} has clicked category: ${req.params.category}`)
  return res.send('ok');
});

app.get('*', function (req, res) {
  res.sendFile(path.join(__dirname, 'client/build', 'index.html'));
});


parsePhrase = function(phrase) {
  wordDict = wordDb['categories'];
  // list to hold our categories matched to phrase
  matchingCategories = []
  for (var category in wordDict) {
    // Words that match to a category
    // i.e. -> ["brainstorm", "idea", "come up with"]
    words = wordDict[category]
    for (var i=0; i<words.length; i++) { // "brainstorm", "idea", ...
      if (phrase.toLowerCase().indexOf(words[i]) != -1) { // If the string is in the phrase
        matchingCategories.push([category])
        break;
      }
    }
  }

  return matchingCategories
}

app.listen(process.env.PORT || 8080);
