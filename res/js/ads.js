async function display_ad(root_element) {
	await fetch("/ad/get").then(req => req.json()).then(ad_data => {
		root_element.outerHTML = `
			<a class="box m-4" href="${ad_data.link}" target="_blank" rel="noopener noreferrer">
				<i class="fa-solid fa-rectangle-ad m-0 p-0 has-text-black"></i>
				<img src="${ad_data.img}" alt="${ad_data.text}" width="100%" class="m-0 p-0">
				<span class="p-0 m-0 is-size-7 has-text-weight-bold has-text-black">${ad_data.text}</span>
			</a>
		`;
	});
}

function setup_ads() {
	document.getElementById("ads").outerHTML = `
		<div class="column is-3" style="pointer-events: none;"></div>
		<div id="ads" class="column is-3 is-hidden-mobile" style="height: 100%; max-height: 100%; overflow-y: hidden; position: fixed; right: 0;">
			<div class="box m-4"><button class="button is-white is-fullwidth is-loading m-0 p-0"></button><img class="is-hidden" src="/does-not-exists" onerror="display_ad(this.parentElement);"><span class="has-text-black has-text-weight-bold p-0 m-0">Slot available for advertising.</span></div>
			<div class="box m-4"><button class="button is-white is-fullwidth is-loading m-0 p-0"></button><img class="is-hidden" src="/does-not-exists" onerror="display_ad(this.parentElement);"><span class="has-text-black has-text-weight-bold p-0 m-0">Slot available for advertising.</span></div>
			<div class="box m-4"><button class="button is-white is-fullwidth is-loading m-0 p-0"></button><img class="is-hidden" src="/does-not-exists" onerror="display_ad(this.parentElement);"><span class="has-text-black has-text-weight-bold p-0 m-0">Slot available for advertising.</span></div>
			<div class="box m-4"><button class="button is-white is-fullwidth is-loading m-0 p-0"></button><img class="is-hidden" src="/does-not-exists" onerror="display_ad(this.parentElement);"><span class="has-text-black has-text-weight-bold p-0 m-0">Slot available for advertising.</span></div>
			<div class="box m-4"><button class="button is-white is-fullwidth is-loading m-0 p-0"></button><img class="is-hidden" src="/does-not-exists" onerror="display_ad(this.parentElement);"><span class="has-text-black has-text-weight-bold p-0 m-0">Slot available for advertising.</span></div>
			<div class="box m-4"><button class="button is-white is-fullwidth is-loading m-0 p-0"></button><img class="is-hidden" src="/does-not-exists" onerror="display_ad(this.parentElement);"><span class="has-text-black has-text-weight-bold p-0 m-0">Slot available for advertising.</span></div>
			<div class="box m-4"><button class="button is-white is-fullwidth is-loading m-0 p-0"></button><img class="is-hidden" src="/does-not-exists" onerror="display_ad(this.parentElement);"><span class="has-text-black has-text-weight-bold p-0 m-0">Slot available for advertising.</span></div>
			<div class="box m-4"><button class="button is-white is-fullwidth is-loading m-0 p-0"></button><img class="is-hidden" src="/does-not-exists" onerror="display_ad(this.parentElement);"><span class="has-text-black has-text-weight-bold p-0 m-0">Slot available for advertising.</span></div>
			<div class="box m-4"><button class="button is-white is-fullwidth is-loading m-0 p-0"></button><img class="is-hidden" src="/does-not-exists" onerror="display_ad(this.parentElement);"><span class="has-text-black has-text-weight-bold p-0 m-0">Slot available for advertising.</span></div>
			<div class="box m-4"><button class="button is-white is-fullwidth is-loading m-0 p-0"></button><img class="is-hidden" src="/does-not-exists" onerror="display_ad(this.parentElement);"><span class="has-text-black has-text-weight-bold p-0 m-0">Slot available for advertising.</span></div>
		</div>
		<div class="column is-hidden-desktop">
			<h1 class="title">Sponsors of The World Times</h1>
			<div class="box m-4"><button class="button is-white is-fullwidth is-loading m-0 p-0"></button><img class="is-hidden" src="/does-not-exists" onerror="display_ad(this.parentElement);"><span class="has-text-black has-text-weight-bold p-0 m-0">Slot available for advertising.</span></div>
			<div class="box m-4"><button class="button is-white is-fullwidth is-loading m-0 p-0"></button><img class="is-hidden" src="/does-not-exists" onerror="display_ad(this.parentElement);"><span class="has-text-black has-text-weight-bold p-0 m-0">Slot available for advertising.</span></div>
			<div class="box m-4"><button class="button is-white is-fullwidth is-loading m-0 p-0"></button><img class="is-hidden" src="/does-not-exists" onerror="display_ad(this.parentElement);"><span class="has-text-black has-text-weight-bold p-0 m-0">Slot available for advertising.</span></div>
			<div class="box m-4"><button class="button is-white is-fullwidth is-loading m-0 p-0"></button><img class="is-hidden" src="/does-not-exists" onerror="display_ad(this.parentElement);"><span class="has-text-black has-text-weight-bold p-0 m-0">Slot available for advertising.</span></div>
			<div class="box m-4"><button class="button is-white is-fullwidth is-loading m-0 p-0"></button><img class="is-hidden" src="/does-not-exists" onerror="display_ad(this.parentElement);"><span class="has-text-black has-text-weight-bold p-0 m-0">Slot available for advertising.</span></div>
			<div class="box m-4"><button class="button is-white is-fullwidth is-loading m-0 p-0"></button><img class="is-hidden" src="/does-not-exists" onerror="display_ad(this.parentElement);"><span class="has-text-black has-text-weight-bold p-0 m-0">Slot available for advertising.</span></div>
			<div class="box m-4"><button class="button is-white is-fullwidth is-loading m-0 p-0"></button><img class="is-hidden" src="/does-not-exists" onerror="display_ad(this.parentElement);"><span class="has-text-black has-text-weight-bold p-0 m-0">Slot available for advertising.</span></div>
			<div class="box m-4"><button class="button is-white is-fullwidth is-loading m-0 p-0"></button><img class="is-hidden" src="/does-not-exists" onerror="display_ad(this.parentElement);"><span class="has-text-black has-text-weight-bold p-0 m-0">Slot available for advertising.</span></div>
			<div class="box m-4"><button class="button is-white is-fullwidth is-loading m-0 p-0"></button><img class="is-hidden" src="/does-not-exists" onerror="display_ad(this.parentElement);"><span class="has-text-black has-text-weight-bold p-0 m-0">Slot available for advertising.</span></div>
			<div class="box m-4"><button class="button is-white is-fullwidth is-loading m-0 p-0"></button><img class="is-hidden" src="/does-not-exists" onerror="display_ad(this.parentElement);"><span class="has-text-black has-text-weight-bold p-0 m-0">Slot available for advertising.</span></div>
		</div>
	`;
	
	let scroll_index = 0;
	setInterval(() => {
		let ads_scroller = document.getElementById("ads");
		let scroll_count = ads_scroller.scrollHeight / innerHeight;

		ads_scroller.scrollTo({
			top: scroll_index * innerHeight,
			left: 0,
			behavior: "smooth"
		});

		scroll_index += 1;
		if (scroll_index > scroll_count) {
			scroll_index = 0;
		}
	}, 5000);
}

