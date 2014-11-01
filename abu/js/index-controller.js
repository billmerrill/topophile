var indexController = (function(){
    "use strict";
    
    var map, model, geocoder,
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
        
        newBBoxHandler = function(newBBox) {
            bbox = newBBox
            updateBBoxDisplay()
        },
        
        updateBBoxDisplay = function() {
            nwlatDisplay.val(bbox['nwlat']);
            nwlonDisplay.val(bbox['nwlon']);
            selatDisplay.val(bbox['selat']);
            selonDisplay.val(bbox['selon']);
        },
        
        geocoderResultHandler = function(data, status) {
            map.showSearchResult(data[0]['lat'], data[0]['lon'])
        };
  
    return{
        init: function(mapModule, modelModule, geocoderModule) {
            map = mapModule;
            model = modelModule;
            geocoder = geocoderModule;
            
            map.init("map", newBBoxHandler);
            model.init("model-canvas");
            model.showModel('./assets/rainier.stl');    
            geocoder.init(geocoderResultHandler);
            
          
            nwlatDisplay = $("#nwlat");
            nwlonDisplay = $("#nwlon");
            selatDisplay = $("#selat");
            selonDisplay = $("#selon");
            
            $("#gc-search-button").click(
                function() {geocoder.search($("#gc-search").val())}
            );
        },

        previewTopo: function() {
            generateModel();
        }
    };
    
}());