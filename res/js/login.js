function toast_notify(content, class_type="warning") {
	let notify_area = document.getElementById("toasts");
	if (!notify_area) { console.log(`${class_type}: ${content}`); return }
	
	let notif_el = document.createElement("div");
	
	notif_el.id = `notification-${notify_area.children.length + 1}`;

	notif_el.classList.add("notification");
	notif_el.classList.add("box");
	notif_el.classList.add(`is-${class_type}`);
	notif_el.classList.add("p-2");
	notif_el.classList.add("m-2");
	notif_el.classList.add("pr-6");

	notif_el.innerHTML = "";
	notif_el.innerHTML += `<button class="delete" onclick="this.parentElement.classList.add('is-hidden');"></button>`;
	notif_el.innerHTML += content;

	notify_area.appendChild(notif_el);

	window.setTimeout(() => {
		notify_area.removeChild(notif_el);
	}, 5000);
}

async function login() {
	let btn = document.getElementById("btn");
	btn.classList.add("is-loading");

	let details = {
		userid: document.getElementById("userid").value,
		password: document.getElementById("password").value
	}

	if (!details.userid) {
		toast_notify("User ID required!", "danger");
		btn.classList.remove("is-loading");
		document.getElementById("userid").focus();
		return;
	}
	if (!details.password) {
		toast_notify("Password required!", "danger");
		btn.classList.remove("is-loading");
		document.getElementById("password").focus();
		return;
	}

	await fetch(`/user/in/check`, {
		method: "POST",
		headers: {
			"Content-Type": "application/json"
		},
		body: JSON.stringify(details)
	}).then(req => req.json()).then(res => {
		if (res.status != 200) {
			toast_notify(res.msg, "danger");
			btn.classList.remove("is-loading");
		} else {
			toast_notify("Signed In!", "success")
			location.href = `/dash`;
			btn.classList.remove("is-loading");
		}
	});
}

async function signup() {
	let btn = document.getElementById("btn");
	btn.classList.add("is-loading");

	let details = {
		name: document.getElementById("name").value,
		userid: document.getElementById("userid").value,
		password: document.getElementById("password").value,
		mail: document.getElementById("mail").value
	}

	if (!details.userid) {
		toast_notify("User ID required!", "danger");
		btn.classList.remove("is-loading");
		document.getElementById("userid").focus();
		return;
	}
	if (!details.password) {
		toast_notify("Password required!", "danger");
		btn.classList.remove("is-loading");
		document.getElementById("password").focus();
		return;
	}
	if (details.password.length < 8) {
		toast_notify("Password requires minimum of 8 characters!", "danger");
		btn.classList.remove("is-loading");
		document.getElementById("password").focus();
		return;
	}
	if (!details.name) {
		toast_notify("Name required!", "danger");
		btn.classList.remove("is-loading");
		document.getElementById("name").focus();
		return;
	}
	if (details.userid.length < 8) {
		toast_notify("User ID requires minimum of 8 characters!", "danger");
		btn.classList.remove("is-loading");
		document.getElementById("password").focus();
		return;
	}
	if (!details.mail) {
		toast_notify("E-Mail required!", "danger");
		btn.classList.remove("is-loading");
		document.getElementById("name").focus();
		return;
	}

	await fetch(`/user/new/check`, {
		method: "POST",
		headers: {
			"Content-Type": "application/json"
		},
		body: JSON.stringify(details)
	}).then(req => req.json()).then(res => {
		if (res.status != 200) {
			toast_notify(res.msg, "danger");
			btn.classList.remove("is-loading");
		} else {
			toast_notify("Signed In!", "success")
			location.href = `/dash`;
			btn.classList.remove("is-loading");
		}
	});
}

