document.addEventListener("DOMContentLoaded", () => {
	const calendarElem = document.getElementById("calendar");

	const calendar = new FullCalendar.Calendar(calendarElem, {
		initialView: "dayGridMonth"
	});

	const ev = calendar.addEvent({
		title: "Meeting",
		start: "2024-09-03T10:30:00",
		end: "2024-09-03T11:00:00"
	});

	calendar.render();
});