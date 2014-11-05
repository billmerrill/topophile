var indexModel = (function() {
    var canvas,viewer;
     
    return {
       init: function(displayCanvasId) {
            canvas = document.getElementById(displayCanvasId);
            viewer = new JSC3D.Viewer(canvas);
            viewer.setParameter('ModelColor',       '#9999FF');
            viewer.setParameter('BackgroundColor1', '#DDDDDD');
            viewer.setParameter('BackgroundColor2', '#DDDDDD');
            viewer.setParameter('RenderMode',       'flat');
            viewer.init();
            viewer.update();
       },
       
       showModel: function(modelUrl) {
           viewer.replaceSceneFromUrl(modelUrl);
       }
       
    } 
    
}());