'use strict';

$(window).ready(function() {
	console.log('ohai.');
	$('#front-mainsignup > a').click(function(e) {
		e.preventDefault();

		$('#front-mainsignup .form').show();
		$('#front-mainsignup a').hide();
		$( "#front-mainsignup .form" ).animate({
			width: '100%'
		}, 200, function() {
			$('#front-mainsignup .form input[name=username]').focus();
		});
	});
});