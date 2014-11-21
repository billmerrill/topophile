var modelModel = (function() {
    "use strict";

    var canvas,
        viewer, 
        references, 
        showSizeReference = false, 
        comparisonMeshParts,
        
        buildComparison = function(scale) {
            if (!scale) {
                scale = [1,1,1]
            }
            var xform = {scale: scale, translate: [250,24.26,1]};
            comparisonMeshParts = references.token(xform);
        }; 
     
    return {
        init: function(displayCanvasId, referenceModule) {
            references = referenceModule;
    		//JSC3D.console.setup('console-area', '120px');
            canvas = document.getElementById(displayCanvasId);
            viewer = new JSC3D.Viewer(canvas);
            viewer.setParameter('ModelColor',       '#9999FF');
            viewer.setParameter('Background',       'off');
            viewer.setParameter('BackgroundColor1', '#DDDDDD');
            viewer.setParameter('BackgroundColor2', '#DDDDDD');
            viewer.setParameter('RenderMode',       'texture');
            viewer.setParameter('Renderer',         'webgl');
            // viewer.setParameter('InitRotationX',     '-70');
            // viewer.setParameter('InitRotationY' ,    '45');
            viewer.init();
            viewer.update();
        },
      
        
       
        toggleSizeReference: function() {
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
       
        showChit: function() {
            var scene = new JSC3D.Scene();
            scene.addChild(references.token());
            viewer.replaceScene(scene);
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
            buildComparison();
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
        
        resetScene: function() {
            viewer.resetScene();
            viewer.update();
        }
        
       
    } 
    
}());