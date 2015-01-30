TOPO.BUILD1.Model = (function() {
    "use strict";

    var canvas, jcanvas,
        viewer, 
        references = TOPO.BUILD1.ModelReferenceObjects, 
        showSizeReference = false, 
        comparisonMeshParts,
        modelWidth = 100,
        busyDisplay,
        resetButton,
        compareButton,
        newModelCallback,
        
        buildComparison = function(scale) {
            if (!scale) {
                scale = [1,1,1]
            }
            var xform = {scale: scale, translate: [modelWidth + 10 ,0,1]};
            comparisonMeshParts = TOPO.BUILD1.ModelReferenceObjects.token(xform);
        },
        
        initViewer = function() {
            viewer = new JSC3D.Viewer(canvas);
            viewer.setParameter('ModelColor',       '#9999FF');
            viewer.setParameter('Background',       'off');
            viewer.setParameter('BackgroundColor1', '#DDDDDD');
            viewer.setParameter('BackgroundColor2', '#DDDDDD');
            viewer.setParameter('RenderMode',       'texturesmooth');
            viewer.setParameter('Renderer',         'webgl');
            viewer.setParameter('InitRotationX',     '-80');
            viewer.setParameter('InitRotationY' ,    '30');
            viewer.init();
            viewer.update();
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
        
        resetScene = function() {
            viewer.resetScene();
            viewer.update();
        } 
    
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
            initViewer();
        },
       
        scaleReferenceObject: function(scale) {
            var i;
            var currScene = viewer.getScene();
            for (i in comparisonMeshParts) {
                currScene.removeChild(comparisonMeshParts[i]);
            }
            buildComparison([scale,scale,scale]);
            if (showSizeReference) {
                for (i in comparisonMeshParts) {
                    currScene.addChild(comparisonMeshParts[i]);
                }
            }
            viewer.update();
        },
       
        showModel: function(modelUrl, width) {
            // viewer.replaceSceneFromUrl(modelUrl);
            modelWidth = width
            buildComparison([1,1,1]);
            var loader = new JSC3D.StlLoader;
            loader.onload = function(scene) {
                if (showSizeReference) {
                    var i;
                    for (i in comparisonMeshParts) {
                        currScene.addChild(comparisonMeshParts[i]);
                    }
                }
                    viewer.replaceScene(scene);
            };
            loader.loadFromUrl(modelUrl);
        },
        
        showBusy: function() {
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
            $.ajax({
                type: "GET",
                url: TOPO.BUILD1.getConfig('bamService'),
                data: { 'nwlat': modelSpec.nwlat,
                        'nwlon': modelSpec.nwlon,
                        'selat': modelSpec.selat,
                        'selon': modelSpec.selon,
                        'size': TOPO.BUILD1.getConfig('modelSize'), 
                        'rez': TOPO.BUILD1.getConfig('modelRez'), //400 dots per 100 mm ~= 100dpi
                        'zfactor': modelSpec.zfactor,
                        'hollow': 1}
            })
            .done(function(data, status, jqxhr) {
                thee.showModel(data['url'], data['x-size-mm']);
                // sizeTools.setSize(data['x-size-mm'], data['y-size-mm'], data['z-size-mm']);
                // sizeTools.initPresets();
                thee.currentModelId = data['model_id'];
                // setSendButton(data['model_id'] + ".stl");
                // setPricing(data['model_id'])
                newModelCallback(data);

            })
            .fail(function(data, stats, error) {
                alert("Sorry, I couldn't build a model.")
            })
            .always(function(data) {
                thee.hideBusy();
            });
        },
       
    } 
    
}());