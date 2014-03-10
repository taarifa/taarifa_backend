function loadMap(){
  var map = L.map('map').setView([-6.3153, 35.15625], 6);

  L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      attribution: '(c) OpenStreetMap contributors'
  }).addTo(map);

  //leaflet clustering plugin with control over what the clustering icon looks like
  var markers = new L.MarkerClusterGroup({
    iconCreateFunction: function(cluster) {
      var children = cluster.getAllChildMarkers();
      var childCount = cluster.getChildCount();

      //TODO loop over the children and determine the status of the cluster

      //Using std divicon but could use something else
      return new L.DivIcon({
        html: '<div><span>' + childCount + '</span></div>',

             //TODO use all-broken-cluster, all-fixed-cluster, or mixed-cluster here depending on the status of the child waterpoints
             //even better: single class with interpolation over the colour

             className: 'leaflet-marker-icon marker-cluster marker-cluster-medium leaflet-zoom-animated leaflet-clickable',
             iconSize: new L.Point(40, 40)
      });
    }
  });

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
