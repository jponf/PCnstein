
function getGeoInfoByIP(asinc_func) {

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
					alert(geoJSON.countryName);
					asinc_func(geoJSON);
				} else {
					alert('Empty response');
				}
			}
		}

		xmlhttp.open("GET", "http://smart-ip.net/geoip-json", true);
		xmlhttp.withCredentials = "true";
		xmlhttp.send();

	} else {
		alert('It was impossible to create an XMLHttpRequest object')
	}
}