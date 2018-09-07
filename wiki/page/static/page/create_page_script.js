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
        } else {
            textarea = $('#id_html');
            let viewarea = $('#html_wrapper');
            let width = textarea.width();
            let height = textarea.height();
            viewarea.width(width);
            viewarea.height(height);
            viewarea.html(textarea.val());
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

    $("#html_upload_image").change(function() {
        data = {"image" : $(this).prop('files')[0]};
        console.log(data)
        $.ajax({
            type: "POST",
            contentType: false,
            processData: false,
            url: "api/upload_image/",
            data: data,
            success: function(){alert("Image uploaded successfully")}
        });
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
