function show_chars() {
	var chars_left = 350 - $(this).val().length;
	$('#new-post-char-counter').html(chars_left);

	if(chars_left < 0)
		$('#new-post-char-counter').css('color', 'red');
	else if(chars_left < 15)
		$('#new-post-char-counter').css('color', 'orange');
	else
		$('#new-post-char-counter').css('color', 'inherit');
}

$(document).ready(function() {
	$('#text-input').keyup(show_chars);
	$('#text-input').change(show_chars);
});
