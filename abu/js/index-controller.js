var indexController = (function(){
    "use strict";
    
    var map, model,
        bbox,
        bamService = "http://climb.local:8080/",
        nwlatDisplay,
        nwlonDisplay,
        selatDisplay,
        selonDisplay,
        
    
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
        },
        
        newBBox = function(newBBox) {
            bbox = newBBox
            updateBBoxDisplay()
        },
        
        updateBBoxDisplay = function() {
            nwlatDisplay.val(bbox['nwlat']);
            nwlonDisplay.val(bbox['nwlon']);
            selatDisplay.val(bbox['selat']);
            selonDisplay.val(bbox['selon']);
        }
  
    
    
    return{
        init: function(map, model) {
            map = map;
            model = model;
          
            nwlatDisplay = $("#nwlat");
            nwlonDisplay = $("#nwlon");
            selatDisplay = $("#selat");
            selonDisplay = $("#selon");
            
            map.newBBoxHandler(newBBox)
            // setup Map and Model here
        },

        previewTopo: function() {
            generateModel();
        }
    };
    
}());