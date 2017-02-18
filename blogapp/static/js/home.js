$(function() {
	$("#news-blog-tabs a").click(function(e) {
		e.preventDefault();
		$("#news-blog-tabs li").removeClass("active");
		$(this).parent().addClass("active");

		$(".feed").hide();
		$($(this).attr("href")).fadeIn();
	});

	$(".tab_content").each(function() {
		// Comma to point
		var bnmValue = $.trim($(this).find("ins:first span").text());
		bnmValue = bnmValue.replace(/,/g, ".");
		bnmValue = parseFloat(bnmValue);

		// Курсы валют каждого банка в массив (купля / продажа)
		var buying = new Array();
		var selling = new Array();
		$(this).find(".table .tr:gt(0)").each(function() {
			var b = $(this).find(".td.b").text();
			var c = $(this).find(".td.c").text();
		
			buying.push(b);
			selling.push(c);
		});
		
		if ($(this).attr("id") == "tab4") {
			decimals = 3; // rub
		} else {
			decimals = 2;
		}
		
		closestBuying = getBestBuying(buying, decimals);
		closestSelling = getBestSelling(selling, decimals);
		
		$(this).find(".table .tr:gt(0)").each(function() {
			var b = $(this).find(".td.b").text();
			var c = $(this).find(".td.c").text();

			
			if (b.search(closestBuying) != -1) {
				$(this).find(".td.b").addClass("best");
			}
			
			if (c.search(closestSelling) != -1) {
				$(this).find(".td.c").addClass("best");
			}
		});
	});
	
	// Сортировка валютных курсов по выгодности обмена.
	$(".tab_container .th.b").click(function(e) {
		e.preventDefault();
		if ($(this).attr("sorted")) return false;
		
		$(".tab_container .th").removeAttr("sorted");
		$(this).attr("sorted", true);
		var divId = $(this).parent().parent().parent().attr("id");
		$("#"+divId+" .table .tr:gt(0)").tsort(".td.b", {order: "desc"});
	});
	$(".tab_container .th.c").click(function(e) {
		e.preventDefault();
		if ($(this).attr("sorted")) return false;
		
		$(".tab_container .th").removeAttr("sorted");
		$(this).attr("sorted", true);
		var divId = $(this).parent().parent().parent().attr("id");
		$("#"+divId+" .table .tr:gt(0)").tsort(".td.c", {order: "asc"});
		downEmptyRates(divId);
	});
	
});


/**
 * При сортировке, данная функци яставит последними в списке банки, у которых не указан валютный курсы.
 * @param divId
 */
function downEmptyRates(divId) {
	var selector = "#" + divId;
	
	$(selector).find(".tr:gt(0)").each(function() {
		var t = $(this).find(".td.c").text();
		t = $.trim(t);
		var l = t.length;
		
		if (l <= 1) {
			$(this).insertAfter($(selector).find(".tr:last"));
		}
	});
}











