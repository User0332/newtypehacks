// authInfo should be defined prior to loading this library

async function makeAPICall(endpoint, body, method, extraHeaders) {
	return await fetch(endpoint, {
		headers: {
			Authorization: `Bearer ${(await getAuthInfo()).accessToken}`,
			...extraHeaders
		},
		method,
		body
	})
}

async function getJSONInfoFromAPICall(endpoint, body, method, headers) {
	return await (await makeAPICall(endpoint, body, method, headers)).json()
}

function getUserInfo(userID) {
	if (!userID) return getJSONInfoFromAPICall("/api/get-self");

	return getJSONInfoFromAPICall(`/api/get-user?id=${userID}`);
}

function getAllMessages() {
	return getJSONInfoFromAPICall(`/api/list-messages`);
}

function getAllCalendarEvents() {
	return getJSONInfoFromAPICall(`/api/calendar/list-events`);
}

function getAllCalendarEventObjects () {
	return getJSONInfoFromAPICall(`/api/calendar/get-aggregated-event-info`);
}

function getEventInfo(eventID) {
	return getJSONInfoFromAPICall(`/api/calendar/get-event?id=${eventID}`);
}

function getMessageInfo(messageID) {
	return getJSONInfoFromAPICall(`/api/get-message?id=${messageID}`);
}

function sendMessageToServer(content) {
	return getJSONInfoFromAPICall(`/api/send-message`, JSON.stringify({
		content
	}), "POST", {
		"Content-Type": "application/json"
	});
}