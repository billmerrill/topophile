var modelModel = (function() {
    "use strict";

    var canvas,
        viewer, 
        references, 
        showSizeReference = false, 
        comparisonMesh,
        
        buildComparison = function(scale) {
            if (!scale) {
                scale = [1,1,1]
            }
            var xform = {scale: scale, translate: [250,24.26,1]};
            comparisonMesh = references.token(xform);
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
            viewer.setParameter('RenderMode',       'flat');
            viewer.setParameter('Renderer',         'webgl');
            // viewer.setParameter('InitRotationX',     '-70');
            // viewer.setParameter('InitRotationY' ,    '45');
            viewer.init();
            viewer.update();
        },
      
        
       
        toggleSizeReference: function() {
            showSizeReference = !showSizeReference; 
            if (comparisonMesh) {
                var currScene = viewer.getScene();
                if (showSizeReference) {
                    currScene.addChild(comparisonMesh);
                } else {
                    currScene.removeChild(comparisonMesh);
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
            var currScene = viewer.getScene();
            currScene.removeChild(comparisonMesh);
            buildComparison([scale,scale,scale]);
            currScene.addChild(comparisonMesh);
            viewer.update();
        },
       
        showModel: function(modelUrl, width) {
            // viewer.replaceSceneFromUrl(modelUrl);
            buildComparison();
            var loader = new JSC3D.StlLoader;
            loader.onload = function(scene) {
                if (showSizeReference) {
                    scene.addChild(comparisonMesh);
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