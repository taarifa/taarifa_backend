function loadMap(){
  var map = L.map('map').setView([-6.3153, 35.15625], 6);

  L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      attribution: '(c) OpenStreetMap contributors'
  }).addTo(map);

  var markers = L.markerClusterGroup();
  map.addLayer(markers);

  function addWaterPoint(waterpoint) {

    //TODO: set color depending on the waterpoint status
    var color = 'blue';

    var icon = L.AwesomeMarkers.icon({
        prefix: 'glyphicon',
        icon: 'tint',
        markerColor: color
    });

    //TODO: use status
    var popupTxt = ("<b>Waterpoint: " + waterpoint.id + "</b><br>Status: unknown.");

    //TODO: attach the status to the marker so other code can use this (e.g., clustering)
    var marker = L.marker([waterpoint.latitude,waterpoint.longitude], {icon: icon});
    marker.bindPopup(popupTxt);
    markers.addLayer(marker);
  }


  $.getJSON( "/reports", function( data ) {
    //slice down to speed up testing
    //data = data.slice(0,500);
    data.forEach( function (waterpoint, index) {
      addWaterPoint(waterpoint);
    });
  });
}
