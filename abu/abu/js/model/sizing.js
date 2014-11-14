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
        xSize = function(val) { return accessDimension(0,val) },
        ySize = function(val) { return accessDimension(1,val) },
        zSize = function(val) { return accessDimension(2,val) },
        xDisplay, yDisplay, zDisplay;
        
        return {
    
            initDisplay: function(x,y,z){
                xDisplay = $(x);
                yDisplay = $(y);
                zDisplay = $(z);
            },
            
            updateDisplay: function() {
                xDisplay.val(xSize());
                yDisplay.val(ySize());
                zDisplay.val(zSize());
            },
            
            setSize: function(x,y,z) {
                dimensions[currentSizePreset] = [x,y,z];
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
            
            changePresetSize: function(newPreset) {
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
    }
}());