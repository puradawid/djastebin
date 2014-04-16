$(document).ready(function() {
	$(".comment-reply a").click(function() {
		var parent = $(this).parents('.comment-row');
		$('#comment_form').insertAfter(parent);
		var input = $('textarea[id=id_content]');
		input.focus();
		var last_char = input.val()[input.val().length - 1];
		if (last_char && last_char != '\n' && last_char != ' ')
			input.val(input.val() + " ");
		input.val( input.val() + "@" + parent.find(".comment-author a").text() + ": " );
		$('input[id=id_comment_parent]').val(this.id.replace('node_', ''));
		$('#cancel_reply').css('display', 'inline-block');
    	$('html,body').animate({scrollTop: parent.offset().top - 20},'slow');
		return false;
	});
	$('#cancel_reply').click(function() {
		$('#comment_form').insertAfter('#comments_tree');
		$('input[id=id_comment_parent]').val('');
		$('#cancel_reply').css('display', 'none');
		$('#id_content').val('');
		return false;
	});
});
