var modelController = (function() {
    "use strict";
    
    var bamService = "http://127.0.0.1:8080/test",
        physicalXDisplay, physicalYDisplay, physicalZDisplay,
        modelCanvas, nwlat, nwlon, selat, selon, zfactor, md,
 
    modelData = function(){
        
        this.xSize = 0;
        this.ySize = 0;
        this.zSize = 0;
        this.xDisplay = null;
        this.yDisplay = null;
        this.zDisplay = null;
        this.currentSizePreset = 'small',
        this.initDisplay = function(x,y,z){
            this.xDisplay = $(x);
            this.yDisplay = $(y);
            this.zDisplay = $(z);
        }
        this.updateDisplay = function() {
            this.xDisplay.val(this.xSize);
            this.yDisplay.val(this.ySize);
            this.zDisplay.val(this.zSize);
        }
        this.setSize = function(x,y,z) {
            this.xSize = x;
            this.ySize = y;
            this.zSize = z;
        };
        this.changePresetSize = function(newPreset) {
            this.currentSizePreset = newPreset;
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
                    'size': 200, 
                    'rez': 400,
                    'zfactor': zfactor}
        })
        .done(function(data, status, jqxhr) {
            modelCanvas.showModel(data['url']);
            md.setSize(model['x-size'], model['y-size'], model['z-size']);
            md.updateDisplay();
            $("#build-model").prop('disabled', false);

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
        modelCanvas.init("model-canvas");
    },
    
    initUi = function() {
        $('#model-building').hide();
        physicalXDisplay = $('#xsize')
        physicalYDisplay = $('#ysize')
        physicalZDisplay = $('#zsize')
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
    };
   
    return {
        init: function(modelModule) {
            md = new modelData();
            md.initDisplay('#xsize', '#ysize', '#zsize')
            
            modelCanvas = modelModule;
            initComponents();
            initUi();
            
            fakeUpData();
            initPage();
            
        }
    }
    
}());