function tooltip(options){
	
	var
		jTooltip,
		jTooltipReducer,
		jTooltipContent,
		jTooltipHoverHelper,
		jTooltipPoint,
		sHash,
		sPrevHash,
		sCookieName,
		sSaved,
		defaultOptions = {
			link: ".tooltip-link",
			tooltip: "#main-tooltip"
		};
		


	init();
	
	
	function init(){
		options = $.extend({}, defaultOptions, options);
		
		jTooltip = $(options.tooltip);
		sHash = options.hash;
		sSaved = "";
		if (options.cookieName !== undefined){
			sCookieName = options.cookieName;
			sSaved = "#" + $.cookie(sCookieName);
		}
		
		jTooltipReducer = jTooltip.find(".tooltip-reducer");
		jTooltipHoverHelper = jTooltip.find(".tooltip-hover-helper");
		jTooltipPoint = jTooltip.find(".tooltip-point");
		
		attachEvents();
		
		if(sHash){
			jTooltip.find('a').click(function(){
				window.location.hash = sHash;
			});
		}
		if (window.location.hash == sHash)
			showTooltip();
	}
	
	
	function attachEvents(){
		if (options.showOnHover) {

			$(options.link)
				.mouseenter(linkTrigger)
				.mouseleave(hideTooltip)

		} else {
			$(options.link).click(linkTrigger);
			
			jTooltip.click(function(e){
				e.stopPropagation();
			})
			
			$.eventBus.bind("tooltip.global-open", hideTooltip);
		}
		
		jTooltip.find(".tooltip-close, .custom-close").click(hideTooltip);
	}
	
	
	function linkTrigger(e){

		if (!options.fixedContent) {
		
			var sTooltipId = tooltipId(this);
	
			jTooltipContent = null;
			
			if (sTooltipId) {
				jTooltipContent = $(".tooltip-content.t_" + sTooltipId);
			}

			if (jTooltipContent && jTooltipContent.length) {
				if(!options.showOnHover){
					e.stopPropagation();
				}
				
				insertNewContent();
				showTooltip(tooltipHolder(this), e.pageX);
			}
			
		}
		
		if (options.fixedContent){
			e.preventDefault();
			e.stopPropagation();
			
			if (!jTooltip.is(":visible")) {
				$.eventBus.trigger("tooltip.global-open");
				$(this).addClass(options.activeClass)
				showTooltip();
			} else {
				hideTooltip();				
			}
		}
	}
	
	function tooltipId(el){
		el = $(el);
		
		var sId = $.data(el, "tooltip");

		if (!sId) {
			sId = getSuffixClass(el, "t_");
			$.data(el, "tooltip", sId);
		}
		
		return sId;
	}
	
	function tooltipHolder(el){
		el = $(el);
		
		var
			sClass = "tooltip-holder",
			jHolder = el.find("." + sClass);
		
		if (jHolder.length == 0) {
			jHolder = $("<span />", { className: sClass });
			el.prepend(jHolder);
		}
		
		return jHolder;
	}
	
	
	function bindDocumentEvents(){
		$(document)
			.bind("click", documentClick)
			.bind("keyup", documentKeyup)
	}

	function unbindDocumentEvents(){
		$(document)
			.unbind("click", documentClick)
			.unbind("keyup", documentKeyup)
	}
	
	function documentClick(event) {
		if (!$(event.target).parents().filter(jTooltip).length) {
			hideTooltip();
		}
	}
	
	function documentKeyup(event) {
		var code = event.keyCode ? event.keyCode : event.which ? event.which : null;
		if (code == 27) {
			hideTooltip();
		} 
	}
	
	
	function insertNewContent(){
		jTooltipReducer.html(jTooltipContent.html());
	}

	
	function showTooltip(jHolder, pageX){
		if (!options.showOnHover) {
			bindDocumentEvents();
		}
		if (!options.fixedContent && jHolder.length) {
			jHolder.append(jTooltip);
		}
		
		if (options.showOnHover) {
			var
				pageWidth = document.documentElement.clientWidth;
				tooltipWidth = 425,
				tooltipPointPosition = 40;

			if (jHolder.offset().left + tooltipWidth >= pageWidth) {
				jTooltip.css("left", pageWidth - tooltipWidth - jHolder.offset().left)
				jTooltipPoint.css("left", Math.max(pageX - (pageWidth - tooltipWidth), 30));
			} else {
				jTooltipPoint.css("left", Math.max(pageX - jHolder.offset().left + 20, 30));
			}
			
			jTooltipHoverHelper.show();
			jTooltip.fadeIn(200);
		} else {
			jTooltip.show();
		}
		
	}
	
	function hideTooltip(){
		jTooltipHoverHelper.hide();
		unbindDocumentEvents();
		
		if (options.showOnHover) {
			jTooltip.removeAttr("style").hide();
		} else {
			jTooltip.fadeOut(200);
			if(sHash == window.location.hash && sSaved)
				window.location.hash = sSaved;
			
			$.eventBus.trigger("tooltip.global-close");
		}

		if (options.fixedContent && options.activeClass){
			$(options.link).removeClass(options.activeClass)
		}
		
	}
	
	return this;
}

$(function(){
	tooltip({ showOnHover: true });
});