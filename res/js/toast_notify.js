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