$( document ).ready(function() {
    console.log( "ready!" );

    var textarea;
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
    
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    //needed for csrf handling while doing post call for uploading images
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $(".add_tag_button").click(function(){
        tag = $(this).attr('name').replace("add_","").replace("_tag","");
        insertTag(tag);
    });

    $('#html_view_toggle').click(function(){
        obj = $(this)
        if (obj.val() === 'Switch to html') {
            // use a hidden div and put the text as html() there
            let viewarea = $('#html_wrapper');
            viewarea.html(textarea);            
            obj.val('Switch to view');
            $("#edit_page_button_row").show();
        } else {
            textarea = $('#id_html');
            let viewarea = $('#html_wrapper');
            let width = textarea.width();
            let height = textarea.height();
            viewarea.width(width);
            viewarea.height(height);
            viewarea.html(textarea.val());
            $("#edit_page_button_row").hide();
            obj.val('Switch to html');
        }
    });

    $("#html_tag_list").change(function() {
        tag = $(this).val();
        if (tag !== 0) {
            insertTag(tag);
            $(this).val('0')
        }
    });

  /* Handling the image uploading */
    $(".js-upload-photos").click(function () {
       $("#fileupload").click();
    });

    $("#fileupload").fileupload({
        dataType: 'json',
        done: function (e, data) {
            if (data.result.is_valid) {
                alert("Photos successfully uploaded! Url: " + data.result.url);
            } else {
                alert("There was an error uploading your images");
            }
        }
    });

    $("[id^=insert_image]").click(function(e) {
        e.preventDefault();
        let textarea = $("#id_html");
        let imageUrl = $(this).prop("src");
        let htmlString = '<img src="' + imageUrl + '" />';
        let value = textarea.val();
        textarea.val(value + htmlString);
        $('#imagesInsertionModal').modal('hide');
        textarea.focus();
    });

    function insertTag(tag)
    {
        let textarea = $("#id_html");
        let value = textarea.val();

        let caretPosition = textarea.prop("selectionStart");
        let textBefore = value.substring(0,  caretPosition );
        let textAfter  = value.substring(caretPosition, value.length);

        let newValue = textBefore;
        let newCaretPosition = 0;
        
        if (['br', 'hr'].includes(tag)) {
            newValue += '<' + tag + '/>' + textAfter;
            newCaretPosition = caretPosition + tag.length + 3;
        } else {
            newValue += '<' + tag + '>' + '</' + tag + '>' + textAfter;
            newCaretPosition = caretPosition + tag.length + 2;
        }
         
        textarea.val(newValue);
        textarea.focus();

        textarea.prop("selectionStart", newCaretPosition);
        textarea.prop("selectionEnd", newCaretPosition);
    }
});
