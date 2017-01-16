$(function(){
     $(".modal-content").on("click", ".btn-success", function(evt){
//        evt.preventDefault();
        //var container = $(".modal-content");
        var new_text = $(this).parent().parent().find("textarea").val();
        var btn_save = $(this);
        var text_dest = $("#" + $(btn_save).data("text-target"))
        console.log($(btn_save).data("text-target"));
        var myData = {};
        myData['csrfmiddlewaretoken'] = getCookie('csrftoken');
        myData['text'] = new_text;
        var container = $(this).parent();
        var myButton = $(this);
        $.ajax({
            url: btn_save.attr('href'),
            type: 'POST',
            data: myData,
            success: function(response){
                var text = response['text'].replace(/\n/g, '<br>');
                text_dest.html(text);
            }
        })
    });

    window.setInterval(azaza, 2000);

});

function azaza() {
    console.log('azaza');
};

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


