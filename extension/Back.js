chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  if (request.action === "batch") {
    const number = request.parameter1;
    // const endDate = request.parameter2;

    fetch("http://localhost:5000/batch_classify", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ number: number }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data.name);
        console.log("routed");
      });

    return true;
  }

  if (request.action === "start") {
    fetch("http://localhost:5000/realtime_classify", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        const emailId = data.id;
        const labelName = data.label;
        console.log("Email message ID is " + emailId);
        console.log("Label Name is " + labelName);
        chrome.identity.getAuthToken({ interactive: true }, function (token) {
          if (chrome.runtime.lastError) {
            console.error(
              "Error in getting auth token:",
              chrome.runtime.lastError
            );
            return;
          }
          createLabelOnGmail(token, labelName)
            .then((createdLabel) => {
              console.log("Label created on Gmail:", createdLabel);
              const labelId = createdLabel.id;
              console.log(labelId);
              console.log(token);
              applyLabelToEmail(token, emailId, labelId)
                .then(() => {
                  console.log("Label applied");
                  return;
                })
                .catch((error) => {
                  console.log("Error assigning label", error);
                });
            })
            .catch((error) => {
              console.error("Error creating label on Gmail:", error);
            });
        });
      })
      .catch((error) => {
        console.error("Error fetching data from server:", error);
      });
    return true;
  }
});

function createLabelOnGmail(token, labelName) {
  // First, check if the label already exists
  return fetch(
    `https://www.googleapis.com/gmail/v1/users/me/labels?name=${encodeURIComponent(
      labelName
    )}`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  )
    .then((response) => {
      if (!response.ok) {
        throw new Error(
          `Failed to check if label exists. Status: ${response.status}, ${response.statusText}`
        );
      }
      return response.json();
    })
    .then((data) => {
      // Check if the response contains labels
      if (!Array.isArray(data.labels)) {
        throw new Error(
          "Invalid response format. Expected an array of labels."
        );
      }

      // Check if label with the same name already exists
      const existingLabel = data.labels.find(
        (label) => label.name === labelName
      );
      if (existingLabel) {
        console.log(`Label '${labelName}' already exists. Skipping creation.`);
        return { name: existingLabel.name, id: existingLabel.id };
      } else {
        // If label does not exist, create it
        return fetch("https://www.googleapis.com/gmail/v1/users/me/labels", {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            name: labelName,
            labelListVisibility: "labelShow",
            messageListVisibility: "show",
          }),
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error(
                `Failed to create label on Gmail. Status: ${response.status}, ${response.statusText}`
              );
            }
            return response.json();
          })
          .then((label) => {
            console.log("Label created:", label);
            return { name: label.name, id: label.id };
          })
          .catch((error) => {
            console.error("Error creating label on Gmail:", error);
            throw error;
          });
      }
    })
    .catch((error) => {
      console.error("Error checking label existence:", error);
      throw error;
    });
}

function applyLabelToEmail(token, id, labelId) {
  console.log(token);
  console.log("message id is " + id);
  return fetch(
    `https://gmail.googleapis.com/gmail/v1/users/me/messages/${id}/modify`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        addLabelIds: [labelId],
      }),
    }
  )
    .then((response) => {
      if (!response.ok) {
        throw new Error(
          `Failed to apply label to email. Status: ${response.status}, ${response.statusText}`
        );
      }
      console.log(`Label applied to email ${id}`);
    })
    .catch((error) => {
      console.error("Error applying label to email:", error);
      throw error; // Rethrow the error to be caught in the main function
    });
}
