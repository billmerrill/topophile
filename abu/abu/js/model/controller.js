var modelController = (function() {
    "use strict";
    
    var bamService = "http://127.0.0.1:8080",
        swPriceSerivce = "http://127.0.0.1:8080/price",
        physicalXDisplay, physicalYDisplay, physicalZDisplay,
        comparisonButton,
        resetViewButton,
        modelCanvas, 
        nwlat, nwlon, selat, selon, zfactor, sizeTools,
  
    presetChangeHandler = function(data) {
        switch (data['preset']) {
            case 'small':
                modelCanvas.scaleReferenceObject(1);
                break;
            case 'medium': 
                modelCanvas.scaleReferenceObject(.5);
                break;
            case 'large': 
                modelCanvas.scaleReferenceObject(1.0/3.0);
                break;
            case 'custom': 
                modelCanvas.scaleReferenceObject(.2);
                break;
        }
    },
    
    getParams = function() {
        var url = document.location;
        var searchObject = {},
            queries, split, i;

        queries = document.location.search.replace(/^\?/, '').split('&');
        for( i = 0; i < queries.length; i++ ) {
            split = queries[i].split('=');
            searchObject[split[0]] = split[1];
        }
        return searchObject;
    },

    getModelUrl = function() {
        $("#model-building").show();
        $.ajax({
            type: "GET",
            url: bamService,
            data: { 'nwlat': nwlat,
                    'nwlon': nwlon,
                    'selat': selat,
                    'selon': selon,
                    'size': 100, //always 100
                    'rez': 400, //400 dots per 100 mm ~= 100dpi
                    'zfactor': zfactor,
                    'price': 'e'}
        })
        .done(function(data, status, jqxhr) {
            window.console.log(data)
            modelCanvas.showModel(data['url'], data['x-size-mm']);
            sizeTools.setSize(data['x-size-mm'], data['y-size-mm'], data['z-size-mm']);
            sizeTools.initPresets();
            $("#white_plastic_price").html(data['price'][6]['price'])
        })
        .fail(function(data, stats, error) {
            alert("Sorry, I couldn't build a model.")
        })
        .always(function(data) {
            $("#model-building").hide();
            $("#model-canvas").show()
        });
    },
    
    initComponents = function() {
        modelCanvas.init("model-canvas", referenceObjects);
        sizeTools.init(presetChangeHandler, '#xsize', '#ysize', '#zsize', '#small-size-preset',
                    '#medium-size-preset', '#large-size-preset', '#custom-size-preset', 
                    '#toggle-size-comparison');
    },
    
    initUi = function() {
        $('#model-building').hide();
        physicalXDisplay = $('#xsize')
        physicalYDisplay = $('#ysize')
        physicalZDisplay = $('#zsize')
        comparisonButton = $('#toggle-size-comparison');
        comparisonButton.click(function(e) {
            modelCanvas.toggleSizeReference();
            modelCanvas.resetScene();
        })
        resetViewButton = ($('#reset-view'));
        resetViewButton.click(function(e) {
            modelCanvas.resetScene();
        })
    },
    
    fakeUpData = function() {
        nwlat = 46.9290278;
        nwlon = -121.8229167;
        selat = 46.7762500;
        selon = -121.6701389;
        zfactor = 1.5;
    }, 
    
    initPage = function() {
        getModelUrl();
    },
    
    initInput = function() {
        var params = getParams();
        nwlat = params['nwlat'];
        nwlon = params['nwlon'];
        selat = params['selat'];
        selon = params['selon'];
        zfactor = params['zfactor'];
    };
    
   
    return {
        init: function(modelModule, sizingModule, objectModule) {
            initInput();
            modelCanvas = modelModule;
            sizeTools = sizingModule;
            referenceObjects = objectModule;
            
            initComponents();
            initUi();
            
            // fakeUpData();
            // modelCanvas.showChit();
            initPage();
            
        }
    }
    
}());