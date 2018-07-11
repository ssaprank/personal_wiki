$( document ).ready(function() {
    console.log( "ready!" );

    $(".add_tag_button").click(function(){
    	object = $(this);

    	caretPosition = $("#id_html").prop("selectionStart");

        value = $("#id_html").val();
        textBefore = value.substring(0,  caretPosition );
        textAfter  = value.substring(caretPosition, value.length);

    	tag = object.attr('name').replace("add_","").replace("_tag","");
    	newValue = textBefore + '<' + tag + '>' + '</' + tag + '>' + textAfter;
    	$("#id_html").val(newValue);
    });

});
