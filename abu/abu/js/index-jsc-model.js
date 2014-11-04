var indexModel = (function() {
    var canvas,viewer;
     
    return {
       init: function(displayCanvasId) {
            canvas = document.getElementById(displayCanvasId);
            viewer = new JSC3D.Viewer(canvas);
       },
       
       showModel: function(modelUrl) {
            viewer.setParameter('SceneUrl',         modelUrl);
            // viewer.setParameter('ModelColor',       '#CAA618');
            viewer.setParameter('ModelColor',       '#999999');
            // viewer.setParameter('BackgroundColor1', '#E5D7BA');
            // viewer.setParameter('BackgroundColor2', '#383840');
            viewer.setParameter('BackgroundColor1', '#FFFFFF');
            viewer.setParameter('BackgroundColor2', '#FFFFFF');
            viewer.setParameter('RenderMode',       'flat');
            viewer.setParameter('Renderer',       'webgl');
            viewer.init();
            viewer.update();
       }
       
    } 
    
}());