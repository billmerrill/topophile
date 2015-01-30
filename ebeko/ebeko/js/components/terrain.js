TOPO.BUILD1.Terrain = (function() {
    "use strict";

    var canvas, 
        viewer, 
        busyDisplay, 
        canvasJQ, 
        zFactor = 1, 
        resetAABB = false,
        terrainBounds = {};
     
    return {
        v: function() {
            return viewer;
        },
        
        init: function(displayCanvasId, initZFactor, progressDisplayId) {
            zFactor = initZFactor;
    		//JSC3D.console.setup('console-area', '120px');
            canvas = document.getElementById(displayCanvasId);
            viewer = new JSC3D.Viewer(canvas);
            busyDisplay = $('#' + progressDisplayId);
            busyDisplay.hide();
            canvasJQ = $('#' + displayCanvasId);
            canvasJQ.hide();
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
        }, 
        
        showBusy: function() {
            busyDisplay.show();
            canvasJQ.hide();
        },
        
        hideBusy: function() {
            busyDisplay.hide();
            canvasJQ.show();
        },
        
        renderBounds: function(bounds) {
            var thee = this;
            var newBounds = bounds;
            $.ajax({
                type: "GET",
                url: TOPO.BUILD1.getConfig('bamService'),
                data: { 'nwlat': bounds.nwlat,
                'nwlon': bounds.nwlon,
                'selat': bounds.selat,
                'selon': bounds.selon,
                'size': TOPO.BUILD1.getConfig('terrainSize'), 
                'rez': TOPO.BUILD1.getConfig('terrainRez'),
                'zfactor': 1,
                'model_style': 'preview'}
            })
            .done(function(data, status, jqxhr) {
                terrainBounds = newBounds;
                thee.showModel(data['url']);
            })
            .fail(function(data, stats, error) {
                alert("Sorry, I couldn't build a model.")
            })
            .always(function(data) {
                thee.hideBusy();
            });
        }, 
        
        getBounds: function() {
            return terrainBounds;
        }
    }
}());