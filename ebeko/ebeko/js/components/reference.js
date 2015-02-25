TOPO.BUILD1.ModelReferenceObjects = (function() {
    var
    
    transformVertices = function(vin, transform) {
        var vout = [];
        var i = j = 0;
        while (i < vin.length) {
            var nx = vin[i] * transform['scale'][0] + transform['translate'][0]
            var ny = vin[i+1] * transform['scale'][1] + transform['translate'][1]
            var nz = vin[i+2] * transform['scale'][2] + transform['translate'][2]
            i += 3;
            vout[j++] = nx;
            vout[j++] = ny;
            vout[j++] = nz;
        }
        return vout
    },
    
    GenericCube = function(x,y,z,transform, frontTexUrl, backTexUrl) {
        var front = new JSC3D.Mesh('front');
        front.isDoubleSided = false;
        front.vertexBuffer = [ 0.0, 0.0, z,
                                x, 0.0, z,
                                x,y,z,
                                0.0, y, z];
        front.indexBuffer = [0, 1, 2, 3, -1];
        front.texCoordBuffer = [ 0, 0, 
                                1, 0, 
                                1, 1, 
                                0, 1 ];
        front.texCoordIndexBuffer = [0, 3,2,1,-1];
        if (transform) {
            front.vertexBuffer = transformVertices(front.vertexBuffer, transform);
        }
        front.init();
        var frontTex = new JSC3D.Texture;
        frontTex.onready = function() {
            front.setTexture(frontTex);
        };
        frontTex.createFromUrl(frontTexUrl);
        
        
        var back = new JSC3D.Mesh('back');
        back.isDoubleSided = false;
        back.vertexBuffer = [ 0.0, 0.0, .0,
                                x, 0.0, .0,
                                x, y, .0,
                                0.0, y, .0];
        back.indexBuffer = [0, 3, 2, 1, -1];
        back.texCoordBuffer = [ 0, 0, 
                                1, 0, 
                                1, 1, 
                                0, 1 ];
        back.texCoordIndexBuffer = [1, 0, 3,2,-1];
        if (transform) {
            back.vertexBuffer = transformVertices(back.vertexBuffer, transform);
        }
        back.init();
        var backTex = new JSC3D.Texture;
        backTex.onready = function() {
            back.setTexture(backTex);
        };
        backTex.createFromUrl(backTexUrl);
            
        var sides = new JSC3D.Mesh('sides');
        sides.isDoubleSided = false;
        sides.vertexBuffer = [
            0.0, 0.0, 0.0,
            0.0, 0.0, z,
            x, 0.0, 0.0,
            x, 0.0, z,
            0.0, y , 0.0,
            0.0, y, z,
            x,y,0.0,
            x,y,z];
        
        sides.indexBuffer = [ 0, 2, 3, 1, -1,
                             2, 6, 7, 3, -1,
                             6, 4, 5, 7, -1,
                             4, 0, 1, 5, -1 ];
        if (transform) {
            sides.vertexBuffer = transformVertices(sides.vertexBuffer, transform);
        }
        sides.init();
                         
        return [front,back,sides]
    },
    
    OneDollarModel = function(transform) {
        return GenericCube(66.3, 156, .11, transform, 
                "assets/textures/sm-dollar-front.jpg",
                 "assets/textures/sm-dollar-back.jpg");
    },
    
    EuroModelBill = function(transform) {
        return GenericCube(62, 120, .11, transform, 
                "assets/textures/five-euro-front.jpg",
                 "assets/textures/five-euro-back.jpg");
        return GenericCub
    },
    
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
            vertices = transformVertices(vertices, transform);
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
        dollar: function(transform) {
            return OneDollarModel(transform);
        },
        
        euro: function(transform) {
            return EuroModelBill(transform);
        }
    
    }
    
}());