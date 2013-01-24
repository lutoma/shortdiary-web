function get_cookie(name) {
	var cookie_value = null;

	if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');

		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);

			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookie_value = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookie_value;
}

var csrftoken = get_cookie('csrftoken');

function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
	crossDomain: false,
	beforeSend: function(xhr, settings) {
		if(!csrfSafeMethod(settings.type)) {
			xhr.setRequestHeader("X-CSRFToken", csrftoken);
		}
	}
});