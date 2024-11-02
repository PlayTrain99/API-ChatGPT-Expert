let chatBox = document.querySelector(".chat-box");
let messageInput = document.querySelector("#message-input");
let sendBtn = document.querySelector("#send-btn");

function addMessage(message) {
    let messageDiv = document.createElement("div");


    messageDiv.innerHTML = 
    `<div class="d-flex justify-content-end mb-4">
        <div class="user-message">
            ${message}
        </div>
        <div>
            <img src="${userIconUrl}" class="user-icon">
        </div>
    </div>`;

    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}


function sendMessage() {
    let message = messageInput.value.trim();

    if (message !== "") {
    addMessage(message, true);

    fetch("/api", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message})
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        messageInput.value = ""; // Czyszczenie pola wprowadzania po wysłaniu
        let messageDiv = document.createElement("div");
        
        // Zakładamy, że 'data' ma pole 'response', które zawiera odpowiedź tekstową
        let responseText = data.response || "No response received."; // Jeśli 'data.response' jest undefined, użyj tekst zastępczy
            
        messageDiv.innerHTML = 
        `<div class="d-flex justify-content-start mb-4">
            <div>
                <img src="${botIconUrl}" class="bot-icon">
            </div>
            <div class="bot-message">
                ${responseText}
            </div>
        </div>`;
        
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;

        })
        .catch(error => console.error(error));
    }
}

sendBtn.addEventListener("click", sendMessage);
messageInput.addEventListener("keydown", event => {
    if (event.keyCode === 13 && !event.shiftKey) {
    event.preventDefault();
    sendMessage();
    }
});