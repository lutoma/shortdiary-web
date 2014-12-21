'use strict';

$(window).ready(function() {
	console.log('ohai.');
	$('#vip-pay-banktransfer-link').click(function(e) {
		e.preventDefault();

		$('#vip-banktransfer').slideToggle();
		$('#vip-pay-banktransfer-link').fadeOut();
	});
});