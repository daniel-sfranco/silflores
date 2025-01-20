const actUser = document.getElementById("data").getAttribute("data-user");
const cartUser = document.getElementById("data").getAttribute("data-con");
const wsUrl = new URL(window.location.href);
const ws = new WebSocket(`ws://${wsUrl.host}/ws/chat/${cartUser}-cart`);
const messageInput = document.getElementById("message-input");


ws.onopen = () => {
    const messageList = document.getElementById('messages');
    if (messageList) {
        fetch(`/cart/${cartUser}/messages`, {
            method: "GET",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            }
        })
        .then(response => response.json())
        .then(data => {
            messageList.innerHTML = ''
            if(data.length > 0) {
                let lastDate = ''
                data.messages.forEach(message =>{
                    if(message.date != lastDate){
                        lastDate = message.date
                        const dateP = document.createElement('p')
                        dateP.innerHTML = lastDate
                        dateP.classList.add("dateP")
                        messageList.append(dateP)
                    }
                    const messageContent = document.createElement('p')
                    messageContent.classList.add("messageContent")
                    messageContent.innerHTML = message.content
                    const messageTime = document.createElement('p')
                    messageTime.classList.add('messageTime')
                    messageTime.innerHTML = message.time
                    if(message.sender == actUser){
                        messageContent.style = "text-align: right"
                        messageTime.style = "text-align: right"
                    }
                    messageList.append(messageContent)
                    messageList.append(messageTime)
                    messageList.scrollTop = messageList.scrollHeight;
                })
            }
        })
    }
    console.log("Conexão WebSocket estabelecida");
};

ws.onmessage = (event) => {
    window.location.href = `/cart/${cartUser}/page`;
	messageInput.click()
};

ws.onerror = (error) => {
    console.error("Erro na conexão WebSocket:", error);
};

ws.onclose = (event) => {
    console.log("Conexão WebSocket fechada:", event);
};

function sendMessage(message, sender) {
    const messageToSend = {
        message: `${sender}: ${message}`,
    };
    ws.send(JSON.stringify(messageToSend));
}

document.getElementById("send-message").addEventListener("click", () => {
    sendMessage(messageInput.value, actUser);
    messageInput.value = "";
	messageInput.click()
});

document
    .getElementById("message-input")
    .addEventListener("keyup", ({ key }) => {
        if (key === "Enter") {
            sendMessage(messageInput.value, actUser);
            messageInput.value = "";
			messageInput.click()
        }
    });
