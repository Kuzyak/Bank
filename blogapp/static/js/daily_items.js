var CURRENT_DATE = null;

$(function() {
	$("#datepicker").datepicker("option", "onSelect", function() { AjaxShowCurrentDateDailyItem(); });
	
	//Set date of last daily item
	var lastDailyItemDate = $("#daily_item").attr("currentDate");
	$("#datepicker").datepicker("option", "dateFormat", "yy-mm-dd");
	$("#datepicker").datepicker('setDate', lastDailyItemDate);
	$("#datepicker").datepicker("option", "dateFormat", "dd MM yy");
	CURRENT_DATE = $("#datepicker").datepicker("getDate");
	
	// Next Day Link
	$('a#next').click(function () {
		/*
		var $picker = $("#datepicker");
		var date=new Date($picker.datepicker('getDate'));
		
		var nextDate = $("#daily_item").attr("nextDate");
		if (nextDate.length) {
			$picker.datepicker("option", "dateFormat", "yy-mm-dd");
			$picker.datepicker("setDate", nextDate);
			$picker.datepicker("option", "dateFormat", "dd MM yy");
		} else {
			return false;
		}
		
		
		var newDate = $picker.datepicker("getDate");
		var today = new Date();
		if (newDate.getYear() == today.getYear() && newDate.getMonth() == today.getMonth() && newDate.getDate() >= today.getDate()) {
			$("#next").removeClass("a").addClass("i");
		}
		*/
		
		if ($(this).hasClass("a")) {
			AjaxNextDailyItem();
		}
		
		return false;
	});

	// Previous Day Link
	$('a#prev').click(function () {
		/*
		var $picker = $("#datepicker");
		var date=new Date($picker.datepicker('getDate'));
		
		var prevDate = $("#daily_item").attr("prevDate");
		if (prevDate.length) {
			$picker.datepicker("option", "dateFormat", "yy-mm-dd");
			$picker.datepicker("setDate", prevDate);
			$picker.datepicker("option", "dateFormat", "dd MM yy");
		} else {
			return false;
		}
		
		var newDate = $picker.datepicker("getDate");
		var today = new Date();
		if (newDate < today) {
			$("#next").removeClass("i").addClass("a");
		}
		*/
		
		if ($(this).hasClass("a")) {
			AjaxPrevDailyItem();
		}
		
		return false;
	});
});		



/**
 * Загрузка предыдущего элемента.
 */
function AjaxPrevDailyItem() {
	var currentDailyItemId = $("#daily_item").attr("item_id");
	$(".ajax-loader").show();
	$.ajax({
		type: "POST",
		url: "ajax/daily_items/get_prev_item/" + currentDailyItemId,
		success: function(response) {
			$("#daily_item").replaceWith(response);
			$(".ajax-loader").hide();
			UpdateArrows();
			
			
			/*
			var prevDate = $("#daily_item").attr("prevDate");
			if (!prevDate.length) {
				$("#prev").removeClass("a").addClass("i");
			}
			CURRENT_DATE = $("#datepicker").datepicker("getDate");
			*/
		}		
	});
}

/**
 * Загрузка следующего элемента.
 */
function AjaxNextDailyItem() {
	var currentDailyItemId = $("#daily_item").attr("item_id");
	$(".ajax-loader").show();
	$.ajax({
		type: "POST",
		url: "ajax/daily_items/get_next_item/" + currentDailyItemId,
		success: function(response) {
			$("#daily_item").replaceWith(response);
			$(".ajax-loader").hide();
			UpdateArrows();
			
			/*
			$("#prev").removeClass("i").addClass("a");
			CURRENT_DATE = $("#datepicker").datepicker("getDate");
			*/
		}		
	});
}

/**
 * Загружает элемент в зависимости от текущей выбранной даты
 */
function AjaxShowCurrentDateDailyItem() {
	$("#datepicker").datepicker("option", "dateFormat", "yy-mm-dd");
	var currentDate = $("#datepicker").val();
	$("#datepicker").datepicker("option", "dateFormat", "dd MM yy");

	$.ajax({
		type: "POST",
		url: "ajax/daily_items/get_item_by_date/" + currentDate,
		success: function(response) {
			if (!response.length) {
				/* 
				 * Если возвращен пустой результат значит элемент за эту дату отсутствует, 
				 * возвращаем предыдущую активную дату.
				 */
				$("#datepicker").datepicker("setDate", CURRENT_DATE);
			} else {
				// Если элемент есть, вставляем его в страницу.
				$("#daily_item").replaceWith(response);
				CURRENT_DATE = $("#datepicker").datepicker("getDate");
			}
		}
	});
}



function UpdateArrows() {
	var hasPrev = parseInt($("[name='hasPrev']").val());
	if (hasPrev) {
		$("#prev").removeClass("i").addClass("a");
	} else {
		$("#prev").removeClass("a").addClass("i");
	}
	
	var hasNext = parseInt($("[name='hasNext']").val());
	if (hasNext) {
		$("#next").removeClass("i").addClass("a");
	} else {
		$("#next").removeClass("a").addClass("i");
	}
}








