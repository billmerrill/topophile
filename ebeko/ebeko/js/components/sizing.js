TOPO.BUILD1.Sizing = (function(){
    "use strict";
    
    var currentUnits = 'm',
        presetChangeCallback, currentSizePreset = 'small',
        dimensions = {'small': [],
                       'medium': [],
                       'large': [],
                       'custom': []},
                       
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
       
        showImperialDimensions = function () {
            $(".size-cm").hide();
            $(".size-in").show();    
        },
        
        showMetricDimensions = function () {
            $(".size-cm").show();
            $(".size-in").hide();    
        },
        
        makeDisplayDimension = function(mmval) {
            var cmval = (mmval / 10.0).toPrecision(2);
            var inval = (mmval / 25.4).toPrecision(2);
            return '<span class="size-cm">'+cmval+' cm</span><span class="size-in">'+inval+' in<span>';
        },
        
        updateDisplay =  function() {
            xDisplay.html(makeDisplayDimension(xSize()));
            yDisplay.html(makeDisplayDimension(ySize()));
            zDisplay.html(makeDisplayDimension(zSize()));
            showMetricDimensions();
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
                
                smallButton.toggleClass("active");
                
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
                updateDisplay();
                updatePresets();
            },
            
            getCurrentDimensions: function() {
                return dimensions[currentSizePreset]
            },
            

    }
}());