var indexMap = (function() {
    var map;
  
   
    return {
        init: function(mapDisplayId) {
            map = L.map(mapDisplayId).setView([51.505, -0.09], 13);
            L.tileLayer('http://{s}.tiles.mapbox.com/v3/{id}/{z}/{x}/{y}.png', {
                attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
                maxZoom: 18,
    			id: 'examples.map-i875mjb7'

                }).addTo(map);
        }
    }
    
}());