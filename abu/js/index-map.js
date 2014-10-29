var indexMap = (function() {

    return { 
        init: function() {
            var raster = new ol.layer.Tile({
                source: new ol.source.MapQuest({layer: 'sat'})
            });

            var currentExtent;

            var map = new ol.Map({
                target: 'map',
                layers: [ raster],
                view: new ol.View({
                    center: ol.proj.transform([131.6, 34.5], 'EPSG:4326', 'EPSG:3857'),
                    zoom: 11
                })
            });


            var selectionInteraction;
            selectionInteraction = new ol.interaction.DragBox({
                // condition: ol.events.condition.always,
                style: new ol.style.Style({
                    stroke: new ol.style.Stroke({
                        color: '#33ff33',
                        width: 1 
                    })
                })
            });
            map.addInteraction(selectionInteraction);

            var scaleSelectron = function(ext)  {
                var nwpix = map.getPixelFromCoordinate(ol.extent.getTopLeft(ext));
                var sepix = map.getPixelFromCoordinate(ol.extent.getBottomRight(ext));
                var awidth = sepix[0] - nwpix[0];
                var aheight = sepix[1] - nwpix[1];
                $(selectron.getElement()).width(awidth).height(aheight);
            }

            var selectron = new ol.Overlay( {
                element: $("#extent-selector")
            });    
            map.addOverlay(selectron);


            selectionInteraction.on('boxstart', function(e) {
                $(selectron.getElement()).hide();
            })

            selectionInteraction.on('boxend', function(e){
                var selextent = selectionInteraction.getGeometry().getExtent();
                currentExtent = ol.proj.transformExtent(selextent, 'EPSG:3857','EPSG:4326');
                scaleSelectron(selextent);
                selectron.setPosition([selextent[0], selextent[3]]);
                $(selectron.getElement()).show();
                $('#map-info').text(
                        ol.coordinate.format([currentExtent[0], currentExtent[3]], "{x}, {y}", 2) + " by  " +
                        ol.coordinate.format([currentExtent[2], currentExtent[1]], "{x}, {y}", 2));
                map.removeInteraction(selectionInteraction);
            });
        }
    }

}());