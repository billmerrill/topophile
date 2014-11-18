modelSizing = (function(){
    "use strict";
    
    var currentSizePreset = 'small',
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
        },
        
        
        updateDisplay =  function() {
            xDisplay.val(xSize());
            yDisplay.val(ySize());
            zDisplay.val(zSize());
        },
    
        xSize = function(val) { return accessDimension(0,val) },
        ySize = function(val) { return accessDimension(1,val) },
        zSize = function(val) { return accessDimension(2,val) },
        xDisplay, yDisplay, zDisplay, smallButton, mediumButton,
        largeButton, customButton;
        return {
    
            initDisplay: function(x, y, z, presetS, presetM, presetL, presetC) {
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
            },
            
            initPresets: function() {
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
            
            getCurrentDimensions: function() {
                return dimensions[currentSizePreset]
            },
            

    }
}());