TOPO.BUILD1.Terrain = (function() {
    "use strict";

    var canvas, 
        viewer, 
        busyDisplay, 
        canvasJQ, 
        zFactor = 1, 
        newTerrainCallback,
        resetAABB = false,
        terrainBounds = {},
        terrainRect,
        backgroundColor = '#d4e1ff',
        
        resetScene =  function() {
            viewer.resetScene();
            viewer.update();
        },
        
        /*
         * bounds: the geographic bounds of the model
         * targetBoundsRatio: the size of the model in pixels from a map in 
         *      spherical mercator, epgs:3857.  Used to scale wcs request
         */
        requestTerrainModel = function(bounds, selectionRect) {
            var newBounds = bounds;
            var imageSize;
            showBusy();
            var requestData = {'nwlat': bounds.nwlat,
                'nwlon': bounds.nwlon,
                'selat': bounds.selat,
                'selon': bounds.selon,
                'size': TOPO.BUILD1.getConfig('terrainSize'), 
                'rez': TOPO.BUILD1.getConfig('terrainRez'),
                'zfactor': 1,
                'model_style': 'preview'};
                
            if (TOPO.BUILD1.getConfig('enableMsScaling')) {
                imageSize = TOPO.BUILD1.Utils.scaleRectToMaxLength(selectionRect, 
                                                    TOPO.BUILD1.getConfig('terrainRez'));
                requestData['width'] = imageSize.x;
                requestData['height'] = imageSize.y ;
            }
            
            $.ajax({
                type: "GET",
                url: TOPO.BUILD1.getConfig('bamService'),
                data: requestData
            })
            .done(function(data, status, jqxhr) {
                terrainBounds = newBounds;
                terrainRect = selectionRect;
                showModel(data['url']);
                newTerrainCallback();
                boundsBuffer.completed();
            })
            .fail(function(data, stats, error) {
                showModal("The model engine is having trouble right now.  Please try again later.")
                boundsBuffer.completed();
                hideBusy();
            });
        },
        
        showModel = function(modelUrl) {
            resetAABB = true;
            var loader = new JSC3D.StlLoader;
            loader.onload = function(scene) {
                viewer.replaceScene(scene);
                hideBusy();
            };
            loader.loadFromUrl(modelUrl);
        },    
        
        
        showBusy = function() {
            busyDisplay.show();
            canvasJQ.hide();
        },
        
        hideBusy = function() {
            busyDisplay.hide();
            canvasJQ.show();
        },
        
        zoomIn = function() {
            viewer.zoomFactor *= 1.3;
            viewer.update();
        },
        
        zoomOut = function() {
            viewer.zoomFactor /= 1.3;
            viewer.update();
        },
        
        showModal = function(msg) {
            $('#modal-message').html(msg);
            $('.modal').modal({keyboard: true});
        },
       
        // a singleton to limit calls for terrain previews
        // ignore all but the last bounds requests while a preview is building
        boundsBuffer = function() {
            var isReady = true,
                savedBounds, 
                savedRect;
            
            return {
                reset: function() {
                    isReady: true; 
                    savedBounds = savedRect = null
                },
                completed: function() {
                    if (savedBounds) {
                        requestTerrainModel(savedBounds, savedRect);
                        savedBounds = savedRect = null;
                        isReady = false;
                    } else {
                        isReady = true;
                    }
                },
                getTerrain: function(bounds, rect) {
                    if (isReady) {
                        requestTerrainModel(bounds, rect);
                        isReady = false;
                    } else {
                        savedBounds = bounds;
                        savedRect = rect;
                    }
                }    
            }
        }();
     
    return {
        v: function() {
            return viewer;
        },
        
        init: function(displayCanvasId, initZFactor, progressDisplayId, newTerrainCb, resetViewId) {
            zFactor = initZFactor;
            canvas = document.getElementById(displayCanvasId);
            viewer = new JSC3D.Viewer(canvas);
            busyDisplay = $('#' + progressDisplayId);
            busyDisplay.hide();
            canvasJQ = $('#' + displayCanvasId);
            newTerrainCallback = newTerrainCb;
            $("#" + resetViewId).click(function() {
                resetScene();
            })
            
            canvasJQ.hide();
            viewer.setParameter('ModelColor',       '#aaaaaa');
            viewer.setParameter('Background',       'on');
            viewer.setParameter('BackgroundColor1', backgroundColor);
            viewer.setParameter('BackgroundColor2', backgroundColor);
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
            
            viewer.mouseWheelHandler = function(e){return;};
            viewer.init();
            viewer.update();
            
            $('#terrain-zoomin').click(function(){
                zoomIn();
            });
            $('#terrain-zoomout').click(function(){
                zoomOut();
            });
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
        
        renderBounds: function(bounds, rect) {
            boundsBuffer.getTerrain(bounds, rect);
        },
        
        getBounds: function() {
            return terrainBounds;
        },
        
        getSelectionRect: function() {
            return terrainRect;
        }
    }
}());