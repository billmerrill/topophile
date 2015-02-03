TOPO.BUILD1.Printer = (function() {
    "use strict";
   
    var readyInterval,
        modelId,
        modelUrl,
  
    uploadComplete = function(data) {
        scheduleCheck();
        modelId = data['modelId'];
        modelUrl = data['urls']['privateProductUrl']['address'];
        setPrintStatus("Shapeways is processing your model.");
        $('#buyit').click(function(){window.open(modelUrl)});
    }, 
    
    scheduleCheck = function() {
        readyInterval = setInterval(isModelReady, 5000);
    },
   
    isModelReady = function() {
        $.ajax({
            type: "GET",
            url: TOPO.BUILD1.getConfig('modelPrintableService'),
            data: {'id': modelId}
        })
        .fail(function(data, stats, error) {
            alert("I'm sorry, I couldn't connect.");
            clearInterval(readyInterval);
        })
        .done(function(data, status, jqxhr) {
            checkPrinterProcessingComplete(data);
        })
        .always(function(data){
            console.log('modelIsReady check');
        });
        
    },
    
    checkPrinterProcessingComplete = function(data) {
        console.log(data)
        if (data['ready']) {
            // $('#status').html("MODEL IS READY");
            $('#buyit').show();
            $('#model-building').hide();
            clearInterval(readyInterval);
            setPrintStatus("Your Model Is Ready!");
        }
    },
    
    setPrintStatus =  function(status) {
        $("#print-status").html(status);
    }
    

    return {
        init: function() {
            $('#buyit').hide();
        },
        
        upload: function(modelId) {
            setPrintStatus("Sending Model to Shapeways");
            $('#buyit').hide();
            $.ajax({
                type: "GET",
                url: TOPO.BUILD1.getConfig('uploadService'),
                data: {'model_id': modelId}
            })
            .fail(function(data, stats, error) {
                alert("I'm sorry, I couldn't connect.");
            })
            .done(function(data, status, jqxhr) {
                uploadComplete(data);
            })
            .always(function(data){
            });    
        }
    }
    
}());