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
    },
    
    loadGeoJson = function() {
        $.ajax({
            type: 'GET',
            url: "assets/data-mask.json"
        })
        .done(function(data, status, ctx) {
            L.geoJson(data, {
                style: function (feature) {
                    return { fill: true, fillColor: '#fff', color: '#fff',
                             stroke: false, opacity: 0, fillOpacity:.5};
                },
                onEachFeature: function(feature, layer) {
                    layer.bindPopup("No data, yet. ");
                    return layer;
                }
            }).addTo(map);
        })
        .fail(function(data, status, ctx) {
            console.log("geojson ajax failure");
        })
    };
    
    
    
    return {
        init: function(mapDisplayId, mapCenter, newBoundsCb, clearedBoundsCb) {
            newBoundsCallback = newBoundsCb;
            clearedBoundsCallback = clearedBoundsCb
            
            var imageUrl = '/assets/fakemask.png',
                imageBounds = [[-50, -180], [60, 179]];

            var noData = L.imageOverlay(imageUrl, imageBounds, {'opacity':.5});

            loadGeoJson();
            
            // Abu coords:   center: [ 34.5, 131.6 ],
            map = L.map(mapDisplayId, {
              layers: MQ.hybridLayer(), 
              center: mapCenter, // mt rainier
              zoom: 12,
              minZoom: 2,
              maxBounds: L.latLngBounds(L.latLng(-60, -180),
                                        L.latLng(70, 180))} );
             
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
                if (clearedBoundsCallback) {
                    clearedBoundsCallback();
                }
            });



            
        },
        
        
        showSearchResult: function(data, status) {
            if (data.length > 0) {
                locationFilter.disable();
                var latlng = L.latLng(data[0]['lat'], data[0]['lon']);
                map.setView(latlng, 13);
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
