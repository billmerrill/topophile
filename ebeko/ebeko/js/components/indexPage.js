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
            modelSpec.zfactor = exaggerater.getFactor();
            modelSpec.modelSize = sizing.getCurrentSize();
            return modelSpec;
        },
        
        setUrl = function(newBounds) {
            var newurl = document.location.origin + document.location.pathname  
                        + "?b=" 
                        + geohash.encode(newBounds['nwlat'], newBounds['nwlon'])  
                        + '-'
                        + geohash.encode(newBounds['selat'], newBounds['selon']);
            history.pushState(null, null, newurl);
        },
                     
        newBoundsHandler = function(newBounds) {
            if (firstBounds) {
                $("#terrain-instructions").hide();        
                firstBounds = false;
            }
            terrain.renderBounds(newBounds);
            setUrl(newBounds);  
        },
        
        presetChangeHandler = function(data) {
            model.resizeModel(getModelSpec());
            switch (data['preset']) {
                case 'small':
                    // model.scaleReferenceObject(1);
                    break;
                case 'medium': 
                    // model.scaleReferenceObject(.5);
                    break;
                case 'large': 
                    // model.scaleReferenceObject(1.0/3.0);
                    break;
                case 'custom': 
                    // model.scaleReferenceObject(.2);
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
            terrain.init("terrain-canvas", TOPO.BUILD1.getConfig('elExaggeration'), "terrain-progress", newTerrainHandler, 'terrain-reset');
            geocoder.init(map.showSearchResult, "gc-search", "gc-search-button");
            exaggerater.init(TOPO.BUILD1.getConfig('elExaggerate'), 'exag', 'height-factor', 'zfactor')
            pricing.init('white_plastic_price');
            sizing.init(presetChangeHandler, '#x', '#y', '#z', '#small-size-preset',
                        '#medium-size-preset', '#large-size-preset', '#custom-size-preset', 
                        '#toggle-size-comparison');
            printer.init();
            model.init(newModelHandler, 'model-canvas', 'model-progress', 'toggle-size-comparison', 'model-reset');
        },
        
        initElements = function() {
            $('#build-model').click(function() {
                sizing.resetPresets();
                pricing.clearPrice();
                model.renderModel(getModelSpec())
            }).prop('disabled', true);
            
            $('#threewrapper').click(function() {
                sizing.toggleUnits();
            });
            
            $('#print-model').click(function() {
                console.log("printit");
                printer.upload(currentModelId);
            }).prop('disabled', true);
        },
        
        initUrl = function() {
            var getParams = function() {
                var searchObject = {}, queries, split, i;

                queries = document.location.search.replace(/^\?/, '').split('&');
                for( i = 0; i < queries.length; i++ ) {
                    split = queries[i].split('=');
                    searchObject[split[0]] = split[1];
                }
                return searchObject;
            };
            
            var getBounds = function(ghs) {
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
            
            var params = getParams()
            if ('b' in params) {
                map.setUrlBbox(params['b']);
            }
        }
        
    
    return {
        init: function() {
            initComponents();
            initElements();
            initUrl();
        }
    }
}());