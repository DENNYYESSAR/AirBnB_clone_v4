$(document).ready(function() {
    // Initialize list of selected amenities
    let selectedAmenities = {};

    // Listen for changes on each input checkbox tag
    $('input[type="checkbox"]').change(function() {
        let amenityId = $(this).data('id');
        let amenityName = $(this).data('name');

        if (this.checked) {
            // Checkbox is checked, add Amenity ID to selectedAmenities
            selectedAmenities[amenityId] = amenityName;
        } else {
            // Checkbox is unchecked, remove Amenity ID from selectedAmenities
            delete selectedAmenities[amenityId];
        }

        // Update the h4 tag inside the div Amenities with the list of Amenities checked
        let amenitiesList = Object.values(selectedAmenities).join(', ');
        $('#amenities h4').text(amenitiesList);
    });
});
