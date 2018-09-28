$( document ).ready(function() {
	$("#page_tag_search").autocomplete({
		source: "api/get_page_tags",
		select: function(event) {
			// send a search query using the tag value and the value from the title search field
			SendSearchQuery($(event.target).val(), $('#page_title_search').val());
		},
		minLength: 2,
	});

	$("#page_tag_search").keyup(function(e) {
		if (e.keyCode == 13) {
			SendSearchQuery($(this).val(), $("#page_title_search").val());
		}
	});

	$("#page_title_search").keyup(function(e) {
		if (e.keyCode == 13) {
			SendSearchQuery($("#page_tag_search").val(), $(this).val());
		}
	});

	function SendSearchQuery(tagTerm, titleTerm) {
		data = {};

		if (tagTerm) {
			if (titleTerm) {
				data = {'tag_term' : tagTerm, 'title_term' : titleTerm};
			} else {
				data = {'tag_term' : tagTerm};
			}
		} else if(titleTerm) {
			data = {'title_term' : titleTerm};
		}

		$.get("api/get_search_pages/", data, function(data) { $('#page_list').html(data); });
	}

	$("#goon_wip_article").click(function(e) {
		let url = $("#wip_article_select").val() + "/edit";
		$.get({url: url, success: function(data) {
			window.location.href = url;
		}});

	});

});