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
       
       ashowModel: function(modelUrl) {
            viewer.setParameter('SceneUrl',         modelUrl);
            // viewer.setParameter('ModelColor',       '#CAA618');
            viewer.setParameter('ModelColor',       '#9999FF');
            // viewer.setParameter('BackgroundColor1', '#E5D7BA');
            // viewer.setParameter('BackgroundColor2', '#383840');
            viewer.setParameter('BackgroundColor1', '#DDDDDD');
            viewer.setParameter('BackgroundColor2', '#DDDDDD');
            viewer.setParameter('RenderMode',       'flat');
            // viewer.setParameter('Renderer',       'webgl');
            viewer.init();
            viewer.update();
       },
       
       showModel: function(modelUrl) {
           viewer.replaceSceneFromUrl(modelUrl);
       }
       
    } 
    
}());