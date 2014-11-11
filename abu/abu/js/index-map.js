var indexMap = (function() {
    var map, locationFilter, newBBoxCallback, clearedBBoxCallback,
    
    handleNewBounds = function(e) {
        var alterBounds = locationFilter.getBounds();
        if (alterBounds.isValid()) {
            newBBoxCallback({"nwlat": alterBounds.getNorth(),
                         "nwlon": alterBounds.getWest(),
                         "selat": alterBounds.getSouth(),
                         "selon": alterBounds.getEast()});
        }  
    };
    
    
    
    return {
        init: function(mapDisplayId, mapCenter, newBBoxCb, clearedBBoxCb) {
            newBBoxCallback = newBBoxCb;
            clearedBBoxCallback = clearedBBoxCb
            
            // Abu coords:   center: [ 34.5, 131.6 ],
            map = L.map(mapDisplayId, {
              layers: MQ.hybridLayer(),
              center: mapCenter, // mt rainier
              zoom: 12 } );
             
            var lfOptions = {'adjustButton': null,
                             'buttonPosition': 'topright'};
            locationFilter = new L.LocationFilter(lfOptions).addTo(map);
            
            locationFilter.on("change", function(e) {
                handleNewBounds();
            }); 
            locationFilter.on("enabled", function(e) {
                handleNewBounds();
            }); 
            
            locationFilter.on("disabled", function(e) {
                locationFilter.clearBounds();
                clearedBBoxCallback();
            });
        },
        
        showSearchResult: function(lat, lon) {
            var latlng = L.latLng(lat, lon);
            map.setView(latlng, 10);
        }
    }
    
}());