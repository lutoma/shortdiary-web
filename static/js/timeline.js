'use strict';

var current_year = null;

function render(posts) {
	// TODO Localization
	// FIXME Why is this an object?
	var month_names = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
		7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"};

	// Reformat and sort posts (objects are unsorted, so convert to arrays)
	posts = _.map(posts, function (year_posts, year) {
		year_posts = _.map(year_posts, function (month_posts, month) {
			return {
				'year': year,
				'month': month, 
				'month_name': month_names[month],
				'posts': month_posts
			};
		});

		year_posts = _.sortBy(year_posts, function(month) { return -month.month; });
		console.log('sorted posts: ', year_posts)

		return {'year': year, 'posts': year_posts};
	});

	posts = _.sortBy(posts, function(year) { return -year.year; });
	current_year = posts[0].year;


	var template = Handlebars.compile($("#timeline-main").html());
	var html = template({timegroups: posts});
	$('#timeline-stage').html(html);

	$('#timeline-datepicker li a').click(function (event) {
		var scroll_to = $(event.toElement).data('scrollto');
		$('#timegroup-' + scroll_to).ScrollTo();
	});

	$('#timeline-datepicker').scrollToFixed({marginTop: $('#top-block').outerHeight(true) + 20});

	// Update sidebar year indicator with current scroll position
	$('.timegroup').waypoint(function(direction) {
		var year = _.find(posts, function (year_arr) {
			// In most cases, a leftover of the old year will still be visible.
			// This would result in the old year again being selected as the
			// current one. This prevents this behaviour.
			if(year_arr.year === current_year && direction === 'down') {
				return false;
			}

			return $('#timegroup-' + year_arr.year).isOnScreen();
		});
		
		if (!year) return;

		$('#timeline-datepicker > li.active').removeClass('active');
		$('#timeline-datepicker > li[data-year=' + year.year + ']').addClass('active');
		current_year = year.year;
	}, { offset: '60%' });
}

$(window).ready(function() {
	Handlebars.registerPartial("timeline-boxlist", $("#timeline-boxlist-partial").html());

	$.get('/api/v1/posts/timeline/?format=json', render);
});