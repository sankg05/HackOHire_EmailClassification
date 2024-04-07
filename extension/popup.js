document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("RealTime").addEventListener("click", function () {

    if(this.textContent === "Start")
    {
      this.textContent = "Stop"
     
    }
    else
    {
      this.textContent = "Start"
      return;
    }
    chrome.runtime.sendMessage({ action: "start" }, function (response) {
      // displayEmails(response.emails);
      console.log("started");
    });
  });

  

  const submitButton = document.getElementById('submitButton');

    submitButton.addEventListener('click', function() {
        const inputField = document.getElementById('inputField');
        const inputValue = inputField.value;
        console.log(inputValue);
        // Send input value to background script
        chrome.runtime.sendMessage( { action: "batch" , parameter1: inputValue}, function (response) {
          //   // displayEmails(response.emails);
            console.log(parameter1);
          //   console.log("started");
        });
    });

});


