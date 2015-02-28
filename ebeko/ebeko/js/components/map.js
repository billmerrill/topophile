TOPO.BUILD1.Map = (function() {
    "use strict";

    var map, locationFilter, newBoundsCallback, clearedBoundsCallback,
    
    handleNewBounds = function(e) {
        var alterBounds = locationFilter.getBounds();
        if (alterBounds.isValid()) {
            var bounds = {"nwlat": alterBounds.getNorth(),
                         "nwlon": alterBounds.getWest(),
                         "selat": alterBounds.getSouth(),
                         "selon": alterBounds.getEast()};
            var selectionSize = computeSelectionSize(bounds);
            newBoundsCallback(bounds, selectionSize);
        }  
    }, 
    
    computeSelectionSize = function(bounds) {
        var nwpt = getPixelPt(bounds['nwlat'], bounds['nwlon']);
        var sept = getPixelPt(bounds['selat'], bounds['selon']);
        return sept.subtract(nwpt);
    },
    
    /* used for enableMsScaling */
    getPixelPt = function(lat, lon) {
        return map.project(L.latLng(lat, lon));
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
        
        
        showSearchResult: function(data, status) {
            if (data.length > 0) {
                locationFilter.disable();
                var latlng = L.latLng(data[0]['lat'], data[0]['lon']);
                map.setView(latlng, 10);
            } else {
                alert("No place found.");
            }
        },
        
        setSelection: function(bbox) {
            locationFilter.setBounds(bbox);
            if (!locationFilter.isEnabled()) {
                locationFilter.enable();
            }
        },
        
        setUrlBbox: function(bboxText) {
            var extractBounds = function(ghs) {
                var result = false;
                if (ghs.length==25) {
                    var corners = ghs.split('-');
                    if (corners.length == 2) {
                        // woops, topo is nw-se, leaflet is sw-ne
                        var nwc = geohash.decode(corners[0]);
                        var sec = geohash.decode(corners[1]);
                        result = L.latLngBounds(
                            L.latLng(sec[0], nwc[1]),
                            L.latLng(nwc[0], sec[1]));
                    }
                }
               
                return result;
            };
            
            var bbox = extractBounds(bboxText);
            if (bbox != false) {
                if (bbox.isValid()) {
                    locationFilter.setBounds(bbox);
                    if (!locationFilter.isEnabled()) {
                        locationFilter.enable();
                    }
                }
            }
        },
       

        
    }
    
}());