TOPO.BUILD1.Sizing = (function(){
    "use strict";
    
    var currentUnits = 'm',
        presetChangeCallback, currentSizePreset = 'small',
        dimensions = {'small': [],
                       'medium': [],
                       'large': [],
                       'custom': []},
        modelSizes = {'small': 50,
                     'medium': 100,
                     'large': 200,
                     'custume': 250},
                       
        accessDimension = function(dim, val) {
            if (val) {
                dimensions[currentSizePreset][dim] = val;
                return val;
            } else {
                return dimensions[currentSizePreset][dim]
            }
        },
        
        changePresetSize = function(newPreset) {
            currentSizePreset = newPreset;
            updateDisplay();
            var cbData = {
                'preset': newPreset,
                'x': xSize(),
                'y': ySize(),
                'z': zSize()
            }
            presetChangeCallback(cbData);
        },
    
        showCurrentDimensions = function() {
            if (currentUnits == 'm') {
                showMetricDimensions();
            } else {
                showImperialDimensions();
            }
        },
       
        showImperialDimensions = function () {
            $(".size-cm").hide();
            $(".size-in").show();    
            currentUnits = 'i';
        },
        
        showMetricDimensions = function () {
            $(".size-cm").show();
            $(".size-in").hide();    
            currentUnits = 'm';
        },
        
        makeDisplayDimension = function(mmval) {
            var cmval = (mmval / 10.0).toPrecision(3);
            var inval = (mmval / 25.4).toPrecision(3);
            return '<span class="size-cm">'+cmval+'</span><span class="size-in">'+inval+'<span>';
        },
        
        updateDisplay =  function() {
            xDisplay.html(makeDisplayDimension(xSize()));
            yDisplay.html(makeDisplayDimension(ySize()));
            zDisplay.html(makeDisplayDimension(zSize()));
            showCurrentDimensions();
        },
        
        updatePresets = function() {
            dimensions['medium'] = [dimensions['small'][0] * 2,
                                     dimensions['small'][1] * 2,
                                     dimensions['small'][2] * 2];
            dimensions['large'] = [dimensions['small'][0] * 3,
                                     dimensions['small'][1] * 3,
                                     dimensions['small'][2] * 3];
            dimensions['custom'] = [dimensions['small'][0] * 5,
                                     dimensions['small'][1] * 5,
                                     dimensions['small'][2] * 5];
        },
    
        xSize = function(val) { return accessDimension(0,val) },
        ySize = function(val) { return accessDimension(1,val) },
        zSize = function(val) { return accessDimension(2,val) },
        xDisplay, yDisplay, zDisplay, smallButton, mediumButton,
        largeButton, customButton;
        return {
    
            init: function(presetChangeCb, 
                            x, y, z, 
                            presetS, presetM, presetL, presetC) {
                showMetricDimensions();    
                
                                
                presetChangeCallback = presetChangeCb;
                xDisplay = $(x);
                yDisplay = $(y);
                zDisplay = $(z);
                smallButton = $(presetS);
                mediumButton = $(presetM);
                largeButton = $(presetL);
                customButton = $(presetC);
                
                // smallButton.toggleClass("active");
                
                var presetClick = function(size, e) {
                    changePresetSize(size);
                    $("#presets button").removeClass("active");
                    $(e.target).toggleClass("active");
                }
              
                smallButton.click(function(e) { presetClick('small',e);});
                mediumButton.click(function(e) { presetClick('medium',e);});
                largeButton.click(function(e) { presetClick('large',e);});
                customButton.click(function(e) { presetClick('custom',e);});
            },
            
            setSize: function(x,y,z) {
                dimensions[currentSizePreset] = [x,y,z];
                updatePresets();
                updateDisplay();
            },
            
            resetPresets: function() {
                currentSizePreset = 'small'
                $("#presets button").removeClass("active");
                smallButton.toggleClass("active");    
            },
            
            getCurrentDimensions: function() {
                return dimensions[currentSizePreset]
            },
            
            getCurrentSize: function() {
                return modelSizes[currentSizePreset]
            },
            
            toggleUnits: function() {
                if (currentUnits == 'm') {
                    currentUnits = 'i';
                } else {
                    currentUnits = 'm';
                }
                
                $("#threedim #units span").toggleClass("current");
                showCurrentDimensions();
            }
            

    }
}());