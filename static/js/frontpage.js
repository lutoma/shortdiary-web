$(window).ready(function() {
	$('#invite-request-form').submit(function(event) {
		$('#invite-request-form > i').addClass('icon-spinner icon-spin')

		$.post("/invite/request/",	$(this).serialize(), function() {
			$('#invite-request-form > i').addClass('icon-ok')
			$('#invite-request-form > i').removeClass('icon-spinner icon-spin')
		});

		event.preventDefault();
	});
});