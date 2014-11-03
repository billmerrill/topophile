var indexMap = (function() {
    var map, newBBoxCallback;
    
    return {
        init: function(mapDisplayId, newBBoxCb) {
            newBBoxCallback = newBBoxCb;
            
            // Abu coords:   center: [ 34.5, 131.6 ],
            map = L.map(mapDisplayId, {
              layers: MQ.hybridLayer(),
              center: [ 46.852947, -121.760424 ], // mt rainier
              zoom: 12 } );
              
        },
        
        showSearchResult: function(lat, lon) {
            var latlng = L.latLng(lat, lon);
            map.setView(latlng, 10);
        }
    }
    
}());