TOPO.BUILD1.Utils = (function() {
    return {
        scaleRectToMaxLength: function(rectSize, maxLength) {
            var s = {x:0, y:0};
            if (rectSize[0] > rectSize[1]) {
                s[0] = maxLength;
                s[1] = maxLength * (rectSize[1] / rectSize[0]);
            } else {
                s[1] = maxLength;
                s[0] = maxLength * (rectSize[0] / rectSize[1]);
            }
            return s;
        }    
    }
}());