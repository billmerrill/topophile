TOPO.BUILD1.Utils = (function() {
    return {
        scaleRectToMaxLength: function(rectSize, maxLength) {
            var s = {x:0, y:0};
            if (rectSize.x > rectSize.y) {
                s.x = maxLength;
                s.y = maxLength * (rectSize.y / rectSize.x);
            } else {
                s.y = maxLength;
                s.x = maxLength * (rectSize.x / rectSize.y);
            }
            return s;
        }    
    }
}());