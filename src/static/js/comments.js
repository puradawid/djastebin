$(document).ready(function() {
	$(".comment-reply a").click(function() {
		var parent = $(this).parents('.comment-row');
		$('#comment_form').insertAfter(parent);
		$('input[id=id_comment_parent]').val(this.id.replace('node_', ''));
		$('#cancel_reply').css('display', 'inline-block');
		return false;
	});
	$('#cancel_reply').click(function() {
		$('#comment_form').insertAfter('#comments_tree');
		$('input[id=id_comment_parent]').val('');
		$('#cancel_reply').css('display', 'none');
		return false;
	});
});
