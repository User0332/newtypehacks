const eventID = new URLSearchParams(location.search).get("id");

getEventInfo(eventID).then((eventInfo) => {
	const title = document.getElementById("event-title");
	const description = document.getElementById("event-description");
	const startTimeElem = document.getElementById("start-time");
	const endTimeElem = document.getElementById("end-time");

	title.textContent = `Event '${eventInfo.title}'`;
	description.textContent = eventInfo.description;

	const startTime = new Date(eventInfo.startTime);
	const endTime = new Date(eventInfo.endTime);

	const fmtOptions = {
		weekday: "long",
		year: "numeric",
		month: "numeric",
		day: "numeric",
		hour: "numeric",
		minute: "numeric"
	}

	startTimeElem.textContent = `Starts: ${startTime.toLocaleString("en-US", fmtOptions)}`;
	endTimeElem.textContent = `Ends: ${endTime.toLocaleString("en-US", fmtOptions)}`;
})