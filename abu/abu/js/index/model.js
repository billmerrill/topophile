var indexModel = (function() {
    "use strict";

    var canvas,viewer, zFactor = 1, resetAABB = false;
     
    return {
        v: function() {
            return viewer;
        },
        
        init: function(displayCanvasId, initZFactor) {
            zFactor = initZFactor;
    		//JSC3D.console.setup('console-area', '120px');
            canvas = document.getElementById(displayCanvasId);
            viewer = new JSC3D.Viewer(canvas);
            // viewer.setParameter('ModelColor',       '#9999FF');
            viewer.setParameter('ModelColor',       '#aaaaaa');
            viewer.setParameter('Background',       'off');
            viewer.setParameter('BackgroundColor1', '#DDDDDD');
            viewer.setParameter('BackgroundColor2', '#DDDDDD');
            viewer.setParameter('RenderMode',       'flat');
            viewer.setParameter('Renderer',         'webgl');
            viewer.setParameter('InitRotationX',     '-60');
            viewer.setParameter('InitRotationY' ,    '30');
            viewer.setParameter('FaceCulling' ,    'off');
            viewer.setParameter('Definition',       'standard');
            
            viewer.beforeupdate = function() {
                // set Z axis distortion, aka height multiplier
                this.TOPOzScale = zFactor;
                var scene = this.getScene();
                if (scene) { 
                    if (resetAABB) {
                        this.baseAABBmaxZ = null;
                        this.baseAABBminZ = null;
                        resetAABB = false;
                    }
                    // save the original aabb, distort it like the model Z
                    if (!this.baseAABBmaxZ) {
                        this.baseAABBminZ = scene.aabb.minZ;
                        this.baseAABBmaxZ = scene.aabb.maxZ;
                    }
                }
            }
            
            viewer.init();
            viewer.update();
        },
       
        showModel: function(modelUrl) {
            resetAABB = true;
            viewer.replaceSceneFromUrl(modelUrl);
        },
        
        updateZFactor: function(newZFactor) {
            newZFactor = parseFloat(newZFactor);
            if (newZFactor > -100 && newZFactor < 100) {
                zFactor = newZFactor;
            }
            viewer.update();
        },
        
        getZFactor: function() {
            return zFactor;
        },
        
        resetScene: function() {
            viewer.resetScene();
            viewer.update();
        }
    } 
    
}());