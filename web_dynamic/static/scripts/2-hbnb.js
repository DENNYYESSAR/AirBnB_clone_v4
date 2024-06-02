$(document).ready(function() {
    // Call API to check status
    $.getJSON('http://0.0.0.0:5001/api/v1/status/', function(data) {
        // If status is "OK", add class "available" to #api_status
        if (data.status === "OK") {
            $('#api_status').addClass('available');
        } else {
            // Otherwise, remove class "available" from #api_status
            $('#api_status').removeClass('available');
        }
    });
});
