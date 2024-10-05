function share_this_page() {
	if (navigator.share) {
		navigator.share({
			title: document.title,
			url: location.href
		}).then(() => {
			toast_notify("Thanks for sharing!", "success");
		}).catch(_error_ => {
			toast_notify("Could not share!", "danger");
		});
	} else {
		toast_notify("Sorry, this specific button, is not supported by your device...", "warning")
	}
}

function whatsapp_share() {
	let url = "whatsapp://send?text=";
	url += encodeURIComponent(`Check out this article from The World Times!\n${document.title}\n${location.href}`);

	let a_el = document.createElement("a");
	a_el.target = "_blank";
	a_el.rel = "noopener noreferrer";
	a_el.href = url;

	a_el.click();
}

function facebook_share() {
	let url = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(location.href)}&amp;src=sdkpreparse`;

	let a_el = document.createElement("a");
	a_el.target = "_blank";
	a_el.rel = "noopener noreferrer";
	a_el.href = url;

	a_el.click();
}

function twitter_share() {
	let url = "https://twitter.com/intent/tweet?text=";
	url += encodeURIComponent(`Check out this article from The World Times!\n${document.title}\n${location.href}`);

	let a_el = document.createElement("a");
	a_el.target = "_blank";
	a_el.rel = "noopener noreferrer";
	a_el.href = url;

	a_el.click();
}

