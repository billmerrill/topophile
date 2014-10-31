var indexMap = (function() {
    var map;
  
   
    return {
        init: function(mapDisplayId) {
            map = L.map(mapDisplayId, {
              layers: MQ.satelliteLayer(),
              center: [ 34.5, 131.6 ],
              zoom: 13 } );
        }
    }
    
}());