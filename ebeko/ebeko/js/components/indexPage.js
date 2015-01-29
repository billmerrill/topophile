TOPO.BUILD1.indexPage = (function() {
    "use strict";
    
    var map = TOPO.BUILD1.Map,
        terrain = TOPO.BUILD1.Terrain,
        geocoder = TOPO.BUILD1.Geocoder,
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
            geocoder.init(map.showSearchResult);
        },
        
        initElements = function() {
            $("#gc-search-button").click(
                function() {geocoder.search($("#gc-search").val())}
            );
            $("#gc-search").keyup(function(e){
                if(e.keyCode == 13) {
                    geocoder.search($("#gc-search").val());
                }});
                
                
            zFactorDisplay = $("#zfactor");
            
            zFactorDisplay.val("1.5");
            
            $('#exag').on('change', function(e) {
                console.log('exag change', e);
                if (e.target.id == 'zfactor') {
                    var val = parseFloat(e.target.value);
                    terrain.updateZFactor(val);
                    if ((val >= .1) && (val <= 10)) {
                        $('#height-factor').slider('setValue', val);
                    }
                } else {
                    var val = e.value.newValue;
                    terrain.updateZFactor(val);
                    zFactorDisplay.val(val)
                }
            });
            
            $('#height-factor').slider();
        };
        
    
    
    return {
        init: function() {
            initComponents();
            initElements();
        }
    }
}());