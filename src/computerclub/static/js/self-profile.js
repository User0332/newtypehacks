execWithUserData((userData) => {
	const greeting = document.getElementById("greeting");
	const userEmailElem = document.getElementById("user-email");

	greeting.textContent = `Welcome to your profile, ${userData.name}`;

	const email = authInfo.user.email;

	userEmailElem.textContent = `Your Email: ${email}`;
})