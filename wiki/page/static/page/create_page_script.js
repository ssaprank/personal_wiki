$( document ).ready(function() {
    console.log( "ready!" );

    $(".add_tag_button").click(function(){
        tag = $(this).attr('name').replace("add_","").replace("_tag","");
        insertTag(tag);
    });

    $('#html_view_toggle').click(function(){
        obj = $(this)
        if (obj.val() === 'Switch to html') {
            // use a hidden div and put the text as html() there
            obj.val('Switch to view');
        } else {
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
