var curEUR = curUSD = curRON = curRUB = curUAH = cursGBP = cursCHF = 0;
var cacheEUR = cacheUSD = cacheRON = cacheRUB = cacheUAH = cacheGBP = cacheCHF = 0;
var curMDL = 1;

$(function() {

	GetBNMRates();

	$("[name='converter-mdl']").keyup(function() {
		var val = $("[name='converter-mdl']").val();
		val = val.replace(/\,/g, ".");
		if (IsNumeric(val)) {
			calculateMDL();
		}
	});
	$("[name='converter-eur']").keyup(function() {
		var val = $("[name='converter-eur']").val();
		val = val.replace(/\,/g, ".");
		if (IsNumeric(val)) {
			calculateEUR();
		}
	});
	$("[name='converter-usd']").keyup(function() {
		var val = $("[name='converter-usd']").val();
		val = val.replace(/\,/g, ".");
		if (IsNumeric(val)) {
			calculateUSD();
		}
	});
	$("[name='converter-ron']").keyup(function() {
		var val = $("[name='converter-ron']").val();
		val = val.replace(/\,/g, ".");
		if (IsNumeric(val)) {
			calculateRON();
		}
	});
	$("[name='converter-rub']").keyup(function() {
		var val = $("[name='converter-rub']").val();
		val = val.replace(/\,/g, ".");
		if (IsNumeric(val)) {
			calculateRUB();
		}
	});
	$("[name='converter-uah']").keyup(function() {
		var val = $("[name='converter-uah']").val();
		val = val.replace(/\,/g, ".");
		if (IsNumeric(val)) {
			calculateUAH();
		}
	});
	$("[name='converter-gbp']").keyup(function() {
		var val = $("[name='converter-gbp']").val();
		val = val.replace(/\,/g, ".");
		if (IsNumeric(val)) {
			calculateGBP();
		}
	});
	$("[name='converter-chf']").keyup(function() {
		var val = $("[name='converter-chf']").val();
		val = val.replace(/\,/g, ".");
		if (IsNumeric(val)) {
			calculateCHF();
		}
	});

	$(".calculator input").focus(function() {
		$(".calculator div").removeClass("active");
		$(this).parent().addClass("active");
	});

	$("[name='converter-mdl']").val(1);
	calculateMDL();

	$("[name='converter-mdl']").focus(function() {
		cacheMDL = $(this).val();
		$(this).val("");
	});
	$("[name='converter-eur']").focus(function() {
		cacheEUR = $(this).val();
		$(this).val("");
	});
	$("[name='converter-usd']").focus(function() {
		cacheUSD = $(this).val();
		$(this).val("");
	});
	$("[name='converter-ron']").focus(function() {
		cacheRON = $(this).val();
		$(this).val("");
	});
	$("[name='converter-rub']").focus(function() {
		cacheRUB = $(this).val();
		$(this).val("");
	});
	$("[name='converter-uah']").focus(function() {
		cacheUAH = $(this).val();
		$(this).val("");
	});
	$("[name='converter-gbp']").focus(function() {
		cacheGBP = $(this).val();
		$(this).val("");
	});
	$("[name='converter-chf']").focus(function() {
		cacheCHF = $(this).val();
		$(this).val("");
	});

	$("[name='converter-mdl']").focusout(function() {
		if (!$.trim($(this).val()).length) $(this).val(cacheMDL);
	});
	$("[name='converter-eur']").focusout(function() {
		if (!$.trim($(this).val()).length) $(this).val(cacheEUR);
	});
	$("[name='converter-usd']").focusout(function() {
		if (!$.trim($(this).val()).length) $(this).val(cacheUSD);
	});
	$("[name='converter-ron']").focusout(function() {
		if (!$.trim($(this).val()).length) $(this).val(cacheRON);
	});
	$("[name='converter-rub']").focusout(function() {
		if (!$.trim($(this).val()).length) $(this).val(cacheRUB);
	});
	$("[name='converter-uah']").focusout(function() {
		if (!$.trim($(this).val()).length) $(this).val(cacheUAH);
	});
	$("[name='converter-gbp']").focusout(function() {
		if (!$.trim($(this).val()).length) $(this).val(cacheGBP);
	});
	$("[name='converter-chf']").focusout(function() {
		if (!$.trim($(this).val()).length) $(this).val(cacheCHF);
	});
});

function IsNumeric(input)
{
    return (input - 0) == input && input.length > 0;
}

function calculateMDL() {
	var units = $("[name='converter-mdl']").val();
	units = units.replace(/\,/g, ".");
	var val = curMDL;

	var resultEUR, resultUSD, resultRON, resultRUB, resultUAH, resultGBP, resultCHF;

	resultEUR = val * units / curEUR;
	resultEUR = resultEUR.toFixed(2).replace(/\.?0+$/, '');
	resultEUR = resultEUR.replace(/\./g, ",");

	resultUSD = val * units / curUSD;
	resultUSD = resultUSD.toFixed(2).replace(/\.?0+$/, '');
	resultUSD = resultUSD.replace(/\./g, ",");

	resultRON = val * units / curRON;
	resultRON = resultRON.toFixed(9).replace(/\.?0+$/, '');
	resultRON = resultRON.replace(/\./g, ",");

	resultRUB = val * units / curRUB;
	resultRUB = resultRUB.toFixed(9).replace(/\.?0+$/, '');
	resultRUB = resultRUB.replace(/\./g, ",");

	resultUAH = val * units / curUAH;
	resultUAH = resultUAH.toFixed(9).replace(/\.?0+$/, '');
	resultUAH = resultUAH.replace(/\./g, ",");

	resultGBP = val * units / curGBP;
	resultGBP = resultGBP.toFixed(9).replace(/\.?0+$/, '');
	resultGBP = resultGBP.replace(/\./g, ",");

	resultCHF = val * units / curCHF;
	resultCHF = resultCHF.toFixed(9).replace(/\.?0+$/, '');
	resultCHF = resultCHF.replace(/\./g, ",");

	$("[name='converter-eur']").val(resultEUR);
	$("[name='converter-usd']").val(resultUSD);
	$("[name='converter-ron']").val(resultRON);
	$("[name='converter-rub']").val(resultRUB);
	$("[name='converter-uah']").val(resultUAH);
	$("[name='converter-gbp']").val(resultGBP);
	$("[name='converter-chf']").val(resultCHF);
}


function calculateEUR() {
	var units = $("[name='converter-eur']").val();
	units = units.replace(/\,/g, ".");
	var val = curEUR;

	var resultMDL, resultUSD, resultRON, resultRUB, resultUAH, resultGBP, resultCHF;

	resultMDL = val * units;
	resultMDL = resultMDL.toFixed(9).replace(/\.?0+$/, '');
	resultMDL = resultMDL.replace(/\./g, ",");

	resultUSD = val * units / curUSD;
	resultUSD = resultUSD.toFixed(2).replace(/\.?0+$/, '');
	resultUSD = resultUSD.replace(/\./g, ",");

	resultRON = val * units / curRON;
	resultRON = resultRON.toFixed(9).replace(/\.?0+$/, '');
	resultRON = resultRON.replace(/\./g, ",");

	resultRUB = val * units / curRUB;
	resultRUB = resultRUB.toFixed(9).replace(/\.?0+$/, '');
	resultRUB = resultRUB.replace(/\./g, ",");

	resultUAH = val * units / curUAH;
	resultUAH = resultUAH.toFixed(9).replace(/\.?0+$/, '');
	resultUAH = resultUAH.replace(/\./g, ",");

	resultGBP = val * units / curGBP;
	resultGBP = resultGBP.toFixed(9).replace(/\.?0+$/, '');
	resultGBP = resultGBP.replace(/\./g, ",");

	resultCHF = val * units / curCHF;
	resultCHF = resultCHF.toFixed(9).replace(/\.?0+$/, '');
	resultCHF = resultCHF.replace(/\./g, ",");

	$("[name='converter-mdl']").val(resultMDL);
	$("[name='converter-usd']").val(resultUSD);
	$("[name='converter-ron']").val(resultRON);
	$("[name='converter-rub']").val(resultRUB);
	$("[name='converter-uah']").val(resultUAH);
	$("[name='converter-gbp']").val(resultGBP);
	$("[name='converter-chf']").val(resultCHF);
}

function calculateUSD() {
	var units = $("[name='converter-usd']").val();
	units = units.replace(/\,/g, ".");
	var val = curUSD;

	var resultMDL, resultEUR, resultRON, resultRUB, resultUAH, resultGBP, resultCHF;

	resultMDL = val * units / curMDL;
	resultMDL = resultMDL.toFixed(9).replace(/\.?0+$/, '');
	resultMDL = resultMDL.replace(/\./g, ",");

	resultEUR = val * units / curEUR;
	resultEUR = resultEUR.toFixed(2).replace(/\.?0+$/, '');
	resultEUR = resultEUR.replace(/\./g, ",");

	resultRON = val * units / curRON;
	resultRON = resultRON.toFixed(9).replace(/\.?0+$/, '');
	resultRON = resultRON.replace(/\./g, ",");

	resultRUB = val * units / curRUB;
	resultRUB = resultRUB.toFixed(9).replace(/\.?0+$/, '');
	resultRUB = resultRUB.replace(/\./g, ",");

	resultUAH = val * units / curUAH;
	resultUAH = resultUAH.toFixed(9).replace(/\.?0+$/, '');
	resultUAH = resultUAH.replace(/\./g, ",");

	resultGBP = val * units / curGBP;
	resultGBP = resultGBP.toFixed(9).replace(/\.?0+$/, '');
	resultGBP = resultGBP.replace(/\./g, ",");

	resultCHF = val * units / curCHF;
	resultCHF = resultCHF.toFixed(9).replace(/\.?0+$/, '');
	resultCHF = resultCHF.replace(/\./g, ",");

	$("[name='converter-mdl']").val(resultMDL);
	$("[name='converter-eur']").val(resultEUR);
	$("[name='converter-ron']").val(resultRON);
	$("[name='converter-rub']").val(resultRUB);
	$("[name='converter-uah']").val(resultUAH);
	$("[name='converter-gbp']").val(resultGBP);
	$("[name='converter-chf']").val(resultCHF);
}

function calculateRON() {
	var units = $("[name='converter-ron']").val();
	units = units.replace(/\,/g, ".");
	var val = curRON;

	var resultMDL, resultUSD, resultEUR, resultRUB, resultUAH, resultGBP, resultCHF;

	resultMDL = val * units / curMDL;
	resultMDL = resultMDL.toFixed(9).replace(/\.?0+$/, '');
	resultMDL = resultMDL.replace(/\./g, ",");

	resultUSD = val * units / curUSD;
	resultUSD = resultUSD.toFixed(2).replace(/\.?0+$/, '');
	resultUSD = resultUSD.replace(/\./g, ",");

	resultEUR = val * units / curEUR;
	resultEUR = resultEUR.toFixed(2).replace(/\.?0+$/, '');
	resultEUR = resultEUR.replace(/\./g, ",");

	resultRUB = val * units / curRUB;
	resultRUB = resultRUB.toFixed(9).replace(/\.?0+$/, '');
	resultRUB = resultRUB.replace(/\./g, ",");

	resultUAH = val * units / curUAH;
	resultUAH = resultUAH.toFixed(9).replace(/\.?0+$/, '');
	resultUAH = resultUAH.replace(/\./g, ",");

	resultGBP = val * units / curGBP;
	resultGBP = resultGBP.toFixed(9).replace(/\.?0+$/, '');
	resultGBP = resultGBP.replace(/\./g, ",");

	resultCHF = val * units / curCHF;
	resultCHF = resultCHF.toFixed(9).replace(/\.?0+$/, '');
	resultCHF = resultCHF.replace(/\./g, ",");

	$("[name='converter-mdl']").val(resultMDL);
	$("[name='converter-usd']").val(resultUSD);
	$("[name='converter-eur']").val(resultEUR);
	$("[name='converter-rub']").val(resultRUB);
	$("[name='converter-uah']").val(resultUAH);
	$("[name='converter-gbp']").val(resultGBP);
	$("[name='converter-chf']").val(resultCHF);
}

function calculateRUB() {
	var units = $("[name='converter-rub']").val();
	units = units.replace(/\,/g, ".");
	var val = curRUB;

	var resultMDL, resultUSD, resultRON, resultEUR, resultUAH, resultGBP, resultCHF;

	resultMDL = val * units / curMDL;
	resultMDL = resultMDL.toFixed(9).replace(/\.?0+$/, '');
	resultMDL = resultMDL.replace(/\./g, ",");

	resultUSD = val * units / curUSD;
	resultUSD = resultUSD.toFixed(2).replace(/\.?0+$/, '');
	resultUSD = resultUSD.replace(/\./g, ",");

	resultRON = val * units / curRON;
	resultRON = resultRON.toFixed(9).replace(/\.?0+$/, '');
	resultRON = resultRON.replace(/\./g, ",");

	resultEUR = val * units / curEUR;
	resultEUR = resultEUR.toFixed(2).replace(/\.?0+$/, '');
	resultEUR = resultEUR.replace(/\./g, ",");

	resultUAH = val * units / curUAH;
	resultUAH = resultUAH.toFixed(9).replace(/\.?0+$/, '');
	resultUAH = resultUAH.replace(/\./g, ",");

	resultGBP = val * units / curGBP;
	resultGBP = resultGBP.toFixed(9).replace(/\.?0+$/, '');
	resultGBP = resultGBP.replace(/\./g, ",");

	resultCHF = val * units / curCHF;
	resultCHF = resultCHF.toFixed(9).replace(/\.?0+$/, '');
	resultCHF = resultCHF.replace(/\./g, ",");

	$("[name='converter-mdl']").val(resultMDL);
	$("[name='converter-usd']").val(resultUSD);
	$("[name='converter-ron']").val(resultRON);
	$("[name='converter-eur']").val(resultEUR);
	$("[name='converter-uah']").val(resultUAH);
	$("[name='converter-gbp']").val(resultGBP);
	$("[name='converter-chf']").val(resultCHF);
}

function calculateUAH() {
	var units = $("[name='converter-uah']").val();
	units = units.replace(/\,/g, ".");
	var val = curUAH;

	var resultMDL, resultUSD, resultRON, resultRUB, resultEUR, resultGBP, resultCHF;

	resultMDL = val * units / curMDL;
	resultMDL = resultMDL.toFixed(9).replace(/\.?0+$/, '');
	resultMDL = resultMDL.replace(/\./g, ",");

	resultUSD = val * units / curUSD;
	resultUSD = resultUSD.toFixed(2).replace(/\.?0+$/, '');
	resultUSD = resultUSD.replace(/\./g, ",");

	resultRON = val * units / curRON;
	resultRON = resultRON.toFixed(9).replace(/\.?0+$/, '');
	resultRON = resultRON.replace(/\./g, ",");

	resultRUB = val * units / curRUB;
	resultRUB = resultRUB.toFixed(9).replace(/\.?0+$/, '');
	resultRUB = resultRUB.replace(/\./g, ",");

	resultEUR = val * units / curEUR;
	resultEUR = resultEUR.toFixed(2).replace(/\.?0+$/, '');
	resultEUR = resultEUR.replace(/\./g, ",");

	resultGBP = val * units / curGBP;
	resultGBP = resultGBP.toFixed(9).replace(/\.?0+$/, '');
	resultGBP = resultGBP.replace(/\./g, ",");

	resultCHF = val * units / curCHF;
	resultCHF = resultCHF.toFixed(9).replace(/\.?0+$/, '');
	resultCHF = resultCHF.replace(/\./g, ",");

	$("[name='converter-mdl']").val(resultMDL);
	$("[name='converter-usd']").val(resultUSD);
	$("[name='converter-ron']").val(resultRON);
	$("[name='converter-rub']").val(resultRUB);
	$("[name='converter-eur']").val(resultEUR);
	$("[name='converter-gbp']").val(resultGBP);
	$("[name='converter-chf']").val(resultCHF);
}

function calculateGBP() {
	var units = $("[name='converter-gbp']").val();
	units = units.replace(/\,/g, ".");
	var val = curGBP;

	var resultMDL, resultUSD, resultRON, resultRUB, resultEUR, resultUAH, resultCHF;

	resultMDL = val * units / curMDL;
	resultMDL = resultMDL.toFixed(9).replace(/\.?0+$/, '');
	resultMDL = resultMDL.replace(/\./g, ",");

	resultUSD = val * units / curUSD;
	resultUSD = resultUSD.toFixed(2).replace(/\.?0+$/, '');
	resultUSD = resultUSD.replace(/\./g, ",");

	resultRON = val * units / curRON;
	resultRON = resultRON.toFixed(9).replace(/\.?0+$/, '');
	resultRON = resultRON.replace(/\./g, ",");

	resultRUB = val * units / curRUB;
	resultRUB = resultRUB.toFixed(9).replace(/\.?0+$/, '');
	resultRUB = resultRUB.replace(/\./g, ",");

	resultEUR = val * units / curEUR;
	resultEUR = resultEUR.toFixed(2).replace(/\.?0+$/, '');
	resultEUR = resultEUR.replace(/\./g, ",");

	resultUAH = val * units / curUAH;
	resultUAH = resultUAH.toFixed(9).replace(/\.?0+$/, '');
	resultUAH = resultUAH.replace(/\./g, ",");

	resultCHF = val * units / curCHF;
	resultCHF = resultCHF.toFixed(9).replace(/\.?0+$/, '');
	resultCHF = resultCHF.replace(/\./g, ",");

	$("[name='converter-mdl']").val(resultMDL);
	$("[name='converter-usd']").val(resultUSD);
	$("[name='converter-ron']").val(resultRON);
	$("[name='converter-rub']").val(resultRUB);
	$("[name='converter-eur']").val(resultEUR);
	$("[name='converter-uah']").val(resultUAH);
	$("[name='converter-chf']").val(resultCHF);
}

function calculateCHF() {
	var units = $("[name='converter-chf']").val();
	units = units.replace(/\,/g, ".");
	var val = curCHF;

	var resultMDL, resultUSD, resultRON, resultRUB, resultEUR, resultGBP;

	resultMDL = val * units / curMDL;
	resultMDL = resultMDL.toFixed(9).replace(/\.?0+$/, '');
	resultMDL = resultMDL.replace(/\./g, ",");

	resultUSD = val * units / curUSD;
	resultUSD = resultUSD.toFixed(2).replace(/\.?0+$/, '');
	resultUSD = resultUSD.replace(/\./g, ",");

	resultRON = val * units / curRON;
	resultRON = resultRON.toFixed(9).replace(/\.?0+$/, '');
	resultRON = resultRON.replace(/\./g, ",");

	resultRUB = val * units / curRUB;
	resultRUB = resultRUB.toFixed(9).replace(/\.?0+$/, '');
	resultRUB = resultRUB.replace(/\./g, ",");

	resultEUR = val * units / curEUR;
	resultEUR = resultEUR.toFixed(2).replace(/\.?0+$/, '');
	resultEUR = resultEUR.replace(/\./g, ",");

	resultUAH = val * units / curUAH;
	resultUAH = resultUAH.toFixed(9).replace(/\.?0+$/, '');
	resultUAH = resultUAH.replace(/\./g, ",");

	resultGBP = val * units / curGBP;
	resultGBP = resultGBP.toFixed(9).replace(/\.?0+$/, '');
	resultGBP = resultGBP.replace(/\./g, ",");

	$("[name='converter-mdl']").val(resultMDL);
	$("[name='converter-usd']").val(resultUSD);
	$("[name='converter-ron']").val(resultRON);
	$("[name='converter-rub']").val(resultRUB);
	$("[name='converter-eur']").val(resultEUR);
	$("[name='converter-uah']").val(resultUAH);
	$("[name='converter-gbp']").val(resultGBP);
}

function GetBNMRates() {
	curEUR = $("[name='today-eur']").val();
	curEUR = curEUR.replace(/\,/g, ".");
	curEUR = (1 / curEUR);
	curUSD = $("[name='today-usd']").val();
	curUSD = curUSD.replace(/\,/g, ".");
	curUSD = (1 / curUSD);
	curRON = $("[name='today-ron']").val();
	curRON = curRON.replace(/\,/g, ".");
	curRUB = $("[name='today-rub']").val();
	curRUB = curRUB.replace(/\,/g, ".");
	curUAH = $("[name='today-uah']").val();
	curUAH = curUAH.replace(/\,/g, ".");
	curGBP = $("[name='today-gbp']").val();
	curGBP = curGBP.replace(/\,/g, ".");
	curCHF = $("[name='today-chf']").val();
	curCHF = curCHF.replace(/\,/g, ".");
}

$(document).ready(function() {
	$("[id^='vlt']").each(function() {
		var _id = $(this).attr("id");
		var lastDigit = _id.match(/\d/g);
		if (!lastDigit || lastDigit.length != 2) {
			return;
		}
		var $input = $("input#vlt" + lastDigit);
		$(this).zclip({
			path: 'js/ZeroClipboard.swf',
			copy: function() {
				return $input.val();
			},
			beforeCopy: function() {
				$input.addClass('active')
			},
			afterCopy: function() {
				var interval = setInterval(function() {
					$input.addClass('active2');
					var interval2 = setInterval(function() {
						$input.removeClass('active2');
						$input.removeClass('active');
						clearInterval(interval2)
					}, 600);
					clearInterval(interval);
				}, 0);
			}
		});
	});
});
