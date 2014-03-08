function loadMap(){
  $('#home').hide();
  $('#mapcontainer').show();

  var map = L.map('map').setView([-6.3153, 35.15625], 6);

  L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      attribution: '© OpenStreetMap contributors'
    }).addTo(map);

  function addWaterPoint(waterpoint) {
    L.marker([waterpoint.latitude,waterpoint.longitude]).addTo(map)
      .bindPopup(waterpoint);
  }

  $.getJSON( "/reports", function( data ) {
    var items = [];

    //to load all of the data points, remove the '.slice(x,y)
    data.slice(0,100).forEach( function (waterpoint, index) {
      addWaterPoint(waterpoint);
    });
  });
}
