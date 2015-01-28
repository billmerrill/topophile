TOPO.BUILD1.indexPage = (function() {
    "use strict";
    
    var map = TOPO.BUILD1.Map,
        terrain = TOPO.BUILD1.Terrain,
        firstBounds = true,
        
        newBoundsHandler = function(newBounds) {
            if (firstBounds) {
                firstBounds = false;
            }
            previewTopo();
        },
        
        initComponents = function() {
            // map.init("map", TOPO.BUILD1.getConfig('mapStartPoint'), newBoundsHandler, clearedBoundsHandler);
            map.init("map", TOPO.BUILD1.getConfig('mapStartPoint'));
            terrain.init("terrain-canvas", TOPO.BUILD1.getConfig('elExaggeration'), "terrain-progress");
        };
    
    
    return {
        init: function() {
            initComponents();
            
        }
    }
}());