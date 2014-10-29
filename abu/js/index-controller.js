var indexController = (function(){
    "use strict";
    
    var map, model,
        bbox,
        bamService = "http://climb.local:8080/",
    
        setBBox = function() {
            bbox = {'nwlat': $("#nwlat").value,
                    'nwlon': $("#nwlon").value,
                    'selat': $("#selat").value,
                    'selon': $("#selon").value};
        },
        
        updateModel = function(modelUrl) {
            alert("got model " + modelUrl);
            // model.setModel(modelUrl);
        },
        
        getModelUrl = function() {
            $.ajax({
                type: "GET",
                url: bamService,
                data: { 'nwlat': bbox['nwlat'],
                        'nwlon': bbox['nwlon'],
                        'selat': bbox['selat'],
                        'selon': bbox['selon'],
                        'size': 200, 
                        'rez': 50 }
            })
            .done(function(data, status, jqxhr) {
                updateModel(data)
            });
        },
        
        generateModel = function() {
            setBBox();
            getModelUrl();
        };
  
    
    
    return{
        init: function(map, model) {
            this.map = map;
            this.model = model;
            // setup Map and Model here
        },

        previewTopo: function() {
            generateModel();
        }
    };
    
}());