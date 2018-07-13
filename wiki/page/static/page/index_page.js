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

	function AutocompleteSelectedHandler(event) {
		$.get("api/get_pages_by_tag/", JSON.stringify($(event.target).val()));
	}
});