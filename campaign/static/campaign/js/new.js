$(function(){
     $("td#camp_started").on("click", ".btn", function(evt){
        evt.preventDefault();
        var myData = {};
        myData['csrfmiddlewaretoken'] = getCookie('csrftoken');
        var container = $(this).parent();
        var myButton = $(this);
        $.ajax({
            url: $(this).attr('href'),
            type: 'POST',
            data: myData,
            success: function(response){
                var date = response['date'];
                $(myButton).fadeOut(function(){
                    $(container).append(date);
                });
            }
        })
    });

    $("td#camp_ended").on("click", ".btn", function(evt){
        evt.preventDefault();
        var myData = {};
        myData['csrfmiddlewaretoken'] = getCookie('csrftoken');
        var container = $(this).parent().find('p.end-date');
        var myButton = $(this);
        $.ajax({
            url: $(this).attr('href'),
            type: 'POST',
            data: myData,
            success: function(response){
                //var date = response['date'];
                //console.log(date);
                if (response['date']) {
                    console.log('resume');
                    container.html(response['date']);
                    myButton.text("Возобновить");
                } else {
                    container.html("");
                    console.log('delay');
                    myButton.text("Остановить");
                }
            }
        })
    });

});

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


