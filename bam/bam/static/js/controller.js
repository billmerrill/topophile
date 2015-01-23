var buyController = (function() {
    "use strict";
   
    var readyInterval,
        modelId,
        modelUrl,
        mockprintableService = "http://127.0.0.1:9090/fake_ready",
        danaPrintableService = "http://127.0.0.1:9090/is_printable",
   
    modelIsReady = function() {
        $.ajax({
            type: "GET",
            url: danaPrintableService,
            data: {'id': modelId}
        })
        .fail(function(data, stats, error) {
            alert("I'm sorry, I couldn't connect.");
            clearInterval(readyInterval);
        })
        .done(function(data, status, jqxhr) {
            updateStatus(data);
        })
        .always(function(data){
            console.log('modelIsReady check');
        });
        
    },
    
    updateStatus = function(data) {
        console.log(data)
        if (data['ready']) {
            $('#status').html("MODEL IS READY");
            $('#buyit').show();
            $('#model-building').hide();
            clearInterval(readyInterval);
        }
    },
    
    scheduleCheck = function() {
        readyInterval = setInterval(modelIsReady, 5000);
    }
    
    return {
        init: function(mId, mUrl) {
            $('#buyit').hide();
            modelId = mId;
            modelUrl = mUrl;
            scheduleCheck();
            $('#buyit').click(function(){window.open(modelUrl)});
        }
    }
    
}());