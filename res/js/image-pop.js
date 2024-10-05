function img_pop_load() {
	Array.from(document.querySelectorAll(".content > p > img, .content > img")).forEach(i => {
		i.addEventListener("click", () => {
			window.open(i.src);
		});
	});
}