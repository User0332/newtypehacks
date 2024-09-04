document.addEventListener("DOMContentLoaded", () => {
	const calendarElem = document.getElementById("calendar");

	const calendar = new FullCalendar.Calendar(calendarElem, {
		initialView: "dayGridMonth"
	});

	getAllCalendarEventObjects().then((eventInfos) => {
		for (const eventInfo of eventInfos) {
			const ev = calendar.addEvent({
				title: eventInfo.title,
				start: eventInfo.startTime,
				end: eventInfo.endTime,
				url: `/view-event?id=${eventInfo.id}`
			});
		}
	}).then(() => calendar.render());

});