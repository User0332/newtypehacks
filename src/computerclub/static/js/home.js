const authUrl = "https://4273616.propelauthtest.com";
const authClient = PropelAuth.createClient({ authUrl });
const getUserInfoRoute = "/api/get-self"
let authInfo;

async function getAuthInfo() {
	return await authClient.getAuthenticationInfoOrNull();
}

async function execWithUserData(func) {
	const authInfo = await getAuthInfo();

	if (!authInfo) return;

	const res = await fetch(
		getUserInfoRoute, {
			"headers": {
				Authorization: `Bearer ${authInfo.accessToken}`
			}
		}
	);
	
	const userData = await res.json();

	func(userData)
}

document.addEventListener("scroll", function() {
	const cards = document.querySelectorAll(".program-card");
	const screenPosition = window.innerHeight;

	for (const card of cards)
	{
		const cardPosition = card.getBoundingClientRect();

		if (cardPosition.top < screenPosition) {
			card.classList.add("slide-in");
		}
		else {
			card.classList.remove("slide-in")
		}
	}
});

execWithUserData(() => {

});