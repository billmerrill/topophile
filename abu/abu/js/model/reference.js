referenceObjects = (function() {
    var

    getUSQuarterChip = function(transform) {
        
        var vertices = [
            0.0, 0.0, 0.0,
            0.0, 0.0, 1.75,
            24.26, 0.0, 0.0,
            24.26, 0.0, 1.75,
            0.0, 24.26, 0.0,
            0.0, 24.26, 1.75,
            24.26, 24.26, 0.0,
            24.26, 24.26, 1.75];
        
        var indicies = [ 0, 2, 3, 1, -1,
                         2, 6, 7, 3, -1,
                         6, 4, 5, 7, -1,
                         4, 0, 1, 5, -1,
                         1, 3, 7, 5, -1,
                         0, 4, 6, 2, -1];
                         
        if (transform) {
            var vn = [];
            var i = j = 0;
            while (i < vertices.length) {
                var nx = vertices[i] * transform['scale'][0] + transform['translate'][0]
                var ny = vertices[i+1] * transform['scale'][1] + transform['translate'][1]
                var nz = vertices[i+2] * transform['scale'][2] + transform['translate'][2]
                i += 3;
                vn[j++] = nx;
                vn[j++] = ny;
                vn[j++] = nz;
            }
            vertices = vn;
        }
        
		var mesh = new JSC3D.Mesh;
		mesh.name = 'token';
        mesh.isDoubleSided = false;

		mesh.vertexBuffer = vertices;
        mesh.indexBuffer = indicies;
		mesh.init();
		return mesh;
	}; 
 
  
    return {
        token: function(transform) {
            return getUSQuarterChip(transform);
        },
        quarter: function() {
            
        }
    }
    
}());