const messageInput = document.getElementById("message-input");
const messagePreview = document.getElementById("message-preview");
const messageContainer = document.getElementById("message-container");
const socket = io();
const md = window.markdownit();

messageInput.addEventListener('input', () => {
	messagePreview.innerHTML = md.render(messageInput.value);
});

socket.on("new-message", renderLocalMessage);

async function renderDBMessage(messageInfo) {
	const authorName = (await getUserInfo(messageInfo.author)).name;
	const messageContent = messageInfo.content;

	const messageDiv = document.createElement("div");
	messageDiv.className = "message";

	const authorElem = textElem("span", `${authorName}: `);
	authorElem.className = "author-name";
	authorElem.onclick = () => location.href = `/view-profile?id=${messageInfo.author}`;


	const messageElem = elem("div", md.render(messageContent));
	messageElem.className = "message-content";

	messageDiv.append(
		authorElem,
		messageElem
	);

	messageContainer.appendChild(messageDiv);

	messageContainer.scrollTop = messageContainer.scrollHeight;
}

async function renderLocalMessage(localMessageInfo) {
	const messageDiv = document.createElement("div");
	messageDiv.className = "message";

	const authorElem = textElem("span", `${localMessageInfo.authorName}: `);
	authorElem.className = "author-name";
	authorElem.onclick = () => location.href = `/view-profile?id=${localMessageInfo.authorID}`;

	const messageElem = elem("div", md.render(localMessageInfo.content));
	messageElem.className = "message-content";

	messageDiv.append(
		authorElem,
		messageElem
	);

	messageContainer.appendChild(messageDiv);

	messageContainer.scrollTop = messageContainer.scrollHeight;
}

async function renderAllDBMessages() {
	const messages = (await getAllMessages());

	for (const messageID of messages) {
		renderDBMessage(
			await getMessageInfo(messageID)
		);
	}
}

function sendMessage() {
	const messageContent = messageInput.value;

	sendMessageToServer(messageContent).then((resp) => {
		if (resp.status != "success") alert("You may not send messages in this thread!");
	});

	messageInput.value = "";
	messagePreview.innerHTML = "";
}

renderAllDBMessages();

messageInput.addEventListener("keydown", (ev) => {
	if ((ev.key == "Enter") && (ev.ctrlKey)) sendMessage();
});