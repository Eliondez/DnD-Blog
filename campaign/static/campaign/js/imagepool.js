function getImageListForList(url) {
  $.getJSON(url, function(data) {
    var images = $("ul.image-selector .image-itm");
    var imgCount = data.images.length - 1;

    for (var i = 0; i < 4; i++) {
      var addLink = $(images.get(i)).find("a.insert");
      var delLink = $(images.get(i)).find("a.delete");
      var imgDiv = $(images.get(i)).find("div.image-itm-body");

      if (i <= imgCount) {
        addLink.attr('href', data.images[i].src);
        delLink.attr('href', data.images[i].delete_src);
        imgDiv.attr('style', "background-image: url(" + data.images[i].src + ")");
      } else {
        addLink.attr('href', "#");
        delLink.attr('href', "#");
        imgDiv.attr('style', "background: #ccc");
      }
      
    }

    var leftBut = $(".image-selector .prev a");
    if (data.prev_url == "") {
      leftBut.addClass("disabled");
      leftBut.attr("href", "#");
    } else {
      leftBut.removeClass("disabled");
      leftBut.attr("href", data.prev_url);
    }

    var rightBut = $(".image-selector .next a");
    if (data.next_url == "") {
      rightBut.addClass("disabled");
      rightBut.attr("href", "#");
    } else {
      rightBut.removeClass("disabled");
      rightBut.attr("href", data.next_url);
    }
  });
}

function getCaretPos(jQobject) {
  var obj = jQobject.get(0);
  obj.focus();
  if (document.selection) {
    var sel = document.selection.createRange();
    var clone = sel.duplicate();
    sel.collapse(true);
    clone.moveToElementText(obj);
    clone.setEndPoint("EndToEnd", sel);
    return clone.text.length;
  } else if (obj.selectionStart !== false) return obj.selectionStart;
  else return 0;
}

$(function() {
  var contentField = $("form textarea[name=content]");

  $("#imagepool_prev, #imagepool_next").click(function(evt) {
    evt.preventDefault();
    getImageListForList($(this).attr("href"));
  });

  $("li.prev a, li.next a").click(function(evt) {
    evt.preventDefault();
    getImageListForList($(this).attr("href"));
  });

    $('#file_to_upload').change(function() {
        $('#imagepool_form').submit();
    });

  $("#imagepool_output").on("load", function() {
    getImageListForList($(".image-selector").attr("href"));
  });

  $(".image-selector").on("click", ".image-itm a.insert", function(evt) {
    evt.preventDefault();
    var content = contentField.val();
    var position = getCaretPos(contentField);
    content = content.substring(0, position) + "[img]" + location.protocol +
    "//" + location.host + $(this).attr("href") + "[/img]" +
    content.substring(position);
    contentField.val(content);
  });

  $(".image-selector").on("click", ".image-itm a.delete", function(evt) {
    evt.preventDefault();
    if (window.confirm("Удалить изображение?")) {
      $.getJSON($(this).attr("href"), function(data) {
        getImageListForList($(".image-selector").attr("href"));
      });
    }
  });

  getImageListForList($(".image-selector").attr("href"));
});
