/**
* Call onOpen once a sheet is installed to load everything.
*/
function onInstall(e) {
  onOpen(e);
}

/**
* Setup dropdown menu on load of Polaris.
*/
function onOpen(e) {
  var ui = SpreadsheetApp.getUi();

  // setup menu
  ui.createMenu("Douglas")
  .addItem("Show Sidebar 1", "initializeSideBar")
  .addItem("Show Sidebar 2", "initializeSideBar2")
  .addToUi();
  }

function include(filename) {
  return HtmlService.createHtmlOutputFromFile(filename).getContent();
}

function initializeSideBar() {
  var html = HtmlService.createTemplateFromFile('sidebar').evaluate()
  .setTitle('Douglas Recommender 1');
  SpreadsheetApp.getUi() // Or DocumentApp or FormApp.
  .showSidebar(html);
}

function initializeSideBar2() {
  var html = HtmlService.createTemplateFromFile('sidebar2').evaluate()
  .setTitle('Douglas Recommender 2');
  SpreadsheetApp.getUi() // Or DocumentApp or FormApp.
  .showSidebar(html);
}

function callAPI(task_query) {
  var form_data = {
    'task_query': task_query
  };
  var options = {
    'method': 'post',
    'payload': form_data,
    muteHttpExceptions: true
  };
  var response = UrlFetchApp.fetch('https://stark-anchorage-45810.herokuapp.com/get_helpers', options);
  var response_code = response.getResponseCode();
  var response_body = response.getContentText();
  
  var json = {};
  
  if (response_code == 200) {
    json = JSON.parse(response_body);
  } else {
    Logger.log(Utilities.formatString("Request failed. Expected 200, got %d: %s", response_code, response_body));
  }
  
  // return json data
  return json['result'];

}

function testCallAPI() {
  
  var task_query = 'i need help debugging my meteor app'
  
  var form_data = {
    'task_query': task_query
  };
  var options = {
    'method': 'post',
    'payload': form_data,
    muteHttpExceptions: true
  };
  var response = UrlFetchApp.fetch('https://stark-anchorage-45810.herokuapp.com/get_helpers', options);
  var response_code = response.getResponseCode();
  var response_body = response.getContentText();
  
  var json = {};
  
  if (response_code == 200) {
    json = JSON.parse(response_body);
  } else {
    Logger.log(Utilities.formatString("Request failed. Expected 200, got %d: %s", response_code, response_body));
  }
  
  // return json data
  Logger.log(Utilities.formatString("Request response: %s", json));

}

