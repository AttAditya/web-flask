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

function switch_mode(mode) {
	let containers_modes = [
		"void", "preview", "meta", "content", "publish"
	];

	containers_modes.forEach((v, i) => {
		if (!document.getElementById(`${v}-container`).classList.contains("is-hidden")) {
			document.getElementById(`${v}-container`).classList.add("is-hidden");
		}

		document.getElementById(`${v}-mode-button`).disabled = false;
	});

	document.getElementById(`${mode}-container`).classList.remove("is-hidden");
	document.getElementById(`${mode}-mode-button`).disabled = true;
}

function load_authors(authors_id) {
	fetch("/users/get", {
		method: "POST",
		headers: {
			"Content-Type": "application/json"
		},
		body: JSON.stringify(authors_id)
	}).then(req => req.json()).then(authors_data => {
		authors_data.data.forEach(author => {
			document.getElementById("article-authors").innerHTML = "";
			document.getElementById("article-authors").innerHTML += `
				<div class="column is-6">
					<a href="/user/${author.id}" class="box columns p-4 is-mobile">
						<div class="column is-2 p-0">
							<img src="${author.data.img}" alt="${author.id}" width="100%" height="auto" style="border-radius: 100%; aspect-ratio: 1 / 1; object-fit: cover;">
						</div>
						<div class="column is-10 py-0">
							<div class="content">
								<div class="title">
									${author.data.name}
								</div>
								<div class="subtitle">
									${author.id}
								</div>
							</div>
						</div>
					</a>
				</div>
			`;
		});
	});
}

function preview_load() {
	let art_content = tinymce.get("art-content-editor").getContent();
	document.getElementById("content").innerHTML = art_content ? art_content : `
		<span class="is-size-7 has-text-weight-semibold">
			(Please use content editor to add content)
		</span>
	`;

	load_authors(document.getElementById("article-authors-input").value.split(","));
}

async function send_article() {
	let btn = document.getElementById("final-submit-button");
	btn.classList.add("is-loading");

	let data = {
		name: document.getElementById("article-name-input").value,
		content: tinymce.get("art-content-editor").getContent(),
		thumbnail: document.getElementById("article-thumbnail-src").value,
		tags: document.getElementById("article-tags-input").value.replaceAll(" ", "-").toLowerCase().split(","),
		authors: document.getElementById("article-authors-input").value.replaceAll(" ", "-").split(",")
	}

	if (!data.name) {
		switch_mode("meta");
		toast_notify("Name required!", "danger");
		btn.classList.remove("is-loading");
		return
	}
	if (!data.content) {
		switch_mode("content");
		toast_notify("Content required!", "danger");
		btn.classList.remove("is-loading");
		return
	}
	if (!data.thumbnail) {
		switch_mode("meta");
		toast_notify("Thumbnail required!", "danger");
		btn.classList.remove("is-loading");
		return
	}
	if (!data.tags[0]) {
		switch_mode("meta");
		toast_notify("Tags required!", "danger");
		btn.classList.remove("is-loading");
		return
	}
	if (!data.authors[0]) {
		switch_mode("meta");
		toast_notify("Authors required!", "danger");
		btn.classList.remove("is-loading");
		return
	}

	await fetch(`/upload/article`, {
		method: "POST",
		headers: {
			"Content-Type": "application/json"
		},
		body: JSON.stringify(data)
	}).then(req => req.json()).then(res => {
		if (res.status != 200) {
			toast_notify(res.msg, "danger");
			btn.classList.remove("is-loading");
		} else {
			toast_notify("Article Created!", "success")
			location.href = `/article/${res.id}`;
			btn.classList.remove("is-loading");
		}
	}).catch((_error_) => {
		toast_notify("Server not connecting... Article not published...", "danger");
		btn.classList.remove("is-loading");
		fetch("/errors/post", {
			method: "POST",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify([String(_error_)])
		})
	});
}

