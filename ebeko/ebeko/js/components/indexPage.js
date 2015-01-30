TOPO.BUILD1.indexPage = (function() {
    "use strict";
    
    var map = TOPO.BUILD1.Map,
        terrain = TOPO.BUILD1.Terrain,
        geocoder = TOPO.BUILD1.Geocoder,
        exaggerater = TOPO.BUILD1.Exaggerater,
        model = TOPO.BUILD1.Model,  
        pricing = TOPO.BUILD1.Pricing,
        sizing = TOPO.BUILD1.Sizing,
        firstBounds = true,
        
        getModelSpec = function () {
            var modelSpec = terrain.getBounds();
            modelSpec['zfactor'] = exaggerater.getFactor();
            return modelSpec;
        },
                     
        newBoundsHandler = function(newBounds) {
            if (firstBounds) {
                $("#terrain-instructions").hide();        
                firstBounds = false;
            }
            terrain.renderBounds(newBounds);
        },
        
        presetChangeHandler = function() {
            
        },
        
        newModelHandler = function(modelData) {
            // modelCanvas.showModel(data['url'], data['x-size-mm']);
            // sizeTools.setSize(data['x-size-mm'], data['y-size-mm'], data['z-size-mm']);
            // sizeTools.initPresets();
            // currentModelId = data['model_id'];
            // setSendButton(data['model_id'] + ".stl");
            // setPricing(data['model_id'])    
            
            sizing.setSize(modelData['x-size-mm'], modelData['y-size-mm'], modelData['z-size-mm']);
            pricing.updatePrice(modelData['model_id']);
        },
        
        initComponents = function() {
            map.init("map", TOPO.BUILD1.getConfig('mapStartPoint'), newBoundsHandler);
            terrain.init("terrain-canvas", TOPO.BUILD1.getConfig('elExaggeration'), "terrain-progress");
            geocoder.init(map.showSearchResult, "gc-search", "gc-search-button");
            exaggerater.init(TOPO.BUILD1.getConfig('elExaggerate'), 'exag', 'height-factor', 'zfactor')
            pricing.init('white_plastic_price');
            sizing.init(presetChangeHandler, '#xsize', '#ysize', '#zsize', '#small-size-preset',
                        '#medium-size-preset', '#large-size-preset', '#custom-size-preset', 
                        '#toggle-size-comparison');
            model.init(newModelHandler, 'model-canvas', 'model-progress', 'toggle-size-comparison', 'reset-view');
        },
        
        initElements = function() {
            $('#build-model').click(function() {
                model.renderModel(getModelSpec())
            })
        }
        
    
    return {
        init: function() {
            initComponents();
            initElements();
        }
    }
}());