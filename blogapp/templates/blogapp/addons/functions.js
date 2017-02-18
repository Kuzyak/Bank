function sortAsc(a, b){
	if(a < b)
		return -1
	if(a > b) 
    	 return 1

	return 0
}

function sortDesc(a, b){
	if(a > b)
		return -1
	if(a < b)
		return 1

	return 0
}

function sortFloat(a, b) {
	return a - b;
}

function nl2br(str) {
	return str.replace(/([^>])\n/g, '$1<br/>');
}

function validateEmail(email) { 
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}

function validatePhone(phone) {
	var phoneRegExp = /^(?:\+)?[0-9-\s()]{5,}$/
	return phoneRegExp.test(phone);
}

function isNumber(n) {
  return !isNaN(parseFloat(n)) && isFinite(n);
}

/**
 * Функция получает массив аргументов и возвращает лучший курс покупки, т.е.
 * самое большое значение в виде строки.
 * @param {float} values - массив значений с валютными курсами банков
 * @param {int} decimals - кол-во символов после запятых
 */
function getBestBuying(values, decimals) {
	for (var i = 0; i < values.length; i++) {
		values[i] = values[i].replace(/,/g, ".");
		values[i] = parseFloat(values[i]);
	}	
	
	// Удаление из массива NaN значений
	var tmp = new Array();
	for (var i = 0; i < values.length; i++) {
		if (values[i]) {
			tmp.push(values[i]);
		}
	}
	
	tmp = tmp.sort(sortFloat);
	
	// Лучший курс
	var result = tmp[tmp.length - 1];
	if (result) {
		result = result.toFixed(decimals);
		result = result.toString().replace(/\./g, ",");
	} else {
		result = 0;
	}
	
	return result;
}

/**
 * Функция получает массив аргументов и возвращает лучший курс продажи, т.е.
 * наименьшее значение в виде строки.
 * @param {float} values - массив значений с валютными курсами банков
 * @param {int} decimals - кол-во символов после запятых
 */
function getBestSelling(values, decimals) {
	for (var i = 0; i < values.length; i++) {
		values[i] = values[i].replace(/,/g, ".");
		values[i] = parseFloat(values[i]);
	}	
	
	// Удаление из массива NaN значений
	var tmp = new Array();
	for (var i = 0; i < values.length; i++) {
		if (values[i]) {
			tmp.push(values[i]);
		}
	}
	
	tmp = tmp.sort(sortFloat);
	
	// Лучший курс
	var result = tmp[0];
	if (result) {
		result = result.toFixed(decimals);
		result = result.toString().replace(/\./g, ",");
	} else {
		result = 0;
	}
	
	return result;
}

if (!Array.indexOf) {
  Array.prototype.indexOf = function (obj, start) {
    for (var i = (start || 0); i < this.length; i++) {
      if (this[i] == obj) {
        return i;
      }
    }
    return -1;
  }
}

// Max of array
function getMaxOfArray(numArray) {
  return Math.max.apply(null, numArray);
}

// Min of array
function getMinOfArray(numArray) {
  return Math.min.apply(null, numArray);
}

function getHashValue(hashKey) {
	hash = location.hash.substr(1);
	
	if (!hashKey) return hash;
	
	var params = hash.split("&");
	for (var i = 0; i < params.length; i++) {
		var tmpParam = params[i].split("=");
		if (tmpParam.length == 2) {
			var key = tmpParam[0];
			var val = tmpParam[1];
			if (key == hashKey) {
				return val;
			}
		}
	}
	
	return false;
}















