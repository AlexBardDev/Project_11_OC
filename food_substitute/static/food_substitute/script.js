// Submit the form after the click on the button
$("#about button").on("click", function () {
	$("#about form").submit();
});

// Enable tootips
$(function () {
  $('[data-toggle="tooltip"]').tooltip();
});

// Remove a DOM element after 3 seconds
if ($(".special_message")) {
  setTimeout(function () {
    $(".special_message").remove();
  }, 3000);
};
