var indexController = (function(){
    "use strict";
    
    var map, model, geocoder,
        bamService = "http://127.0.0.1:8080/",
        firstBounds = true,
        firstTopo = true,
        nwlatDisplay,
        nwlonDisplay,
        selatDisplay,
        selonDisplay,
        zFactorDisplay,
    
        getModelUrl = function() {
            $("#model-building").show();
            $.ajax({
                type: "GET",
                url: bamService,
                data: { 'nwlat': nwlatDisplay.val(),
                        'nwlon': nwlonDisplay.val(),
                        'selat': selatDisplay.val(),
                        'selon': selonDisplay.val(),
                        'size': 200, 
                        'rez': 75,
                        'zfactor': zFactorDisplay.val()}
            })
            .done(function(data, status, jqxhr) {
                model.showModel(data['url']);
                $("#build-model").prop('disabled', false);

            })
            .fail(function(data, stats, error) {
                alert("Sorry, I couldn't build a model.")
            })
            .always(function(data) {
                $("#model-building").hide();
                $("#model-canvas").show()
            });
        },
        
        newBoundsHandler = function(newBounds) {
            if (firstBounds) {
                $("#preview-topo").prop('disabled', false);
                firstBounds = false;
            }
            updateBoundsDisplay(newBounds)
        },
        
        clearedBoundsHandler = function() {
            // something
        },
        
        updateBoundsDisplay = function(bounds) {
            nwlatDisplay.val(bounds['nwlat']);
            nwlonDisplay.val(bounds['nwlon']);
            selatDisplay.val(bounds['selat']);
            selonDisplay.val(bounds['selon']);
        },
        
        geocoderResultHandler = function(data, status) {
            map.showSearchResult(data[0]['lat'], data[0]['lon'])
        },
        
        previewTopo = function() {
            if (firstTopo) {
                $("#instructions").hide();        
                firstTopo = false;
            }
            $("#model-canvas").hide()
            getModelUrl();
        },
        
        initRainierBounds = function() {
            //Upper Left  (-121.8229167,  46.9290278) (121d49'22.50"W, 46d55'44.50"N)
            //Lower Right (-121.6701389,  46.7762500) (121d40'12.50"W, 46d46'34.50"N)

            nwlatDisplay.val(46.9290278);
            nwlonDisplay.val(-121.8229167);
            selatDisplay.val(46.7762500);
            selonDisplay.val(-121.6701389);
        },
        
        initComponents = function() {
            var mt_rainier = [ 46.852947, -121.760424 ];
            
            map.init("map", mt_rainier, newBoundsHandler, clearedBoundsHandler);
            model.init("model-canvas");
            geocoder.init(geocoderResultHandler);
        },
        
        initUi = function() {
            nwlatDisplay = $("#nwlat");
            nwlonDisplay = $("#nwlon");
            selatDisplay = $("#selat");
            selonDisplay = $("#selon");
            zFactorDisplay = $("#zfactor");
            
            zFactorDisplay.val("1.5");
            
            $("#gc-search-button").click(
                function() {geocoder.search($("#gc-search").val())}
            );
            $("#gc-search").keyup(function(e){
                if(e.keyCode == 13) {
                    geocoder.search($("#gc-search").val());
                }});
            
            $("#preview-topo").click( function() {
                previewTopo();} 
            ).prop('disabled', true);
            
            $("#build-model").prop('disabled', true);
            
            $("#model-building").hide();
        };
        
        

    return{
        init: function(mapModule, modelModule, geocoderModule) {
            map = mapModule;
            model = modelModule;
            geocoder = geocoderModule;

            initComponents();
            initUi();
        }
    };
    
}());