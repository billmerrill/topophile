TOPO.BUILD1.indexPage = (function() {
    "use strict";
    
    var map = TOPO.BUILD1.Map,
        terrain = TOPO.BUILD1.Terrain,
        geocoder = TOPO.BUILD1.Geocoder,
        exaggerater = TOPO.BUILD1.Exaggerater,
        firstBounds = true,
        zFactorDisplay,

        newBoundsHandler = function(newBounds) {
            if (firstBounds) {
                $("#terrain-instructions").hide();        
                firstBounds = false;
            }
            terrain.renderBounds(newBounds);
        },
        
        initComponents = function() {
            map.init("map", TOPO.BUILD1.getConfig('mapStartPoint'), newBoundsHandler);
            terrain.init("terrain-canvas", TOPO.BUILD1.getConfig('elExaggeration'), "terrain-progress");
            geocoder.init(map.showSearchResult, "gc-search", "gc-search-button");
            exaggerater.init(TOPO.BUILD1.getConfig('elExaggerate'), 'exag', 'height-factor', 'zfactor')
        },
        
    
    return {
        init: function() {
            initComponents();
        }
    }
}());