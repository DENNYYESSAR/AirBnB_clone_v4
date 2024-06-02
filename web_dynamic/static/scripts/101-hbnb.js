$(document).ready(function() {
    $.getJSON('http://0.0.0.0:5001/api/v1/status/', function(data) {
        if (data.status === "OK") {
            $('#api_status').addClass('available');
        }
    });

    $('#search_button').click(function() {
        var amenities = [];
        $('.amenity:checked').each(function() {
            amenities.push($(this).data('id'));
        });

        var states = [];
        $('.state:checked').each(function() {
            states.push($(this).data('id'));
        });

        var cities = [];
        $('.city:checked').each(function() {
            cities.push($(this).data('id'));
        });

        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            url: 'http://0.0.0.0:5001/api/v1/places_search/',
            data: JSON.stringify({'amenities': amenities, 'states': states, 'cities': cities}),
            success: function(data) {
                $('.places').empty();
                for (var i = 0; i < data.length; i++) {
                    var place = data[i];
                    var article = '<article>' +
                                    '<div class="
