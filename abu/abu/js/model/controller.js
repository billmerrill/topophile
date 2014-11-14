var modelController = (function() {
    "use strict";
    
    var bamService = "http://127.0.0.1:8080/test",
        physicalXDisplay, physicalYDisplay, physicalZDisplay,
        modelCanvas, nwlat, nwlon, selat, selon, zfactor, md,
 
    modelData = function(){
        
        this.currentSizePreset = 'small',
        this.dimensions = {'small': [],
                           'medium': [],
                           'large': [],
                           'custom': []};
        this.accessDimension = function(dim, val) {
            if (val) {
                this.dimensions[this.currentSizePreset][dim] = val;
                return val;
            } else {
                return this.dimensions[this.currentSizePreset][dim]
            }
        };
        this.xSize = function(val) { return this.accessDimension(0,val) };
        this.ySize = function(val) { return this.accessDimension(1,val) };
        this.zSize = function(val) { return this.accessDimension(2,val) };
        this.xDisplay = null;
        this.yDisplay = null;
        this.zDisplay = null;
        this.initDisplay = function(x,y,z){
            this.xDisplay = $(x);
            this.yDisplay = $(y);
            this.zDisplay = $(z);
        };
        this.updateDisplay = function() {
            this.xDisplay.val(this.xSize());
            this.yDisplay.val(this.ySize());
            this.zDisplay.val(this.zSize());
        };
        this.setSize = function(x,y,z) {
            this.dimensions[this.currentSizePreset] = [x,y,z];
        };
        this.initPresets = function() {
            this.dimensions['medium'] = [this.dimensions['small'][0] * 2,
                                         this.dimensions['small'][1] * 2,
                                         this.dimensions['small'][2] * 2];
            this.dimensions['large'] = [this.dimensions['small'][0] * 3,
                                         this.dimensions['small'][1] * 3,
                                         this.dimensions['small'][2] * 3];
            this.dimensions['custom'] = [this.dimensions['small'][0] * 5,
                                         this.dimensions['small'][1] * 5,
                                         this.dimensions['small'][2] * 5];
        }
        this.getCurrentDimensions = function() {
            return this.dimensions[this.currentSizePreset]
        }
        this.changePresetSize = function(newPreset) {
            this.currentSizePreset = newPreset;
            this.updateDisplay();
            // switch(this.currentSizePreset) {
            //     case 'small':
            //         
            //         break;
            //     case 'medium':
            //         break;
            //     case 'large':
            //         break;
            //     case 'custom':
            //         break;
            // }
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
            md.setSize(data['x-size'], data['y-size'], data['z-size']);
            md.initPresets();
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