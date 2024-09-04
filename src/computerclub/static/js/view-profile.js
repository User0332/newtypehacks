const userID = new URLSearchParams(location.search).get("id");

execWithUserData((selfUserData) => {
	if (selfUserData.id == userID) location.href = "/self-profile";
})

getUserInfo(userID).then((userData) => {
	const greeting = document.getElementById("greeting");
	const userEmailElem = document.getElementById("user-email");

	greeting.textContent = `${userData.name}'s Profile`;

	const email = userData.email;

	userEmailElem.textContent = `${userData.name}'s email: ${email}`;
})