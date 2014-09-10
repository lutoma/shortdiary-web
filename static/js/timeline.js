'use strict';

function render(posts) {
	console.log(posts)
	var monthNames = [ "January", "February", "March", "April", "May", "June",
    	"July", "August", "September", "October", "November", "December" ];

	var template = Handlebars.compile($("#timeline-main").html());
	var html = template({timegroups: posts});
	$('#timeline-stage').html(html);

	$('#timeline-datepicker li a').click(function (event) {
		var scroll_to = $(event.toElement).data('scrollto');
		$('#timegroup-' + scroll_to).ScrollTo();
	});

	$('#timeline-datepicker').scrollToFixed({marginTop: $('#top-block').outerHeight(true) + 20});
}

$(window).ready(function() {
	Handlebars.registerPartial("timeline-boxlist", $("#timeline-boxlist-partial").html());

	$.get('/api/v1/posts/timeline/', render);
});