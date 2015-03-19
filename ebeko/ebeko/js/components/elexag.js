TOPO.BUILD1.Exaggerater =  (function(){
    "use strict";
    
    var exagValue, newValueCallback;
    
    return {
        init: function(newValueCb, startExag, exagContainerId, exagSliderId, exagValueId) {
            var terrain = TOPO.BUILD1.Terrain,
                slider = $('#' + exagSliderId);
               
            newValueCallback = newValueCb;
            exagValue = $("#" + exagValueId);
            exagValue.val(startExag);
            slider.slider();
            
            $('#' + exagContainerId).on('change', function(e) {
                if (e.target.id == 'zfactor') {
                    var val = parseFloat(e.target.value);
                    terrain.updateZFactor(val);
                    if ((val >= .1) && (val <= 10)) {
                        slider.slider('setValue', val);
                    }
                    newValueCallback(val);
                } else {
                    var val = e.value.newValue;
                    terrain.updateZFactor(val);
                    exagValue.val(val)
                    newValueCallback(val);
                }
            });
            
        }, 
        
        getFactor: function() {
            return exagValue.val();
        },
        
        getFactorUrlData: function() {
            return (10*Number(exagValue.val())).toString(36);
        },
        
        setUrlZFactor: function(newz) {
            newz = parseInt(newz, 36) / 10.0;
            newz = newz.toFixed(1);
            exagValue.val(newz);
            exagValue.trigger('change');
            
        },
    }
}());
