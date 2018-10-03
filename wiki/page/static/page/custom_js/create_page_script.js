const STORAGE_PAGE_URL_ITEM = "current_url";
const STORAGE_PAGE_DATA_ITEM = "page_data";
const API_ENDPOINT = "http://127.0.0.1:8000/api/";
// if true - the page is being submitted, so no data should be written to the local storage
var pageBeingSubmitted = false;


$( document ).ready(function() {
    var textarea = $('#id_html');
    var specialCharactersRegex = /[!@#$%\^\&\*()_+\-=\[\]{};:'"\\|,.<>\/\?]/;

    bindRemovePageTagEventListener();
    bindInsertImageEventListener();

    $(window).on("unload beforeunload", function() {
        current_url = window.location.pathname;

        // if we just loaded create or edit page view
        if (/^\/(\d+\/edit|create)$/.test(current_url) && !pageBeingSubmitted) {
            // refill the storage

            let data = JSON.stringify({
                "title" : $('#id_title').val(),
                "html" : $('#id_html').val(),
                "wip" : $('#id_work_in_progress').val()
            });

            localStorage.setItem(STORAGE_PAGE_DATA_ITEM, data);
            localStorage.setItem(STORAGE_PAGE_URL_ITEM, current_url);
        }
    });

    window.onload = function() {
        current_url = window.location.pathname;
        pageBeingSubmitted = false;

        // if we just loaded create or edit page view
        if (/^\/(\d+\/edit|create)$/.test(current_url)) {
            let storedPage = localStorage.getItem(STORAGE_PAGE_URL_ITEM);
            if (storedPage != null) {
                if (storedPage == current_url) {
                    // load storage info
                    let storedPageData = JSON.parse(localStorage.getItem(STORAGE_PAGE_DATA_ITEM));
                    let title = storedPageData.title;
                    let html = storedPageData.html;
                    let hidden_tags_input = storedPageData.hiddenTagsInput;
                    let wip = storedPageData.wip;

                    $('#id_title').val(title);
                    $('#id_html').val(html);
                    $('#id_work_in_progress').val(wip);
                } else {
                    // remove storage info
                    localStorage.removeItem(STORAGE_PAGE_DATA_ITEM);
                    localStorage.removeItem(STORAGE_PAGE_URL_ITEM);
                }
            }
        }
    }

    $("#edit_page_form").keydown(function(e) {
        if (e.keyCode == 13 && !(textarea.is(":focus"))) {
            e.preventDefault();
            return false;
        }
    });

    $("#edit_page_form").submit(function(e) {
        current_url = window.location.pathname;
        pageBeingSubmitted = true;

        //bring back html textarea in case we're in view mode
        if ($("#html_view_toggle").val() == "Switch to html") {
            $('#html_view_toggle').click()
        }

        // clear storage data of the page
        localStorage.removeItem(STORAGE_PAGE_DATA_ITEM);
        localStorage.removeItem(STORAGE_PAGE_URL_ITEM);
    });

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
        let viewarea = $('#html_wrapper');
        if (obj.val() === 'Switch to html') {
            // use a hidden div and put the text as html() there
            viewarea.html(textarea);            
            obj.val('Switch to view');
            $("#edit_page_button_row").show();
        } else {
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
                // now add image to the modal for insertion
                getLastUploadedImageForInsertion();
            } else {
                alert("There was an error uploading your images");
            }
        }
    });


    function insertTag(tag)
    {
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

    $("#id_tags").autocomplete({
        source: API_ENDPOINT + "get_page_tags",
        minLength: 2
    });

    $("#id_tags").keyup(function(e) {
        e.preventDefault();
        if (e.keyCode == 13) {
            // on pressing enter - add to page tags container div its name and a button that will delete it
            let tagName = $(this).val();

            if (tagName == "") {
                return;
            }

            // if new tag name does not contain any of the special characters
            if (specialCharactersRegex.test(tagName)) {
                $("#error_modal_body").text("Tags must not contain any special characters!");
                $('#error_message_modal').modal('show');
            } else {
                // hidden input is being read after the form gets submitted
                let hiddenInputVal = $("#hidden_page_tags_input").val();
                if (hiddenInputVal == "") {
                    $("#hidden_page_tags_input").val(tagName)
                } else {
                    $("#hidden_page_tags_input").val(hiddenInputVal + "," + tagName)
                }

                // after creating a new tag - insert appropriate html to the tags container
                getLastInsertedTag(tagName);

                $(this).val("");
            }
        }
    });

    // bind event listener to all remove_page_tag buttons (needed when creating new buttons on-the-fly)
    function bindRemovePageTagEventListener() {
        $("button.remove_page_tag").unbind("click");
        $("button.remove_page_tag").click(function(e) { 
            let tagName = $(this).attr('id').replace("remove_page_tag_","");
            let hiddenInputValue = $("#hidden_page_tags_input").val(); 

            let regex = /(^\,)($\,)/;
            $("#page_tag_name_" + tagName).remove();

            hiddenInputValue = hiddenInputValue.replace(tagName, "").replace(",,",",").replace(/^\,|\,$/,"");

            $("#hidden_page_tags_input").val(hiddenInputValue);                
        });
    }

    function bindInsertImageEventListener() {
        $(".insert_image").unbind("click");
        $(".insert_image").click(function(e) {
            e.preventDefault();
            let imageUrl = $(this).prop("src");
            let htmlString = '<img src="' + imageUrl + '" />';
            let value = textarea.val();
            textarea.val(value + htmlString);
            $('#imagesInsertionModal').modal('hide');
            textarea.focus();
        });
    }

    function getLastUploadedImageForInsertion() {
        $.get({
            url: API_ENDPOINT + "get_last_uploaded_image",
            success: function(data) {
                let modalBodyElement = $("#image_insertion_modal_body"); 
                modalBodyElement.html(modalBodyElement.html() + data);
                bindInsertImageEventListener();
            }
        });
    }

    function getLastInsertedTag(tagName) {
        $.get({
            url: API_ENDPOINT + "get_last_inserted_tag",
            data: {'tag_name' : tagName},
            success: function(data) {
                let tagContainerElement = $("#page_tags_container"); 
                tagContainerElement.html(tagContainerElement.html() + data);
                bindRemovePageTagEventListener();
            }
        });
    }


});
