TOPO.BUILD1.Printer = (function() {
    "use strict";
   
    var topoModelId,
        swModelId,
        swModelUrl,
  
    uploadComplete = function(data) {
        scheduleCheck();
        swModelId = data['modelId'];
        swModelUrl = data['urls']['privateProductUrl']['address'];
        setPrintStatus("Shapeways is processing your model.");
        $('#buyit').click(function(){window.open(swModelUrl)});
    }, 
    
    scheduleCheck = function() {
        setTimeout(isModelReady, TOPO.BUILD1.getConfig('printablePause'))
    },
   
    isModelReady = function() {
        $.ajax({
            type: "GET",
            url: TOPO.BUILD1.getConfig('modelPrintableService'),
            data: {'swid': swModelId,
                   'tpid': topoModelId}
        })
        .fail(function(data, stats, error) {
            alert("I'm sorry, I couldn't connect.");
        })
        .done(function(data, status, jqxhr) {
            checkPrinterProcessingComplete(data);
        })
        .always(function(data){
            console.log("checked ready")
        });
        
    },
    
    checkPrinterProcessingComplete = function(data) {
        console.log(data)
        if (data['ready']) {
            $('#buyit').show();
            $('#model-building').hide();
            setPrintStatus("Your Model Is Ready!");
        } else {
            setTimeout(isModelReady, TOPO.BUILD1.getConfig('printablePause'))
        }
    },
    
    setPrintStatus =  function(status) {
        $("#print-status").html(status);
    }
    

    return {
        init: function() {
            $('#buyit').hide();
        },
        
        upload: function(modelName) {
            topoModelId = modelName
            setPrintStatus("Sending Model to Shapeways");
            $('#buyit').hide();
            $.ajax({
                type: "GET",
                url: TOPO.BUILD1.getConfig('uploadService'),
                data: {'model_id': modelName}
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