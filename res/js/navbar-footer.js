var navbar = `
	<nav id="navbar" class="navbar is-primary is-fixed-top px-4" role="navigation" aria-label="main navigation">
		<div class="navbar-brand">
			<a href="/" class="navbar-item">
				<img src="/res/logo-transparent.png" alt="The World Times" style="padding: 5px 5px; background: white; box-sizing: content-box; border-radius: 10px; /* mix-blend-mode: screen; filter: brightness(100); */">
			</a>

			<a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" onclick="document.getElementById('navbar-menu').classList.toggle('is-active'); this.classList.toggle('is-active');">
				<span aria-hidden="true"></span>
				<span aria-hidden="true"></span>
				<span aria-hidden="true"></span>
			</a>
		</div>

		<div id="navbar-menu" class="navbar-menu">
			<div class="navbar-start">
				<a class="navbar-item has-text-weight-semibold" href="/">Home</a>
				<a class="navbar-item has-text-weight-semibold" href="/category/event">Highlights</a>
				<a class="navbar-item has-text-weight-semibold" href="/category/state">State</a>
				<a class="navbar-item has-text-weight-semibold" href="/category/fact">Facts</a>
				<!--a class="navbar-item has-text-weight-semibold" href="/category/sport">Sports</a-->
				<a class="navbar-item has-text-weight-semibold" href="/category/lifestyle">Lifestyle</a>
				<!--a class="navbar-item has-text-weight-semibold" href="/category/tech">Technology</a-->
				<a class="navbar-item has-text-weight-semibold" href="/category/business">Business</a>
				<a class="navbar-item has-text-weight-semibold" href="/category/politic">Politics</a>
				<a class="navbar-item has-text-weight-semibold" href="/category/entertainment">Entertainment</a>
			</div>

			<div class="navbar-end">
				<a target="_blank" rel="noopener noreferrer" class="navbar-item" ignore_href="https://www.instagram.com/theworldtimes.in/"><i class="fa-brands fa-instagram fa-xl"></i><span class="is-hidden-desktop ml-2">Instagram</span></a>
				<a target="_blank" rel="noopener noreferrer" class="navbar-item" ignore_href="https://twitter.com/worldtimes_in"><i class="fa-brands fa-twitter fa-xl"></i><span class="is-hidden-desktop ml-2">Twitter</span></a>
				<a target="_blank" rel="noopener noreferrer" class="navbar-item" ignore_href="https://www.facebook.com/people/The-World-Times/100093097914112/"><i class="fa-brands fa-facebook fa-xl"></i><span class="is-hidden-desktop ml-2">Facebook</span></a>
				<a target="_blank" rel="noopener noreferrer" class="navbar-item" href="mailto:info@theworldtimes.in"><i class="fa-solid fa-envelope fa-xl"></i><span class="is-hidden-desktop ml-2">E-Mail</span></a>
			</div>
		</div>
	</nav>
`;

var footer = `
	<footer id="footer" class="footer p-0 m-0 has-background-white-bis" style="z-index: 100;">
		<div class="container is-fullhd p-4" style="z-index: 100;">
			<div class="columns p-4">
				<div class="column">
					<div class="content">
						<img src="/res/logo-transparent.png" alt="The World Times" width="128px" height="128px">
						<br><br>
						<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png"></a>
						<br>
						Copyrights <a href="/">theworldtimes.in</a> (c) 2023 - All Rights Reserved, licensed under
						<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">
							CC 4.0 License
						</a>
					</div>
				</div>
				<div class="divider is-vertical is-black"></div>
				<div class="column">
					<div class="content">
						<h3 class="title">CONTACT US</h3>
						<div class="mb-2">
							<a target="_blank" rel="noopener noreferrer" href="https://www.instagram.com/theworldtimes.in/">
								<i class="fa-brands fa-instagram fa-xl"></i>
								<span class="ml-2 has-text-weight-semibold">
									Instagram
								</span>
							</a>
						</div>
						<div class="mb-2">
							<a target="_blank" rel="noopener noreferrer" href="https://twitter.com/worldtimes_in">
								<i class="fa-brands fa-twitter fa-xl"></i>
								<span class="ml-2 has-text-weight-semibold">
									Twitter
								</span>
							</a>
						</div>
						<div class="mb-2">
							<a target="_blank" rel="noopener noreferrer" href="https://www.facebook.com/people/The-World-Times/100093097914112/">
								<i class="fa-brands fa-facebook fa-xl"></i>
								<span class="ml-2 has-text-weight-semibold">
									Facebook
								</span>
							</a>
						</div>
						<div class="mb-2">
							<a target="_blank" rel="noopener noreferrer" href="mailto:info@theworldtimes.in">
								<i class="fa-solid fa-envelope fa-xl"></i>
								<span class="ml-2 has-text-weight-semibold">
									E-Mail
								</span>
							</a>
						</div>
					</div>
				</div>
				<div class="divider is-vertical is-black"></div>
				<div class="column">
					<div class="content">
						<h3 class="title">QUICK LINKS</h3>
						<a href="/dash">Dashboard</a><br>
						<a href="/policy/ads">Advertise with us</a><br>
						<a href="/policy">TAC &amp; Privacy Policy</a><br>
						<!--a href="/credits">Credits</a><br-->
					</div>
				</div>
			</div>
		</div>
	</footer>
`;

function load_navbar_footer() {
	document.getElementById("navbar").outerHTML = navbar;
	document.getElementById("footer").outerHTML = footer;
}

