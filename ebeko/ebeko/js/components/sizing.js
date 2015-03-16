TOPO.BUILD1.Sizing = (function(){
    "use strict";
    
    var currentUnits = 'm',
        presetChangeCallback, currentSizePreset = 'medium',
        modelDimensions = [0,0,0],
        modelSizes = {'small': 50,
                     'medium': 100,
                     'large': 200,
                     'custom': 250},
        modelScaleMMisM = {'x_model_mm_is_m': 0,
                       'y_model_mm_is_m': 0,
                       'z_model_mm_is_m': 0},
        modelZExag = 1,
                       
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
        
        formatYards = function(y) {
            if (y > 1000) {
                return (y/1760).toFixed(2) + " miles";
            } else {
                return y.toFixed(1) + " yards"
            }
            
        },
        
        formatMeters = function(m) {
            if (m > 900) {
                return (m/1000).toFixed(2) + " km";
            } else {
                return m.toFixed(1) + " m"
            }
            
        },
        
        makeDisplayScale = function(meters_to_mm) {
            var meters_per_cm = (meters_to_mm * 10.0).toFixed(1);
            var yards_per_inch = (meters_to_mm * 25.4 * 1.0936 ).toFixed(1);
            return '<span class="size-cm">1 cm : '+ formatMeters(meters_per_cm) +
                '</span><span class="size-in">1 in : ' + formatYards(yards_per_inch) +
                '<span>';
        },
        
        setScales = function(data) {
            modelScaleMMisM = [data['x_mm_is_m'],
                               data['y_mm_is_m'],
                               data['z_mm_is_m']];
        },
        
        updateDisplay =  function() {
            xDisplay.html(makeDisplayDimension(modelDimensions[0]));
            yDisplay.html(makeDisplayDimension(modelDimensions[1]));
            zDisplay.html(makeDisplayDimension(modelDimensions[2]));
            xScaleDisplay.html(makeDisplayScale(modelScaleMMisM[0]));
            zScaleDisplay.html(makeDisplayScale(modelScaleMMisM[2]));
            showCurrentDimensions();
        },
        
        xDisplay, yDisplay, zDisplay, 
        xScaleDisplay, yScaleDisplay, zScaleDisplay,
        smallButton, mediumButton,
        largeButton, customButton;
        
        return {
    
            init: function(presetChangeCb, 
                            x, y, z, 
                            xScale, zScale,
                            presetS, presetM, presetL, presetC) {
                showMetricDimensions();    
                
                                
                presetChangeCallback = presetChangeCb;
                xDisplay = $(x);
                yDisplay = $(y);
                zDisplay = $(z);
                xScaleDisplay = $(xScale);
                // yScale = $(yScale);
                zScaleDisplay = $(zScale);
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
            
            setNewModel: function(data) {
                modelDimensions =[data['x-size-mm'], data['y-size-mm'], data['z-size-mm']];
                setScales(data);
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