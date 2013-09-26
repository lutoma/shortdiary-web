function location_callback(position) {
	$('input[name=location_lat]').val(position.coords.latitude.toFixed(12));
	$('input[name=location_lon]').val(position.coords.longitude.toFixed(12));

	var pos = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);

	var map_options = {
		zoom: 12,
		center: pos,
		mapTypeId: google.maps.MapTypeId.ROADMAP,
		streetViewControl: false,
		mapTypeControl: false
	}

	map = new google.maps.Map($("#map-canvas").get(0), map_options);
	new google.maps.Marker({position: pos, map: map});

	geocoder = new google.maps.Geocoder();

	geocoder.geocode({'latLng': pos}, function(results, status) {

		if(status != google.maps.GeocoderStatus.OK) {
			console.log("Could not geocode: " + status);
			$('#post-location-info').hide();
		}

		$(results).each(function(idx, value) {
			if(value['types'][0] != 'locality')
				return;

			$('#post-location-info').html('Location: ' + value['formatted_address']);
			$('input[name=location_verbose]').val(value['formatted_address'])
		});
	});
}

$(document).ready(function() {
	$('#post-location-info').show();

	if(navigator.geolocation)
		navigator.geolocation.getCurrentPosition(location_callback);
});