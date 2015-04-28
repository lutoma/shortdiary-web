function location_callback(position) {
	$('input[name=location_lat]').val(position.coords.latitude.toFixed(12));
	$('input[name=location_lon]').val(position.coords.longitude.toFixed(12));

	L.mapbox.accessToken = 'pk.eyJ1IjoibHV0b21hIiwiYSI6ImVkbzF4MG8ifQ.pIpC2pu9savl1ZZLl8TGrA';
	var map = L.mapbox.map('map-canvas', 'lutoma.m1iha18e', {zoomControl: false});
	map.scrollWheelZoom.disable();
	var layer = L.mapbox.featureLayer().addTo(map);

	map.setView([position.coords.latitude, position.coords.longitude], 16);
	L.marker([position.coords.latitude, position.coords.longitude]).addTo(map);

	var pos = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);

	geocoder = new google.maps.Geocoder();

	geocoder.geocode({'latLng': pos}, function(results, status) {

		if(status != google.maps.GeocoderStatus.OK) {
			console.log("Could not geocode: " + status);
			$('#post-location-info').hide();
		}

		$(results).each(function(idx, value) {
			if(value['types'][0] != 'locality')
				return;

			$('#post-location-info').html(t_location + ': ' + value['formatted_address']);
			$('input[name=location_verbose]').val(value['formatted_address'])
		});
	});
}

$(document).ready(function() {
	$('#post-location-info').show();

	if(navigator.geolocation)
		navigator.geolocation.getCurrentPosition(location_callback);
});