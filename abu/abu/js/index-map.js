var indexMap = (function() {
    var map, locationFilter, newBBoxCallback;
    
    return {
        init: function(mapDisplayId, newBBoxCb) {
            newBBoxCallback = newBBoxCb;
            
            // Abu coords:   center: [ 34.5, 131.6 ],
            map = L.map(mapDisplayId, {
              layers: MQ.hybridLayer(),
              center: [ 46.852947, -121.760424 ], // mt rainier
              zoom: 12 } );
             
            var lfOptions = {'adjustButton': null,
                             'buttonPosition': 'topright'};
            locationFilter = new L.LocationFilter(lfOptions).addTo(map);
            locationFilter.on("change", function (e) {
                    var alterBounds = locationFilter.getBounds();
                    newBBoxCallback({"nwlat": alterBounds.getNorth(),
                                     "nwlon": alterBounds.getWest(),
                                     "selat": alterBounds.getSouth(),
                                     "selon": alterBounds.getEast()});
            });
            
            locationFilter.on("disabled", function(e) {
                locationFilter.clearBounds();
            });
        },
        
        showSearchResult: function(lat, lon) {
            var latlng = L.latLng(lat, lon);
            map.setView(latlng, 10);
        }
    }
    
}());