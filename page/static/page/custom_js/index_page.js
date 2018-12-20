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

	$("#modal_submit_page_deletion").click(function(e) {
		let url = '';

		if ($("#wip_article_select").length > 0) {
			url = $("#wip_article_select").val() + "/delete"
		} else {
			url = window.location.href + 'delete';
		}

		$.get({url: url, success: function(data) {
			window.location.href = url;
		}});
	});

	$("#modal_submit_snippet_deletion").click(function(e) {
		let selected_snippet_id = $("#snippets_select").children("option:selected").val()
		let url = '/delete_snippet';

		$.get({url: url, data: { 'snippet_id' : selected_snippet_id }, success: function(data) {
			window.location.href = url;
		}});
	});

	$("#add_snippet_button").click(function(e) {
		let url = 'api/get_snippet_form';

		$.get({url: url, success: function(data) {
			$('#snippet_creation_modal_body').html(data)
			$("#snippet_creation_modal").modal("show");
		}});
	});

	$("#edit_snippet").click(function(e) {
		let selected_snippet_id = $("#snippets_select").children("option:selected").val()

		let url = 'api/get_snippet_form';
		$.post({url: url, data: {'snippet_id' : selected_snippet_id}, success: function(data) {
			$('#snippet_creation_modal_body').html(data)
			$("#snippet_creation_modal").modal("show");
		}});
	});

});
