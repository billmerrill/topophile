var indexController = (function(){
    "use strict";
    
    var map, model, geocoder,
        bamService = "http://127.0.0.1:8080/build",
        abuService = "http://127.0.0.1:8888/",
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
                        'size': 100, 
                        'rez': 75,
                        'zfactor': 1,
                        'model_style': 'preview'}
            })
            .done(function(data, status, jqxhr) {
                model.showModel(data['url']);
                $("#build-model")
                    .prop('disabled', false)
                    .addClass('btn-success');

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
                firstBounds = false;
            }
            updateBoundsDisplay(newBounds);
            previewTopo();
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
            if (data.length > 0) {
                map.showSearchResult(data[0]['lat'], data[0]['lon'])
            } else {
                alert("No place found.");
            }
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
            model.init("model-canvas", 1.5);
            geocoder.init(geocoderResultHandler);
        },
        
        initUi = function() {
            nwlatDisplay = $("#nwlat");
            nwlonDisplay = $("#nwlon");
            selatDisplay = $("#selat");
            selonDisplay = $("#selon");
            zFactorDisplay = $("#zfactor");
            
            zFactorDisplay.val("1.5");
            
            $('#exag').on('change', function(e) {
                console.log('exag change', e);
                if (e.target.id == 'height-factor-slider') {
                    console.log('**********************FU');
                }
                if (e.target.id == 'zfactor') {
                    var val = parseFloat(e.target.value);
                    model.updateZFactor(val);
                    if ((val >= .1) && (val <= 10)) {
                        $('#height-factor').slider('setValue', val);
                    }
                } else {
                    var val = e.value.newValue;
                    model.updateZFactor(val);
                    zFactorDisplay.val(val)
                }
            });
                
            $('#height-factor').slider();
            
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
            
            $("#build-model").prop('disabled', true).click(function() { 
                var url = abuService + "model.html?nwlat=" + nwlatDisplay.val() +
                            "&nwlon=" + nwlonDisplay.val() +
                            "&selat=" + selatDisplay.val() + 
                            "&selon=" + selonDisplay.val() +
                            "&zfactor=" + zFactorDisplay.val();
                window.location = url;
            });
            
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