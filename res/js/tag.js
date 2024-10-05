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

function create_card(data) {
	return `
		<div class="column is-full">
			<a href="/a/${data.id}" class="box columns m-2 mb-1">
				<div class="column">
					<img src="${data.thumbnail}" alt="${data.name}" loading="lazy" onerror="this.src='${data.thumbnail}';" style="aspect-ratio: 1200/628; object-fit: contain;">
				</div>
				<div class="divider is-vertical is-danger">
					<i class="fa-solid fa-newspaper fa-lg has-text-black"></i>
				</div>
				<div class="column">
					<div class="content">
						<h1 class="title is-size-2" style="overflow: hidden; text-overflow: ellipsis; -webkit-line-clamp: 2; display: -webkit-box; -webkit-box-orient: vertical;">
							${data.name}
						</h1>
						<h2 class="subtitle is-size-6 mb-1" id="${data.id}-authors">
							By ${data.authors}
						</h2>
						<h2 class="subtitle is-size-6 mt-1 mb-2">
							Published on ${data.date} UTC
						</h2>
						<div class="tags p-0 m-0" id="${data.id}-tags">
							${data.tags.map(i => "<span class='tag m-0'>" + i + "</span>")}
						</div>
					</div>
				</div>
			</a>
		</div>
	`;
}

function display_data(data, tagname) {
	for (let article_data of data[tagname]) {
		document.getElementById("tagged").innerHTML += create_card(article_data);
	}
}

async function load(tagname) {
	let topics = {}
	topics[tagname] = 15

	await fetch(`/articles/meta`, {
		method: "POST",
		headers: {
			"Content-Type": "application/json"
		},
		body: JSON.stringify(topics)
	}).then(req => req.json()).then(res => {
		if (res.status != 200) {
			toast_notify(res.msg, "danger");
		}
		
		display_data(res, tagname);
	}).catch(_error_ => {
		toast_notify("Could not load articles! Server not connecting...", "danger");
	});
}

