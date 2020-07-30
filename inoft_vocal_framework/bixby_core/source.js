
let json_template = require('./dummy_test.json');

function build(intent) {
    console.log(intent);

    let endpoints_json = {
        "action-endpoints": {
        }
    }
    endpoints_json["action-endpoints"].

    /*endpoints {
  action-endpoints {
    action-endpoint (launch) {
      accepted-inputs ($vivContext)
      // local-endpoint (launch.js)
      remote-endpoint ("{remote.url}") {
        method (POST)
      }
    }
    action-endpoint (ANumber) {
      accepted-inputs ($vivContext, IntNumber)
      local-endpoint (ANumber.js)
    }
    action-endpoint (GetContent) {
      accepted-inputs (searchTerm, $vivContext)
      local-endpoint (GetContent.js)
    }
  }
}*/
}

for (let intent_key in json_template.intents) {
    if (json_template.intents.hasOwnProperty(intent_key)) {
        build(json_template.intents[intent_key]);
    }
}