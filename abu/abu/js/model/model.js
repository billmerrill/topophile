var modelModel = (function() {
    "use strict";

    var canvas,viewer, references;
     
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
       
       showChit: function() {
            var scene = new JSC3D.Scene();
            scene.addChild(references.token());
            viewer.replaceScene(scene);
       },
       
       showModel: function(modelUrl, width) {
            // viewer.replaceSceneFromUrl(modelUrl);
            var xform = {scale: [1,1,1], translate: [250,24.26,1]};
            var loader = new JSC3D.StlLoader;
            loader.onload = function(scene) {
                scene.addChild(references.token(xform));
                viewer.replaceScene(scene);
            };
            loader.loadFromUrl(modelUrl);
       }
       
    } 
    
}());