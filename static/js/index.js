$(window).ready(function() {
	$('.delete-post').click(function(event) {
		event.preventDefault();

		confirmation = confirm('Are you sure you want to delete this post?');

		if(!confirmation)
			return false;

		post_id = $(this).data('id');

		console.log('/posts/' + post_id + '/delete/')

		$('#post-' + post_id + ' .edit').html("<i class='icon-spinner icon-spin'></i>");

		$.ajax({
			type: 'DELETE',
			url: '/posts/' + post_id + '/delete/'
		}).done(function() { 
			$('#post-' + post_id).fadeOut();
		});

		return false;
	});
});