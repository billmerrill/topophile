var indexMap = (function() {
    var map, newBBoxCallback;
    
    return {
        init: function(mapDisplayId, newBBoxCb) {
            newBBoxCallback = newBBoxCb;
            
            map = L.map(mapDisplayId, {
              layers: MQ.hybridLayer(),
              center: [ 34.5, 131.6 ],
              zoom: 13 } );
              
        }
    }
    
}());