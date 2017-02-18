$(function(){
	var
		jSitemapPopup = $("#sitemap-popup"),
		jSitemapContent = $("#sitemap-content");
	
	fixButtonsIe();

	
	jSitemapContent.detach();
	jSitemapPopup.find(".tooltip-reducer").html(jSitemapContent.html());
	jSitemapContent.remove();

	tooltip({
		link: "#sitemap-trigger",
		tooltip: jSitemapPopup,
		fixedContent: true,
		activeClass: "active",
		hash: "#sitemap",
		cookieName: "content_state"
	});
	
	sitemap();
	
	
	tooltip({
		link: "#bank-trigger",
		tooltip: "#bank-popup",
		fixedContent: true
	});

	
	function fixButtonsIe(){
		if ($.browser.msie) {
	        $(".navigation .gr-button").hover(
				function(){ $(this).css({ "z-index": 160, "zoom": 1 }); },
				function(){	$(this).removeAttr("style"); }
			);
	        $("#bank-trigger").mouseleave(function(){
	        	$(this).removeAttr("style").css({ "z-index": 140 });
	        });
		}
	}

});


function sitemap() {
	
	var
		jTabs,
		jTabContents,
		jPutGet;
	
	
	init();
	
	
	function init() {
		jTabs = $(".sitemap-tab");
		jTabContents = $(".sitemap-tab-content");
		jPutGet = jTabContents.filter(".sitemap-put-get");
		
		initSelected();
		attachEvents();
	}
	
	function initSelected() {
		var jSelectedTab = jTabs.filter(".selected:eq(0)");
		
		if (!jSelectedTab.length) {
			jSelectedTab = jTabs.eq(0).addClass("selected");
		}
		
		switchTab(jSelectedTab);
	}
	
	function attachEvents() {
		$(".tab-link").click(function(){
			var jTab = $(this).closest(".sitemap-tab");
			
			if (!jTab.hasClass("selected")) {
				jTabs.removeClass("selected");
				jTab.addClass("selected");
				
				switchTab(jTab);
			}

			return false;
		});		
	}
	
	function switchTab(jTab) {
		var
			sTabId = getSuffixClass(jTab, "s_"),
			jTabContent = jTabContents.filter(".s_" + sTabId);
		
		if (jTabContent.length) {
			jTabContents.addClass("hidden");
			
			// пока нету закладок "Взять" и "Положить", убираем
			// if (sTabId != "about") {
			// 	jPutGet.removeClass("hidden");
			// }
			
			jTabContent.removeClass("hidden");
		}

		$.eventBus.trigger("sitemap.tab-switch");
	}
	
}