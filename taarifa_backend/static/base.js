function loadMap(){
  $('#home').hide();
  $('#mapcontainer').show();

  var map = L.map('map').setView([-6.3153, 35.15625], 6);

  L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      attribution: '© OpenStreetMap contributors'
    }).addTo(map);

  var markers = L.markerClusterGroup();

  function addWaterPoint(waterpoint) {
    markers.addLayer(L.marker([waterpoint.latitude,waterpoint.longitude]));
  }
  map.addLayer(markers);

  $.getJSON( "/reports", function( data ) {
    var items = [];

    data.forEach( function (waterpoint, index) {
      addWaterPoint(waterpoint);
    });
  });
}
