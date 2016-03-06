function show_chars() {
	var chars = $(this).val().length;
	var words = $(this).val().split(' ').length - 1;
	var sentences = $(this).val().split(/[\.\?\!:;…‽⸮"«“]+/).length - 1;

	$('#new-post-char-counter').html((chars > 350 ? (t_eventful + ' – ') : '') + sentences + ' ' + t_sentences + ', ' + words + ' ' + t_words + ', ' + chars + ' ' + t_characters);
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

	$('#text-input').textcomplete([
    { 
        mentions: mention_toplist,
        match: /\B@(\w*)$/,
        search: function (term, callback) {
            callback($.map(this.mentions, function (mention) {
                return mention.indexOf(term) === 0 ? mention : null;
            }));
        },
        index: 1,
        replace: function (mention) {
            return '@' + mention + ' ';
        }
    }
], { appendTo: 'body' })

	$('#text-input').overlay([{
		match: /\B@\w+/g,
		css: {'background-color': '#d8dfea'}
	}]);
});
