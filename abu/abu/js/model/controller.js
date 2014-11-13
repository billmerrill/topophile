var modelController = (function() {
    var bamService = "http://127.0.0.1:8080/",
        physicalXDisplay, physicalYDisplay, physicalZDisplay,
        model, nwlat, nwlon, selat, selon, zfactor,
  
    getParams = function() {
        url = document.location;
        var searchObject = {},
            queries, split, i;

        queries = document.location.search.replace(/^\?/, '').split('&');
        for( i = 0; i < queries.length; i++ ) {
            split = queries[i].split('=');
            searchObject[split[0]] = split[1];
        }
        return searchObject;
    }


    getModelUrl = function() {
        $("#model-building").show();
        $.ajax({
            type: "GET",
            url: bamService,
            data: { 'nwlat': nwlat,
                    'nwlon': nwlon,
                    'selat': selat,
                    'selon': selon,
                    'size': 200, 
                    'rez': 400,
                    'zfactor': zfactor}
        })
        .done(function(data, status, jqxhr) {
            model.showModel(data);
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
   
    initComponents = function() {
        model.init("model-canvas");
    },
    
    initUi = function() {
        $('#model-building').hide();
        physicalXDisplay = $('#xsize')
        physicalYDisplay = $('#ysize')
        physicalZDisplay = $('#zsize')
    },
    
    fakeUpData = function() {
        nwlat = 46.9290278;
        nwlon = -121.8229167;
        selat = 46.7762500;
        selon = -121.6701389;
        zfactor = 1.5;
        physicalXDisplay.val("200.0")
        physicalYDisplay.val("400.0")
        physicalZDisplay.val("300.0")
    };
   
    return {
        init: function(modelModule) {
            model = modelModule;
            params = getParams();
            initComponents();
            initUi();
            fakeUpData();
            model.showModel('http://127.0.0.1:9999/3E225D98-E9FE-458F-A1D2-EFD54FCBAF26.stl');
            // getModelUrl();
        }
    }
    
}());