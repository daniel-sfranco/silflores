const actUser = document.getElementById('data').getAttribute("data-user")
const cartUser = document.getElementById('data').getAttribute("data-con")
const wsUrl = new URL(window.location.href);
const ws = new WebSocket(`ws://${wsUrl.host}/ws/chat/${cartUser}-cart`);
const csrftoken = document.querySelector('[name="csrfmiddlewaretoken"]').value;


ws.onopen = () => {
	console.log('Conexão WebSocket estabelecida');
};

ws.onmessage = (event) => {
	const message = JSON.parse(event.data);
	const messageElement = document.getElementById('messages');
	const newMessage = document.createElement('p');
	newMessage.textContent = message.message;
	messageElement.appendChild(newMessage);
};

ws.onerror = (error) => {
	console.error('Erro na conexão WebSocket:', error);
};

ws.onclose = (event) => {
	console.log('Conexão WebSocket fechada:', event);
};

function sendMessage(message, sender) {
	const messageToSend = {
		message: `${sender}: ${message}`,
	};
	ws.send(JSON.stringify(messageToSend));
}

document.getElementById('send-message').addEventListener('click', () => {
	const messageInput = document.getElementById('message-input').value;
	sendMessage(messageInput, actUser);
	document.getElementById('message-input').value = '';
});

document.getElementById('message-input').addEventListener('keyup', ({key}) => {
	if(key === "Enter") {
		const messageInput = document.getElementById('message-input').value;
		sendMessage(messageInput, actUser);
		document.getElementById('message-input').value = '';
	}
})