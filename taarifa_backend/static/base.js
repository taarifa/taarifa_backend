waterpointMarker = L.Marker.extend({
    options: {
        status: 'unknown'
    }
});

function loadMap() {
    $('#map').height($(window).height() - 50);
    var map = L.map('map').setView([-6.3153, 35.15625], 6);

    L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '(c) OpenStreetMap contributors'
    }).addTo(map);

    //TODO hardcoded map of status to classes
    var classMap = {
        'functional': 'fixed-cluster',
        'not functional': 'broken-cluster',
        'in progress': 'inprog-cluster',
        'unknown': 'unknown-cluster'
    }

    //leaflet clustering plugin with control over what the clustering icon looks like
    var markers = new L.MarkerClusterGroup({
        iconCreateFunction: function(cluster) {
            var children = cluster.getAllChildMarkers();

            //count the number of markers for each type
            var counts = {};
            children.forEach(function(m) {
                counts[m.options.status] = (counts[m.options.status] + 1) || 1;
            });

            //take the status with the highest count
            var max_key = _.invert(counts)[_.max(counts)];
            //get the matching class
            var cls = classMap[max_key];

            //Using std divicon but could use something else
            return new L.DivIcon({
                html: '<div><span>' + children.length + '</span></div>',

                className: 'leaflet-marker-icon marker-cluster marker-cluster-medium leaflet-zoom-animated leaflet-clickable ' + cls,
                iconSize: new L.Point(40, 40)
            });
        }
    });

    map.addLayer(markers);

    function addWaterPoint(waterpoint) {
        var status = waterpoint.status;

        //set color depending on the waterpoint status
        //TODO use the defined classes instead of hardcoding colors?
        var color = 'black';
        if (status == 'functional') {
            color = 'blue';
        } else if (status == 'not functional') {
            color = 'red';
        } else if (status == 'in progress') {
            color = 'green';
        } else if (status == 'unknown') {
            color = 'orange';
        } else {}

        var icon = L.AwesomeMarkers.icon({
            prefix: 'glyphicon',
            icon: 'tint',
            markerColor: color
        });

        var popupTxt = ("<b>Waterpoint: " + waterpoint.id + "</b><br>Status: " + status);

        var marker = new waterpointMarker([waterpoint.latitude, waterpoint.longitude], {
            icon: icon,
            status: status
        });
        marker.bindPopup(popupTxt);
        markers.addLayer(marker);
    }


    $.getJSON("/reports", function(data) {
        //slice down to speed up testing
        //data = data.slice(0,500);
        data.forEach(function(waterpoint, index) {
            addWaterPoint(waterpoint);
        });
    });
}

$(window).resize(function() {
  $('#map').height($(window).height() - 50);
});
