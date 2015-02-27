TOPO.BUILD1.Sizing = (function(){
    "use strict";
    
    var currentUnits = 'm',
        presetChangeCallback, currentSizePreset = 'medium',
        modelDimensions = [0,0,0],
        modelSizes = {'small': 50,
                     'medium': 100,
                     'large': 200,
                     'custom': 250},
                       
        changePresetSize = function(newPreset) {
            currentSizePreset = newPreset;
            presetChangeCallback();
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
            xDisplay.html(makeDisplayDimension(modelDimensions[0]));
            yDisplay.html(makeDisplayDimension(modelDimensions[1]));
            zDisplay.html(makeDisplayDimension(modelDimensions[2]));
            showCurrentDimensions();
        },
        
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
                mediumButton = $(presetM).addClass('active');
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
                modelDimensions = [x,y,z];
                updateDisplay();
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