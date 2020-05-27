// Replace with the URL to your deployed Cloud Function
var url = "https://us-central1-dashybutts.cloudfunctions.net/function-1"

// This function will be called when the form is submitted
function onSubmit(event) {

  // The event is a FormResponse object:
  // https://developers.google.com/apps-script/reference/forms/form-response
  var formResponse = event.response;

  // Gets all ItemResponses contained in the form response
  // https://developers.google.com/apps-script/reference/forms/form-response#getItemResponses()
  var itemResponses = formResponse.getItemResponses();

  // Gets the actual response strings from the array of ItemResponses
  var responses = itemResponses.map(function getResponse(e) { return {title: e.getItem().getTitle(), response: DriveApp.getFileById(e.getResponse()).getDownloadUrl()} });
  
  var payload = JSON.stringify({
        "responses": responses
      });
  console.log(payload);
  // Post the payload as JSON to our Cloud Function  
  UrlFetchApp.fetch(
    url,
    {
      "method": "post",
      "payload": payload
    }
  );
}