$( document ).ready(function() {
	let editPageButton = $("#edit_page_button");
	let bottomButtonRow = $("#bottom_button_row");
	if (!bottomButtonRow.isInViewport()) {
		editPageButton.addClass('fixed-bottom');
		editPageButton.addClass('m-3');
	}

	$(window).on('resize scroll', function() {
		applyFixedClassOnEditPageButton();
	});

	function applyFixedClassOnEditPageButton() {
		if (bottomButtonRow.isInViewport()) {
			editPageButton.removeClass('m-3');
			editPageButton.removeClass('fixed-bottom');
		} else {
			editPageButton.addClass('fixed-bottom');
			editPageButton.addClass('m-3');
		}
	}
});