
//
// Recovers geo localization data and pass it to the specified funciton asynchronously
//
function getGeoInfoByIP(async_func) {

	var xmlhttp;

	if(window.XMLHttpRequest) { // Browsers and IE7+
		xmlhttp = new XMLHttpRequest();
	} else {	// For IE6, IE5
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}

	if(xmlhttp) {

		xmlhttp.onreadystatechange = function() {
			if( xmlhttp.readyState == 4 ) {
				if(xmlhttp.responseText) {				
					geoJSON = JSON.parse(xmlhttp.responseText);
					async_func(geoJSON);
				} else {
					alert('Empty geoloc response');
				}
			}
		}

		xmlhttp.open("GET", "/geolocbyip", true);
		xmlhttp.send();

	} else {
		alert('It was impossible to create an XMLHttpRequest object')
	}
}

//
// Reads a file form the given url which contains a list of elements separated
// by the specified separator and pass it to the specified function asynchronously
//
function getDataFromFile(file_url, separator, async_func) {

	var xmlhttp;

	if(window.XMLHttpRequest) { // Browsers and IE7+
		xmlhttp = new XMLHttpRequest();
	} else {	// For IE6, IE5
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}

	if(xmlhttp) {

		xmlhttp.onreadystatechange = function() {
			if( xmlhttp.readyState == 4 ) {
				if(xmlhttp.responseText) {				
					
					var lines = xmlhttp.responseText.split('\n')
					var items = []

					for( var i = 0; i < lines.length; i++ ) {
						var elems = lines[i].split(separator)
						for( var j = 0; j < elems.length; j++ ) {
							items.push(elems[j])
						}
					}

					async_func(items)					

				} else {
					alert('Empty response');
				}
			}
		}

		xmlhttp.open("GET", file_url, true);
		xmlhttp.send();

	} else {
		alert('It was impossible to create an XMLHttpRequest object')
	}
}