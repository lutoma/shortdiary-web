function show_chars() {
	var chars = $(this).val().length;
	var words = $(this).val().split(' ').length - 1;
	var sentences = $(this).val().split(/[\.\?\!:;…‽⸮"«“]+/).length - 1;

	if(chars > 350)
		$('#new-post-char-counter').html('Wow, what an eventful day! – ' + sentences + ' sentences, ' + words + ' words, ' + chars + ' characters');
	else
		$('#new-post-char-counter').html(sentences + ' sentences, ' + words + ' words, ' + chars + ' characters');
}

function image_field_change(input) {
		if(input.files && input.files[0]) {
			var reader = new FileReader();
			reader.onload = function(e) {
				$('#image-upload').css('background', "url(" + e.target.result + ")").html('');
			}

			reader.readAsDataURL(input.files[0]);
		}
}

function prevent_default(e) {
	if(e.preventDefault)
		e.preventDefault();

	return false;
}

function handle_drop(e) {
	if(e.preventDefault)
		e.preventDefault();

	console.log('dropped.');

	var files = e.dataTransfer.files;
	var reader = new FileReader();

	reader.onload = function(e) {
		$('#image-upload').css('background', "url(" + e.target.result + ")").html('');
	}

	reader.readAsDataURL(files[0]);
}

$(document).ready(function() {
	$('#text-input').keyup(show_chars);
	$('#text-input').change(show_chars);

	$('#image-upload').on('dragover', prevent_default);
	$('#image-upload').on('dragenter', prevent_default);

	$('#image-upload').on('drop', handle_drop);

	$('#image-upload').click(function() {
		$('#image-upload-input').click();
	});
});
