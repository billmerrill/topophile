TOPO.BUILD1.Model = (function() {
    "use strict";

    var canvas, jcanvas,
        viewer, 
        references = TOPO.BUILD1.ModelReferenceObjects, 
        showSizeReference = false, 
        comparisonMeshParts,
        deleteMeshParts,
        modelWidth = 100,
        busyDisplay,
        resetButton,
        compareButton,
        newModelCallback,
        COMPARE_DOLLAR = 'dollar',
        COMPARE_EURO = 'euro',
        currentComp = COMPARE_DOLLAR,
        
        buildComparison = function(scale) {
            if (!scale) {
                scale = [1,1,1]
            }
            var xform = {scale: scale, translate: [modelWidth + 10 ,0,1]};
            switch (currentComp) {
                case COMPARE_DOLLAR:
                    comparisonMeshParts = TOPO.BUILD1.ModelReferenceObjects.dollar(xform);
                    break;
                case COMPARE_EURO:
                    comparisonMeshParts = TOPO.BUILD1.ModelReferenceObjects.euro(xform);
                    break;
                default:
                    console.log('buildComparison Error');
            }
        },
        
        initViewer = function() {
            viewer = new JSC3D.Viewer(canvas);
            // viewer.setParameter('ModelColor',       '#9999FF');
            viewer.setParameter('ModelColor',       '#EEEEEE');
            viewer.setParameter('Background',       'on');
            viewer.setParameter('BackgroundColor1', '#d4e1ff');
            viewer.setParameter('BackgroundColor2', '#d4e1ff');
            viewer.setParameter('RenderMode',       'texturesmooth');
            viewer.setParameter('Renderer',         'webgl');
            viewer.setParameter('InitRotationX',     '-80');
            viewer.setParameter('InitRotationY' ,    '30');
            viewer.setParameter('CreaseAngle',       '25');
            
            viewer.mouseWheelHandler = function(e){return;};
            viewer.init();
            viewer.update();
            
            $('#model-zoomin').click(function(){
                zoomIn();
            });
            $('#model-zoomout').click(function(){
                zoomOut();
            });
        },
        
        toggleSizeReference = function() {
            showSizeReference = !showSizeReference; 
            if (comparisonMeshParts) {
                var i;
                var currScene = viewer.getScene();
                if (showSizeReference) {
                    for (i in comparisonMeshParts) {
                        currScene.addChild(comparisonMeshParts[i]);
                    }
                } else {
                    for (i in comparisonMeshParts) {
                        currScene.removeChild(comparisonMeshParts[i]);
                    }
                }    
                currScene.calcAABB();
                viewer.update();
            }
        },
        
        toggleComparison = function(comp) {
            if (showSizeReference) {
                if (comp == currentComp) {
                    showSizeReference = false;
                } else {
                    currentComp = comp;
                    deleteMeshParts = comparisonMeshParts;
                    buildComparison([1,1,1]);
                }
            } else {
                showSizeReference = true;
                if (comp != currentComp){
                    currentComp = comp;
                    deleteMeshParts = comparisonMeshParts;
                    buildComparison([1,1,1]);
                }
            }
        
            updateComparisonScene();
        },
        
        updateComparisonScene = function() {
            if (comparisonMeshParts) {
                var i;
                var currScene = viewer.getScene();
                if (deleteMeshParts) {
                    for (i in deleteMeshParts) {
                        currScene.removeChild(deleteMeshParts[i]);
                    }
                    deleteMeshParts = null;
                }
                if (showSizeReference) {
                    for (i in comparisonMeshParts) {
                        currScene.addChild(comparisonMeshParts[i]);
                    }
                } else {
                    for (i in comparisonMeshParts) {
                        currScene.removeChild(comparisonMeshParts[i]);
                    }
                }    
                currScene.calcAABB();
                viewer.update();
            }
        },
        
        resetScene = function() {
            viewer.resetScene();
            viewer.update();
        },
                
        zoomIn = function() {
            viewer.zoomFactor *= 1.3;
            viewer.update();
        },
        
        zoomOut = function() {
            viewer.zoomFactor /= 1.3;
            viewer.update();
        },
        
       
        initReferences = function() {
            $('#compare-dollar').click(function(e) {
                $('#compare-dollar').toggleClass('active');
                $('#compare-euro').removeClass('active');
                toggleComparison(COMPARE_DOLLAR);
            });
            $('#compare-euro').click(function(e) {
                $('#compare-euro').toggleClass('active');
                $('#compare-dollar').removeClass('active');
                toggleComparison(COMPARE_EURO);
            });
        },
        
        enableReferences = function() {
            $('#compare-dollar').prop('disabled', false);
            $('#compare-euro').prop('disabled', false);
        },
        
        disableReferences = function() {
            $('#compare-dollar').prop('disabled', true);
            $('#compare-euro').prop('disabled', true);
        };
 
    
    return {
    
        init: function(newModelCb, displayCanvasId, progressDisplayId, compareButtonId, resetButtonId) {
            newModelCallback = newModelCb;
            compareButton = $('#'+compareButtonId);
            compareButton.click(function() {
                toggleSizeReference();
                resetScene();
            })
            resetButton = $('#'+resetButtonId);
            resetButton.click(function() {
                resetScene();
            })
            busyDisplay = $('#'+progressDisplayId);
            busyDisplay.hide();
            canvas = document.getElementById(displayCanvasId);
            jcanvas = $(canvas);
            jcanvas.hide();
            initViewer();
            initReferences();
            disableReferences();
        },
        
  
        showModel: function(modelUrl, width) {
            modelWidth = width
            buildComparison([1,1,1]);
            var loader = new JSC3D.StlLoader;
            loader.onload = function(scene) {
                if (showSizeReference) {
                    var i;
                    for (i in comparisonMeshParts) {
                        scene.addChild(comparisonMeshParts[i]);
                    }
                }
                viewer.replaceScene(scene);
                viewer.zoomFactor *= 1.5;
            };
            loader.loadFromUrl(modelUrl);
        },
        
        showBusy: function() {
            $("#model-instructions").hide();        
            jcanvas.hide();
            busyDisplay.show();
        },
        
        hideBusy: function() {
            jcanvas.show();
            busyDisplay.hide();
        },
        
        renderModel: function(modelSpec) {
            var thee = this;
            this.showBusy();
            
            var requestData = { 'nwlat': modelSpec.nwlat,
                    'nwlon': modelSpec.nwlon,
                    'selat': modelSpec.selat,
                    'selon': modelSpec.selon,
                    'size': modelSpec.modelSize, 
                    'rez': TOPO.BUILD1.getConfig('modelRez'), //400 dots per 100 mm ~= 100dpi
                    'zfactor': modelSpec.zfactor,
                    'hollow': 1};
                    
            if (TOPO.BUILD1.getConfig('enableMsScaling')) {
                var imageSize = TOPO.BUILD1.Utils.scaleRectToMaxLength(modelSpec.selectRect, 
                                                    TOPO.BUILD1.getConfig('modelRez'));
                requestData['width'] = imageSize.x;
                requestData['height'] = imageSize.y ;
            }

            $.ajax({
                type: "GET",
                url: TOPO.BUILD1.getConfig('bamService'),
                data: requestData
            })
            .done(function(data, status, jqxhr) {
                thee.showModel(data['url'], data['x-size-mm']);
                thee.currentModelId = data['model_id'];
                enableReferences();
                newModelCallback(data);
            })
            .fail(function(data, stats, error) {
                alert("Sorry, I couldn't build a model.")
            })
            .always(function(data) {
                thee.hideBusy();
            });
        },
        
        resizeModel: function(modelSpec) {
            viewer.replaceScene(new JSC3D.Scene());
            viewer.update();

            this.renderModel(modelSpec);
        }, 
        
    } 
    
}());