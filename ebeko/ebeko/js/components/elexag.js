TOPO.BUILD1.Exaggerater =  (function(){
    "use strict";
    
    return {
        init: function(startExag, exagContainerId, exagSliderId, exagValueId) {
            var terrain = TOPO.BUILD1.Terrain,
                exagValue = $("#" + exagValueId),
                slider = $('#' + exagSliderId);
                
            exagValue.val(startExag);
            slider.slider();
            
            $('#' + exagContainerId).on('change', function(e) {
                if (e.target.id == 'zfactor') {
                    var val = parseFloat(e.target.value);
                    terrain.updateZFactor(val);
                    if ((val >= .1) && (val <= 10)) {
                        slider.slider('setValue', val);
                    }
                } else {
                    var val = e.value.newValue;
                    terrain.updateZFactor(val);
                    exagValue.val(val)
                }
            });
            
        },
    }
}());
