const userID = new URLSearchParams(location.search).get("id");

getUserInfo(userID).then((userData) => {
	const greeting = document.getElementById("greeting");
	const userEmailElem = document.getElementById("user-email");

	greeting.textContent = `Welcome to your profile, ${userData.name}`;

	const email = authInfo.user.email;

	userEmailElem.textContent = `Your Email: ${email}`;
})

execWithUserData((selfUserData) => {
	if (selfUserData.id == userID) location.href = "/self-profile";
})