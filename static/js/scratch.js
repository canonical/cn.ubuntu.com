

//Provides basic templating for strings: TODO: Find a home for this
String.prototype.format = function() {
	var args = arguments;
	return this.replace(/{(\d+)}/g, function(match, number) {
		return typeof args[number] != 'undefined'
			? args[number]
			: match
		;
	});
};

YUI().use('node', 'gallery-carousel', 'gallery-carousel-anim', 'substitute', 'cookie', "event-resize", "transition", "event", function(Y) {

core.setupHtmlClass = function() {
	Y.all('html').removeClass('no-js').addClass('yes-js');
}

core.resizeListener = function() {
	Y.on('windowresize', function(e) {
		core.redrawGlobal();
	});
	core.globalInit();
};

	core.setupAnimations = function(){
		var yOffset = 150;
		if(Y.one('body').hasClass('phone') || Y.one('body').hasClass('phone-scopes')){
			var searchScreen = false;
			var edgeMagic = Y.all('.edge-magic');
			if(Y.one('.search-screen')){
				var searchScreen = {ypos: Y.one('.search-screen').getXY()[1] - yOffset, run: false};
			}
			Y.on('scroll', function(e) {
				 edgeMagic.each(function (node) {
					if(window.scrollY > node.getXY()[1] - yOffset && window.scrollY < node.getXY()[1] && !node.run){
						node.run = true;
						node.one('.slider-animation').addClass('run');
						if(node.one('.slider-animation').getAttribute('class') == 'slider-animation full-swipe run'){
							setTimeout(function(){ node.one('.launcher').addClass('return') }, 2000);
						}
					}
				});
			});
			if(searchScreen) {
				if(window.scrollY > searchScreen.ypos && window.scrollY < searchScreen.ypos + yOffset && !searchScreen.run){
					searchScreen.run = true;
					core.runAnimation('search-screen');
				}else{
					Y.on('scroll', function(e) {
						 if(window.scrollY > searchScreen.ypos && window.scrollY < searchScreen.ypos + yOffset && !searchScreen.run){
						 	searchScreen.run = true;
						 	core.runAnimation('search-screen');
						 }
					});
				}
			}

			Y.all('.replay').on('click', function(e){
				core.rerunAnimation(e.target.get('parentNode').one('.slider-animation').getAttribute('class').replace('slider-animation ','').replace(' run',''));
			});
			if(Y.one('.content-controls .gallery-screen')){
				Y.one('.content-controls .gallery-screen').setStyle('display','block');
				var infoIndex = 0;
				setInterval(function(){
					Y.all('.infographic .main-image').addClass('hide');
					Y.one('.infographic .info-pic-'+infoIndex).removeClass('hide');
					if(++infoIndex > 4){ infoIndex = 0; }
				}, 4000);
			}
		}

		if(Y.one('body').hasClass('tablet')){
			var edgeMagic = Y.all('.slider-animation');
			var videoPanel = Y.all('.the-video');
			Y.on('scroll', function(e) {
				 edgeMagic.each(function (node) {
					if(window.scrollY > node.getXY()[1] - yOffset && window.scrollY < node.getXY()[1] && !node.run){
						node.run = true;
						node.addClass('run');
					}
				});
			});

			Y.all('.screen').on('click', function(e){
				core.rerunAnimation(e.target.get('parentNode').get('parentNode').get('parentNode').one('.slider-animation').getAttribute('class').replace('slider-animation ','').replace(' run',''));
			});

			Y.all('.replay').on('click', function(e){
				core.rerunAnimation(e.target.get('parentNode').one('.slider-animation').getAttribute('class').replace('slider-animation ','').replace(' run',''));
			});
			if(Y.one('.show-video')){
				Y.one('.show-video').on('click',function(e) {
					e.preventDefault();
					videoPanel.addClass('show');
					Y.one('.row-hero').setStyle('height','590px');
					Y.one('.the-video div').set('innerHTML','<iframe width="984" height="554" src="http://www.youtube.com/embed/h384z7Ph0gU?showinfo=0&vq=hd1080&rel=0&modestbranding=0&autoplay=1" frameborder="0" allowfullscreen></iframe>');
				});
			}
			if(Y.one('.close-video')){
				Y.one('.close-video').on('click',function(e) {
					e.preventDefault();
					videoPanel.removeClass('show');
					Y.one('.row-hero').setStyle('height','460px');
					Y.one('.the-video div').set('innerHTML','');
				});
			}
		}
	}

	core.runAnimation = function($anim) {
		switch($anim) {
			case 'search-screen':
				Y.one('.search-screen').addClass('run');
				setTimeout(function(){ Y.one('.search-screen').removeClass('run'); }, 2000);
			break;
			case 'go-back':
				Y.one('.go-back').addClass('run');
			break;
		}
	};

	core.updateSlider = function( $index ) {
	if($index >= 4){ $index = 0; }
	if($index <= -1){ $index = 3; }
	YUI().use('node', function(Y) {
		Y.one('.slide-container').setStyle('left','-'+(700 * $index)+'px');
		Y.all('.slider-dots li').removeClass('active');
		Y.all('.slider-dots li.pip-'+$index).addClass('active');
		Y.all('.slider-animation').removeClass('run');
		Y.one('.full-swipe .launcher').removeClass('return');
		switch($index+''){
			case '0':
				setTimeout(function(){ Y.one('.edge-magic').addClass('run'); }, 1200);
			break;
			case '1':
				setTimeout(function(){ Y.one('.full-swipe').addClass('run');}, 1200);
				setTimeout(function(){ Y.one('.full-swipe .launcher').addClass('return') }, 2000);
			break;
			case '2':
				setTimeout(function(){ Y.one('.go-back').addClass('run'); }, 1200);
			break;
			case '3':
				setTimeout(function(){ Y.one('.content-controls').addClass('run'); }, 1200);
			break;
		}
	});
	return $index;
	}

	core.rerunAnimation = function($type){
		Y.one('.'+$type).removeClass('run');
		if($type == 'full-swipe'){
			Y.one('.full-swipe .launcher').removeClass('return');
			setTimeout(function(){ Y.one('.full-swipe').addClass('run'); }, 400);
			setTimeout(function(){ Y.one('.full-swipe .launcher').addClass('return') }, 1400);
		}else if($type == 'notification-slider' || $type == 'search-screen'){
		  	Y.one('.'+$type).removeClass('run');
      		setTimeout(function(){ Y.one('.'+$type).addClass('run'); }, 1000);
      	}else if($type == 'slider-animation') {

		}else{
			Y.one('.'+$type).removeClass('run');
			setTimeout(function(){ Y.one('.'+$type).addClass('run'); }, 400);
		}
	}


core.globalInit= function() {
	if (document.documentElement.clientWidth < 768) {
		core.globalPrepend = 'div.legal';
		core.setupGlobalNav();
		//core.setupAdditionalInfo();
		Y.one('.nav-global-wrapper').insert('<h2>Ubuntu websites</h2>','before');
	} else if (document.documentElement.clientWidth >= 768) {
		core.globalPrepend = 'body';
		core.setupGlobalNav();
		//Y.all('#additional-info h2').setStyle('cursor', 'default');
	}
};

core.redrawGlobal = function() {
	var globalNav = Y.one("#nav-global");
	if (document.documentElement.clientWidth < 768 && core.globalPrepend != 'div.legal') {
		core.globalPrepend = 'div.legal';
		if (globalNav) {
			globalNav.remove();
			core.setupGlobalNav();
			//core.setupAdditionalInfo();
			Y.one('.nav-global-wrapper').insert('<h2>Ubuntu websites</h2>','before');
			Y.one('#nav-global h2').setStyle('cursor', 'pointer').append('<span></span>').on('click',function(e) {
				this.toggleClass('active');
				this.next('div').toggleClass('active');
			});
		}
	} else if (document.documentElement.clientWidth >= 768 && core.globalPrepend != 'body') {
		core.globalPrepend = 'body';
		if (globalNav) {
			globalNav.remove();
			core.setupGlobalNav();
		}
	}
};

core.setupAccordion = function() {
	Y.all('.row-project li').each(function(node) {
		node.one('h3').append('<span></span>');
		node.one('a').on('click',function(e) {
			e.preventDefault();
			this.toggleClass('active');
			this.next('div').toggleClass('active');
		});
	});
};

core.setupGlobalNavAccordion = function() {
	if(Y.one('#nav-global h2') !== null) {
		Y.one('#nav-global h2').setStyle('cursor', 'pointer').append('<span></span>').on('click',function(e) {
			this.toggleClass('active');
			this.next('div').toggleClass('active');
		});
	}
};

core.setupAdditionalInfo = function() {
	if(Y.one('#additional-info h2 span') === null) {
		Y.one('#additional-info h2').setStyle('cursor', 'pointer').append('<span></span>').on('click',function(e) {
			this.toggleClass('active');
			this.next('div').toggleClass('active');
		});
	}
};

core.mobileNav = function() {
	Y.one('.nav-primary').insert('<a id="menu" class="nav-toggle">☰</a>','before');
	Y.all('.nav-toggle').on('click', function(e) {
		Y.all('header nav ul').toggleClass('active');
		Y.all('.nav-primary').toggleClass('active');
	});
};

core.cookiePolicy = function() {
	function open() {
		YUI().use('node', function(Y) {
			Y.one('body').prepend('<div class="cookie-policy"><div class="wrapper"><a href="?cp=close" class="link-cta">Close</a><p>We use cookies to improve your experience. By your continued use of this site you accept such use. To change your settings please <a href="/privacy-policy#cookies">see our policy</a>.</p></div></div>');
			Y.one('footer.global .legal').addClass('has-cookie');
			Y.one('.cookie-policy .link-cta').on('click',function(e){
				e.preventDefault();
				close();
			});
		});
	}
	function close() {
		YUI().use('node', function(Y) {
			Y.one('.cookie-policy').setStyle('display','none');
			Y.one('footer.global .legal').removeClass('has-cookie');
			setCookie();
		});
	}
	function setCookie() {
		YUI().use('cookie', function (Y) {
			Y.Cookie.set("_cookies_accepted", "true", { expires: new Date("January 12, 2025") });
		});
	}
	if(Y.Cookie.get("_cookies_accepted") != 'true'){
		open();
	}
};

core.tabbedContent = function() {
	Y.all('.tabbed-content .accordion-button').on('click', function(e){
		e.preventDefault();
		e.target.get('parentNode').toggleClass('open');
	});
};

core.rssLoader = {
	"outputFeed" : function(el, jobType) {
		var element = document.getElementById(el);
		if (jobType === undefined) {
			jobType = '';
		} else {
			jobType = ' ' + jobType;
		}
		return function(result){
			if (!result.error){
				var output = '';
				var thefeeds = result.feed.entries;
				var spinner = document.getElementById('spinner');
				if(spinner !== null){
					spinner.style.display = 'none';
				}
				if(element.className.indexOf('with-total') != -1){
					output += '<li>We currently have '+thefeeds.length+jobType+' vacancies';
				}
				console.log(thefeeds);
				for (var i = 0; i < thefeeds.length; i++){
					output += '<li><a href="{0}">{1} &rsaquo;</a></li>'.format(thefeeds[i].link, thefeeds[i].title);
				}
				element.innerHTML = element.innerHTML + output;
				return output;
			}
		}
	},

	"getFeed" : function(url, numItems, el, jobType){
		var feedpointer = new google.feeds.Feed(url); //Google Feed API method
		console.log(numItems);
		if(numItems != null){
			feedpointer.setNumEntries(numItems); //Google Feed API method
		}else{
			feedpointer.setNumEntries(250); //Google Feed API method
		}
		feedpointer.load(this.outputFeed(el, jobType)); //Google Feed API method
	}
};

core.parallaxBackground = function() {
	var body = Y.one('html');
	if(window.devicePixelRatio < 1.5){
		Y.on('scroll', function(e) {
			body.setStyle('backgroundPosition', 'center ' + -window.scrollY * 0.5 + 'px');
		});
	}
};

core.homeAnimation = function() {
	if(Y.one('body').hasClass('home')){
		var anim = Y.one('.animation');
		if(anim != null) {
			anim.addClass('run');
		}
	}
};

core.svgFallback = function() {
	if (!Modernizr.svg || !Modernizr.backgroundsize) {
	 	Y.all("img[src$='.svg']").each(function(node) {
	 		node.setAttribute("src", node.getAttribute('src').toString().match(/.*\/(.+?)\./)[0]+'png');
	 	});
	}
};

core.socialLinks = function() {
	if (document.documentElement.clientWidth > 769) {
		Y.one('.list--social__item--wechat').on("click", function(e) {
			if(!Y.one('.list--social__item--wechat').hasClass('active')){ 
				e.preventDefault();
			}
			this.toggleClass('active');
		});
	}
};

core.scopesSlideshow = function() {

    if(Y.one('.row-slideshow')){
        var carousel = new Y.Carousel({
            boundingBox: "#carousel-container",
            contentBox: "#carousel-container > ul", 
            numVisible: 1, 
            autoPlayInterval: 3500,
            height: 480,
            width: 363
        });
        
        carousel.plug(Y.CarouselAnimPlugin,{animation:{speed: 0.8,effect: Y.Easing.easeOutStrong }});
        carousel.render(); 
        carousel.startAutoPlay();
    }
};


	core.setupAccordion();
	core.resizeListener();
	core.mobileNav();
	//core.cookiePolicy();
	core.socialLinks();
	core.setupGlobalNavAccordion();
	core.setupAnimations();
	core.setupHtmlClass();
	core.tabbedContent();
	core.parallaxBackground();
	core.homeAnimation();
	core.svgFallback();
	core.scopesSlideshow();
});
