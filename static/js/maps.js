function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 13,
        center: {
            lat: 51.49360,
            lng: -0.19204
        }
    });

    var labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    var locations = [
        {
            lat: 51.49360,
            lng: -0.19204
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