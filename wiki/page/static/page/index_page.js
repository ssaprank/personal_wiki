$( document ).ready(function() {
	$("#page_tag_search").autocomplete({
		source: "api/get_page_tags",
		select: function(event) {
			AutocompleteSelectedHandler(event);
		},
		minLength: 2,
	});

	$("#page_tag_search").keyup(function(e) {
		if (e.keyCode == 13) {
			AutocompleteSelectedHandler(e)
		}
	});

	$("#page_title_search").keyup(function(e) {
		if (e.keyCode == 13) {
			$.get(
			"api/get_search_pages/",
			{'search_element': 'title', 'term': $(event.target).val()},
			  function(data){
			  	$('#page_list').html(data);
			  });
		}
	});

	function AutocompleteSelectedHandler(event) {
		$.get(
			"api/get_search_pages/",
			{'search_element': 'tag', 'term': $(event.target).val()},
			  function(data){
			  	$('#page_list').html(data);
			  });
	}
});