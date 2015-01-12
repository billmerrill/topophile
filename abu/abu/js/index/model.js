var indexModel = (function() {
    "use strict";

    var canvas,viewer;
     
    return {
       init: function(displayCanvasId) {
    		//JSC3D.console.setup('console-area', '120px');
            canvas = document.getElementById(displayCanvasId);
            viewer = new JSC3D.Viewer(canvas);
            viewer.setParameter('ModelColor',       '#9999FF');
            viewer.setParameter('Background',       'off');
            viewer.setParameter('BackgroundColor1', '#DDDDDD');
            viewer.setParameter('BackgroundColor2', '#DDDDDD');
            viewer.setParameter('RenderMode',       'texture');
            // viewer.setParameter('RenderMode',       'texturesmooth');
            viewer.setParameter('Renderer',         'webgl');
            viewer.setParameter('InitRotationX',     '-80');
            viewer.setParameter('InitRotationY' ,    '30');
            
            viewer.init();
            viewer.update();
       },
       
       showModel: function(modelUrl) {
           viewer.replaceSceneFromUrl(modelUrl);
           viewer.onloadingcomplete = function() {
               var makeDoubleSided = function(child) {
                   child.isDoubleSided = true;
               };
               this.getScene().forEachChild(makeDoubleSided);
           }
       }
    } 
    
}());