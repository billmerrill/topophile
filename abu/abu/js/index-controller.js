var indexController = (function(){
    "use strict";
    
    var map, model, geocoder,
        bbox,
        bamService = "http://127.0.0.1:8080/",
        nwlatDisplay,
        nwlonDisplay,
        selatDisplay,
        selonDisplay,
    
        setBBox = function() {
            bbox = {'nwlat': $("#nwlat").val(),
                    'nwlon': $("#nwlon").val(),
                    'selat': $("#selat").val(),
                    'selon': $("#selon").val()};
        },
        
        updateModel = function(data, status) {
            alert("model update status \"" + status + "\"");
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
                        'rez': 75 }
            })
            .done(function(data, status, jqxhr) {
                model.showModel(data);
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
        },
        
        previewTopo = function() {
            setBBox();
            getModelUrl();
        },
        
        initRainierDemo = function() {
            //Upper Left  (-121.8229167,  46.9290278) (121d49'22.50"W, 46d55'44.50"N)
            //Lower Right (-121.6701389,  46.7762500) (121d40'12.50"W, 46d46'34.50"N)

            $("#nwlat").val(46.9290278);
            $("#nwlon").val(-121.8229167);
            $("#selat").val(46.7762500);
            $("#selon").val(-121.6701389);
        };
        
        

    return{
        init: function(mapModule, modelModule, geocoderModule) {
            map = mapModule;
            model = modelModule;
            geocoder = geocoderModule;
            
            map.init("map", newBBoxHandler);
            
        
            $("#model-canvas").width($("#map").width());
            $("#model-canvas").height($("#map").height());
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
            $("#gc-search").keyup(function(e){
                if(e.keyCode == 13) {
                    geocoder.search($("#gc-search").val());
                }});
            
            $("#preview-topo").click( function() {
                previewTopo();} 
            );
            
            initRainierDemo();


        }
    };
    
}());