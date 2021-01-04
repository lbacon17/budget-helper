function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 12,
        center: {
            lat: 51.5255337,
            lng: -0.082958
        }
    });

    var labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    var locations = [
        {
            lat: 51.5255337,
            lng: -0.082958
        }
    ]

    var marker = locations.map(function (location, i) {
        return new google.maps.Marker({
            position: location,
            label: labels[i % labels.length]
        });
    });

    var markerCluster = new MarkerClusterer(map, marker,
        { imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m' }
    );
};