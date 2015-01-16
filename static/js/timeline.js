'use strict';

var current_year = null;
var last_filter = null;

function handle_filter(event) {
	var posts = event.data;
	var search_string = $(this).val().toLowerCase();

	// Check if anything has changed
	if (last_filter === search_string) {
		return;
	}

	// Clone posts element so we don't delete entries from the original one
	posts = jQuery.extend(true, {}, posts);


	// Heavy filtering. Each layer first calls the filter for the next lower
	// layer, then only returns true for an element if there actually are any
	// contained elements left.
	//
	// Before, this just used to filter and then rerender, but that causes
	// problems with event handlers and loses input field focus, so just filter
	// and hide on the fly.
	posts = _.filter(posts, function(year) {
		year.posts = _.filter(year.posts, function(month) {
			month.posts = _.filter(month.posts, function(post) {
				var match = (post.text.toLowerCase().indexOf(search_string) >= 0);
				$('.timeline-box[data-post-id="' + post.id + '"]').toggle(match);
				return match;
			})

			var match = (month.posts.length > 0);
			$('#timegroup-m-' + month.year + '-' + month.month).toggle(match);
			return (match);
		});

		var match = (year.posts.length > 0);
		$('#timegroup-' + year.year).toggle(match);
		return (match);
	});

	// Rerender datepicker
	render_datepicker(posts);

	// Show/hide 'no posts' message if necessary
	$('#timeline-filter-notposts > h2 > span').html($(this).val());
	$('#timeline-filter-notposts').toggle(posts.length < 1);

	last_filter = search_string;
}

function setup_handlers(posts) {
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

	// Monitor changes to the filter input and rerender on change
	$('#timeline-filter').on('keyup input blur', posts, handle_filter);
}

function render_datepicker(posts) {
	var template = Handlebars.compile($("#timeline-datepicker-template").html());
	var html = template({timegroups: posts});
	$('#timeline-datepicker').html(html);

	$('#timeline-datepicker li a').click(function (event) {
		var scroll_to = $(event.toElement).data('scrollto');
		$('#timegroup-' + scroll_to).ScrollTo();
	});
}

function render(posts) {
	var template = Handlebars.compile($("#timeline-main").html());
	var html = template({timegroups: posts, media_url: media_url});
	$('#timeline-stage').html(html);

	render_datepicker(posts);

	$('.aside-keepvisible').scrollToFixed({marginTop: $('#top-block').outerHeight(true) - 20});

	setup_handlers(posts);
}

function reformat_data(posts) {
	if (_.isEmpty(posts)) {
		var template = Handlebars.compile($("#timeline-noposts").html());
		$('#timeline-stage').html(template());

		return false;
	}

	// TODO Localization
	// FIXME Why is this an object?
	var month_names = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
		7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"};

	var day_names = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];


	var day = 1000 * 60 * 60 * 24;

	// Reformat and sort posts (objects are unsorted, so convert to arrays)
	posts = _.map(posts, function (year_posts, year) {
		year_posts = _.map(year_posts, function (month_posts, month) {
			month_posts = _.map(month_posts, function (post) {
				// FIXME Code/logic duplication
				var js_date = new Date(post['date']);
				post['editable'] = (new Date() - js_date) <= day * 3;
				post['text'] = post['text'].replace(/\n/g, '<br />');
				post['day'] = js_date.getDate();
				post['dow'] = day_names[js_date.getDay()];
				return post;
			});

			return {
				'year': year,
				'month': month, 
				'month_name': month_names[month],
				'posts': month_posts
			};
		});

		year_posts = _.sortBy(year_posts, function(month) { return -month.month; });
		return {'year': year, 'posts': year_posts};
	});

	posts = _.sortBy(posts, function(year) { return -year.year; });
	current_year = posts[0].year;
	render(posts);
}

$(window).ready(function() {
	mixpanel.track('Dashboard load');
	Handlebars.registerPartial("timeline-boxlist", $("#timeline-boxlist-partial").html());

	$.get('/api/v1/posts/timeline/?format=json', reformat_data);
});
