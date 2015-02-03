TOPO.BUILD1.indexPage = (function() {
    "use strict";
    
    var map = TOPO.BUILD1.Map,
        terrain = TOPO.BUILD1.Terrain,
        geocoder = TOPO.BUILD1.Geocoder,
        exaggerater = TOPO.BUILD1.Exaggerater,
        model = TOPO.BUILD1.Model,  
        pricing = TOPO.BUILD1.Pricing,
        sizing = TOPO.BUILD1.Sizing,
        printer = TOPO.BUILD1.Printer,
        firstBounds = true,
        currentModelId,
        
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
        
        presetChangeHandler = function(data) {
            switch (data['preset']) {
                case 'small':
                    model.scaleReferenceObject(1);
                    pricing.updatePrice(currentModelId, 1.0);
                    break;
                case 'medium': 
                    model.scaleReferenceObject(.5);
                    pricing.updatePrice(currentModelId, 2.0);
                    break;
                case 'large': 
                    model.scaleReferenceObject(1.0/3.0);
                    pricing.updatePrice(currentModelId, 3.0);
                    break;
                case 'custom': 
                    model.scaleReferenceObject(.2);
                    pricing.updatePrice(currentModelId, 5.0);
                    break;
            }
        },
        
        newTerrainHandler = function() {
            $('#build-model').prop('disabled', false);
        },
        
        newModelHandler = function(modelData) {
            sizing.setSize(modelData['x-size-mm'], modelData['y-size-mm'], modelData['z-size-mm']);
            pricing.updatePrice(modelData['model_id']);
            currentModelId = modelData['model_id'];
            $("#print-model").prop('disabled', false);
        },
        
        initComponents = function() {
            map.init("map", TOPO.BUILD1.getConfig('mapStartPoint'), newBoundsHandler);
            terrain.init("terrain-canvas", TOPO.BUILD1.getConfig('elExaggeration'), "terrain-progress", newTerrainHandler);
            geocoder.init(map.showSearchResult, "gc-search", "gc-search-button");
            exaggerater.init(TOPO.BUILD1.getConfig('elExaggerate'), 'exag', 'height-factor', 'zfactor')
            pricing.init('white_plastic_price');
            sizing.init(presetChangeHandler, '#xsize', '#ysize', '#zsize', '#small-size-preset',
                        '#medium-size-preset', '#large-size-preset', '#custom-size-preset', 
                        '#toggle-size-comparison');
            printer.init();
            model.init(newModelHandler, 'model-canvas', 'model-progress', 'toggle-size-comparison', 'reset-view');
        },
        
        initElements = function() {
            $('#build-model').click(function() {
                model.renderModel(getModelSpec())
            }).prop('disabled', true);
            
            $('#model-sizes').click(function() {
                sizing.toggleUnits();
            });
            
            $('#print-model').click(function() {
                console.log("printit");
                printer.upload(currentModelId);
            }).prop('disabled', true);
        }
        
    
    return {
        init: function() {
            initComponents();
            initElements();
        }
    }
}());