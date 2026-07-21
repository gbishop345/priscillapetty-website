/*
 * RapidWeaver 3.5.0 theme functions.
 * Script Version 2.1
 * Updated 26 May 2006.
 * Flash/QuickTime helpers removed — site uses HTML5 video.
 */



/*
 * Function to generate "open in new window" link as W3C compliant
 */

function externalLinks() {
if (!document.getElementsByTagName) return; 
var anchors = document.getElementsByTagName("a"); 
for (var i=0; i<anchors.length; i++) { 
var anchor = anchors[i]; 
if (anchor.getAttribute("href") && 
anchor.getAttribute("rel") == "external") 
anchor.target = "_blank";
} 
} 
window.onload = externalLinks;


/*
 * Responsive navigation for modern mobile browsers.
 * Desktop DOM and layout are left unchanged.
 */
(function () {
	var sidebar;
	var navigation;
	var button;
	var mobileViewport;
	var active = false;

	function closeMenu() {
		if (!sidebar) {
			return;
		}
		sidebar.classList.remove("nav-open");
		if (button) {
			button.setAttribute("aria-expanded", "false");
		}
	}

	function onToggleClick() {
		var isOpen = sidebar.classList.toggle("nav-open");
		button.setAttribute("aria-expanded", isOpen ? "true" : "false");
	}

	function onNavigationClick(event) {
		if (event.target.closest && event.target.closest("a")) {
			closeMenu();
		}
	}

	function onDocumentKeydown(event) {
		if (event.key === "Escape" && sidebar.classList.contains("nav-open")) {
			closeMenu();
			button.focus();
		}
	}

	function enableMobileNavigation() {
		if (active) {
			return;
		}

		sidebar = document.getElementById("sidebarContainer");
		navigation = document.getElementById("navcontainer");
		if (!sidebar || !navigation) {
			return;
		}

		var navigationId = navigation.id || "navcontainer";
		navigation.id = navigationId;

		button = document.createElement("button");
		button.type = "button";
		button.className = "mobile-nav-toggle";
		button.setAttribute("aria-controls", navigationId);
		button.setAttribute("aria-expanded", "false");
		button.appendChild(document.createTextNode("Menu"));
		sidebar.insertBefore(button, navigation);
		document.body.classList.add("mobile-nav-enabled");

		button.addEventListener("click", onToggleClick);
		navigation.addEventListener("click", onNavigationClick);
		document.addEventListener("keydown", onDocumentKeydown);

		active = true;
		closeMenu();
	}

	function disableMobileNavigation() {
		if (!active) {
			return;
		}

		closeMenu();
		document.body.classList.remove("mobile-nav-enabled");

		if (button) {
			button.removeEventListener("click", onToggleClick);
			if (button.parentNode) {
				button.parentNode.removeChild(button);
			}
			button = null;
		}

		if (navigation) {
			navigation.removeEventListener("click", onNavigationClick);
		}

		document.removeEventListener("keydown", onDocumentKeydown);
		active = false;
	}

	function syncMenuState(event) {
		if (event.matches) {
			enableMobileNavigation();
		} else {
			disableMobileNavigation();
		}
	}

	function initMobileNavigation() {
		mobileViewport = window.matchMedia("(max-width: 768px)");
		syncMenuState(mobileViewport);
		if (mobileViewport.addEventListener) {
			mobileViewport.addEventListener("change", syncMenuState);
		} else if (mobileViewport.addListener) {
			mobileViewport.addListener(syncMenuState);
		}
	}

	if (document.readyState === "loading") {
		document.addEventListener("DOMContentLoaded", initMobileNavigation);
	} else {
		initMobileNavigation();
	}
}());


/*
 * External Play/Pause control for HTML5 video.
 * Keeps the native control overlay off the clip itself.
 */
(function () {
	function syncButton(button, video) {
		var playing = !video.paused && !video.ended;
		button.textContent = playing ? "Pause" : "Play";
		button.setAttribute("aria-pressed", playing ? "true" : "false");
		button.setAttribute("aria-label", playing ? "Pause video" : "Play video");
	}

	function enhanceVideo(video) {
		if (video.closest(".video-player")) {
			return;
		}

		video.removeAttribute("controls");
		video.setAttribute("controlsList", "nodownload");

		var wrapper = document.createElement("div");
		wrapper.className = "video-player";

		var button = document.createElement("button");
		button.type = "button";
		button.className = "video-play-toggle";
		syncButton(button, video);

		var media = document.createElement("div");
		media.className = "video-player-media";

		var parent = video.parentNode;
		parent.insertBefore(wrapper, video);
		wrapper.appendChild(button);
		wrapper.appendChild(media);
		media.appendChild(video);

		button.addEventListener("click", function () {
			if (video.paused || video.ended) {
				var playPromise = video.play();
				if (playPromise && typeof playPromise.catch === "function") {
					playPromise.catch(function () {
						syncButton(button, video);
					});
				}
			} else {
				video.pause();
			}
		});

		video.addEventListener("play", function () {
			syncButton(button, video);
		});
		video.addEventListener("pause", function () {
			syncButton(button, video);
		});
		video.addEventListener("ended", function () {
			syncButton(button, video);
		});
	}

	function initVideoPlayers() {
		var videos = document.querySelectorAll("video");
		for (var i = 0; i < videos.length; i++) {
			enhanceVideo(videos[i]);
		}
	}

	function initClipLists() {
		var containers = document.querySelectorAll(".stacks_in");
		for (var i = 0; i < containers.length; i++) {
			var el = containers[i];
			if (el.querySelector('a[href*="/videos/"]')) {
				el.classList.add("clip-list");
			}
		}
	}

	function initMediaEnhancements() {
		initVideoPlayers();
		initClipLists();
	}

	if (document.readyState === "loading") {
		document.addEventListener("DOMContentLoaded", initMediaEnhancements);
	} else {
		initMediaEnhancements();
	}
}());
