$(function(){    
    var service = 'http://localhost:8080';
    var badge = $('<div id="badge">FeedbackGov</div>').click(function() {
        $('<form action="' + service + '" method="post" id="feedback"><p>Leave your feedback about this site over on FeedbackGov. Submitting this form will take you to another site.</p><a href="." id="close_feedback">Close</a><input type="hidden" name="name" value="' + document.title + '"/><input type="hidden" name="url" value="' + window.location + '"/><div><label for="title">Title</label><input type="text" id="title" name="title"/ class="txt"></div><div><label for="description">Description</label><textarea id="descrition" name="description"></textarea></div><div><input type="submit" id="send" name="Send"/></div></form>').appendTo('body');
    }).appendTo('body');
});
