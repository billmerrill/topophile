TOPO.BUILD1.Printer = (function() {
    "use strict";
   
    var topoModelId,
        swModelId,
        swModelUrl,
        stateDisplays,
        newModelName = null,
  
    uploadComplete = function(data) {
        printingState(PRINT_PROCESS);
        scheduleCheck();
        swModelId = data['modelId'];
        swModelUrl = data['urls']['privateProductUrl']['address'];
        console.log("You'll be able to see your model here, but it's not ready yet: ", swModelUrl);
    }, 
    
    scheduleCheck = function() {
        setTimeout(isModelReady, TOPO.BUILD1.getConfig('printablePause'))
    },
   
    isModelReady = function() {
        var data = {'swid': swModelId,
                    'tpid': topoModelId};
        if (newModelName != null) {
            data['name'] = newModelName;
            newModelName = null;
        }
        
        $.ajax({
            type: "GET",
            url: TOPO.BUILD1.getConfig('modelPrintableService'),
            data: data
        })
        .fail(function(data, stats, error) {
            console.log("Error occurred checking printability.");
            printingState(PRINT_ERROR);
        })
        .done(function(data, status, jqxhr) {
            checkPrinterProcessingComplete(data);
        })
        .always(function(data){
            console.log("printer ready?")
        });
        
    },
    
    checkPrinterProcessingComplete = function(data) {
        if (data['ready']) {
            $('#model-building').hide();
            printingState(PRINT_READY);
        } else {
            setTimeout(isModelReady, TOPO.BUILD1.getConfig('printablePause'))
        }
    },
    
    PRINT_INIT = 'init',
    PRINT_UPLOAD = 'upload',
    PRINT_PROCESS = 'process',
    PRINT_READY = 'ready',
    PRINT_ERROR = 'error',
    printingState = function(newState) {
        var x;
        switch(newState) {
            case PRINT_INIT:
                for (x in stateDisplays) {
                    stateDisplays[x].removeClass("doing done");
                }
                break;
            case PRINT_UPLOAD:
                stateDisplays[PRINT_UPLOAD].addClass("doing");
                break;
            case PRINT_PROCESS:
                stateDisplays[PRINT_UPLOAD].removeClass("doing").addClass("done");
                stateDisplays[PRINT_PROCESS].addClass("doing");
                break;
            case PRINT_READY:
                stateDisplays[PRINT_PROCESS].removeClass("doing").addClass("done");
                stateDisplays[PRINT_READY].addClass("doing")
                    .html('<span class="gotoprint">Go See<br>Your Model</span>')
                    .click(function(){window.open(swModelUrl)});
                break;
            case PRINT_ERROR:
                $('#return-url').html(document.location.href);
                $('#error-row').show();
                printingState(PRINT_INIT);
                
                break;
            default:
                console.log("Build Button Error");
        }
        
    }
    

    return {
        init: function() {
            $('#error-row').hide();
            stateDisplays = {};
            stateDisplays[PRINT_UPLOAD] = $('#print_uploading'); 
            stateDisplays[PRINT_PROCESS] =  $('#print_processing');
            stateDisplays[PRINT_READY] = $('#print_ready');
            printingState(PRINT_INIT);
        },
        
        upload: function(modelName) {
            printingState(PRINT_INIT);
            topoModelId = modelName
            printingState(PRINT_UPLOAD);
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
        },
        
        setModelName: function(name) { 
            newModelName = name;
        }
        
        
    }
    
}());