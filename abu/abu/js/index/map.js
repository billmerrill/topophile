var indexMap = (function() {
    "use strict";

    var map, locationFilter, newBoundsCallback, clearedBoundsCallback,
    
    handleNewBounds = function(e) {
        var alterBounds = locationFilter.getBounds();
        if (alterBounds.isValid()) {
            newBoundsCallback({"nwlat": alterBounds.getNorth(),
                         "nwlon": alterBounds.getWest(),
                         "selat": alterBounds.getSouth(),
                         "selon": alterBounds.getEast()});
        }  
    };
    
    
    
    return {
        init: function(mapDisplayId, mapCenter, newBoundsCb, clearedBoundsCb) {
            newBoundsCallback = newBoundsCb;
            clearedBoundsCallback = clearedBoundsCb
            
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
                clearedBoundsCallback();
            });
        },
        
        showSearchResult: function(lat, lon) {
            var latlng = L.latLng(lat, lon);
            map.setView(latlng, 10);
        }
    }
    
}());