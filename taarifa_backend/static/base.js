waterpointMarker = L.Marker.extend({
    options: {
        status: 'unknown'
    }
});

function loadMap() {
    $('#map').height($(window).height() - 50);
    var map = L.map('map').setView([-6.3153, 35.15625], 6);
}

function getReports(callback) {
    $.getJSON("/reports")
        .fail(function (jqxhr, status, error) {
            callback(error, null);
        })
        .done(function (data) {
            callback(null, data);
        });
}

function getDistricts(callback) {
    $.getJSON("/static/tz_districts.geojson")
        .fail(function (jqxhr, status, error) {
            callback(error, null);
        })
        .done(function (data) {
            callback(null, data);
        });
}

function loadData(allDone) {
    async.parallel([
            getReports,
            getDistricts,
        ],
        function (err, results) {
            if (err) throw err;
            initMap(results[0], results[1]);
        }
    );
}

function initMap(waterpoints, districts) {

    //group by lga_name (TODO: assuming equal to district name)
    //TOOD: could be done by db as well
    var wpGrouped = _.groupBy(waterpoints, function (wp) {
        return wp.lga_name.toLowerCase();
    });

    //osm layer
    var osm = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '(c) OpenStreetMap contributors'
    });

    //satellite layer
    var sat = L.tileLayer('http://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        attribution: 'Tiles (c) Esri'
    });

    //main map object
    var map = L.map('map', {
        center: new L.LatLng(-6.3153, 35.15625),
        zoom: 6,
        layers: [osm]
    });

    //geojson layer of the district boundaries as a chloropleth
    var districtLayer = buildDistrictLayer(map, wpGrouped, districts);

    //TODO hardcoded map of status to classes
    var classMap = {
        'functional': 'fixed-cluster',
        'not functional': 'broken-cluster',
        'in progress': 'inprog-cluster',
        'unknown': 'unknown-cluster'
    }

    //leaflet clustering plugin with control over what the clustering icon looks like
    var markers = new L.MarkerClusterGroup({
        iconCreateFunction: function (cluster) {
            var children = cluster.getAllChildMarkers();

            //count the number of markers for each type
            var counts = {};
            children.forEach(function (m) {
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
    }).addTo(map);

    var baseMaps = {
        "Open Street Map": osm,
        "Satellite": sat
    };

    var overlayMaps = {
        "Districts": districtLayer,
        "Markers": markers
    };

    //Legend control
    var legend = L.control.layers(baseMaps, overlayMaps).addTo(map);

    //Now add all the waterpoint markers
    //slice down to speed up testing
    //waterpoints = waterpoints.slice(0,500);
    waterpoints.forEach(function (wp, index) {
        var m = makeWPMarker(wp);
        markers.addLayer(m);
    });
}

function buildDistrictLayer(map, wpGrouped, districts) {
    //heavily based on http://leafletjs.com/examples/choropleth.html
    var districtLayer;

    //little info control that appears when hovering over a district
    var info = L.control();

    info.onAdd = function (map) {
        this._div = L.DomUtil.create('div', 'info');
        this.update();
        return this._div;
    };

    info.update = function (props) {
        var str = "";
        if (props) {
            //get the waterpoint group for this district
            var d = props.District_N.toLowerCase();
            var g = wpGrouped[d];
            str = "No Data";

            if (g) {
                var counts = _.countBy(g, "status");
                str = "<ul><li><b>Functional</b>: " + (counts['functional'] || 0) + "</li>" + "<li><b>Unknown</b>: " + (counts['unknown'] || 0) + "</li>" + "<li><b>Non-functional</b>: " + (counts['not functional'] || 0) + "</li></ul>";
            }
        }

        this._div.innerHTML = '<h4>District</h4>' + (props ?
            '<b>' + props.District_N + '</b><br />' + str : 'Hover over a district');
    };

    info.addTo(map);

    function highlightFeature(e) {
        var layer = e.target;

        layer.setStyle({
            weight: 5,
            color: '#666',
            dashArray: '',
            fillOpacity: 0.7
        });

        if (!L.Browser.ie && !L.Browser.opera) {
            layer.bringToFront();
        }

        var props = layer.feature.properties;
        info.update(props);
    }

    function resetHighlight(e) {
        districtLayer.resetStyle(e.target);
        info.update();
    }

    function zoomToFeature(e) {
        map.fitBounds(e.target.getBounds());
    }

    function onEachFeature(feature, layer) {
        layer.on({
            mouseover: highlightFeature,
            mouseout: resetHighlight,
            click: zoomToFeature
        });
    }

    //The chloropleth shows 5 bands from 0 to 100%
    var colors = ['rgb(255,255,204)', 'rgb(194,230,153)', 'rgb(120,198,121)', 'rgb(49,163,84)', 'rgb(0,104,55)'];
    var grades = _.range(0, 1.25, .25);

    function getColor(val) {
        var idx = _.sortedIndex(grades, val);
        return colors[idx];
    }

    function style(feature) {
        //get the waterpoint group for this district
        var d = feature.properties.District_N.toLowerCase();
        var g = wpGrouped[d];
        var c = '#808080'; //if no data, use gray

        if (g) {
            var n = g.length;
            //what percentage are functional
            var counts = _.countBy(g, "status");
            perc = counts["functional"] / n * 1.0;
            c = getColor(perc);
        }

        return {
            fillColor: c,
            weight: 2,
            opacity: 1,
            color: 'white',
            fillOpacity: 0.7
        };
    }

    //the layer itself
    districtLayer = L.geoJson(districts, {
        style: style,
        onEachFeature: onEachFeature
    }).addTo(map);

    //a legend for the chloropleth colours
    var legend = L.control({
        position: 'bottomright'
    });

    legend.onAdd = function (map) {
        var div = L.DomUtil.create('div', 'info legend');
        div.innerHTML += "<h4>Functional</h4>";
        // loop through our density intervals and generate a label with a colored square for each interval
        grades.forEach(function (g) {
            div.innerHTML += '<i style="background:' + getColor(g) + '"></i> ' + g * 100 + "%<br />";
        });

        return div;
    };

    legend.addTo(map);

    return districtLayer;
}

function makeWPMarker(waterpoint) {
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

    return marker;
}

$(window).resize(function() {
  $('#map').height($(window).height() - 50);
});
