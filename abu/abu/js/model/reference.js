referenceObjects = (function() {
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
    }
    
    USQuarter = function(transform) {
        var vertices = [
            -24.26, 0, 0         ,
            -23.073, 7.497, 0    ,
            -19.627, 14.26, 0    ,
            -14.26, 19.627, 0    ,
            -7.497, 23.073, 0    ,
            0, 24.26, 0          ,
            7.497, 23.073, 0     ,
            14.26, 19.627, 0     ,
            19.627, 14.26, 0     ,
            23.073, 7.497, 0     ,
            24.26, 0, 0          ,
            
            23.073, -7.497, 0    ,
            19.627, -14.26, 0    ,
            14.26, -19.627, 0    ,
            7.497, -23.073, 0    ,
            0, -24.26, 0         ,
            -7.497, -23.073, 0   ,
            -14.26, -19.627, 0   ,
            -19.627, -14.26, 0   ,
            -23.073, -7.497, 0   ,
            
            -24.26, 0, 1.75      ,
            -23.073, 7.497, 1.75 ,
            -19.627, 14.26, 1.75 ,
            -14.26, 19.627, 1.75 ,
            -7.497, 23.073, 1.75 ,
            0, 24.26, 1.75       ,
            7.497, 23.073, 1.75  ,
            14.26, 19.627, 1.75  ,
            19.627, 14.26, 1.75  ,
            23.073, 7.497, 1.75  ,
            24.26, 0, 1.75       ,
            23.073, -7.497, 1.75 ,
            19.627, -14.26, 1.75 ,
            14.26, -19.627, 1.75 ,
            7.497, -23.073, 1.75 ,
            0, -24.26, 1.75      ,
            -7.497, -23.073, 1.75,
            -14.26, -19.627, 1.75,
            -19.627, -14.26, 1.75,
            -23.073, -7.497, 1.75];    
            

        var indicies = [
            0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,0,-1,
            39,38,37,36,35,34,33,32,31,30,29,28,27,26,25,24,23,22,21,20,39,-1,
            19,18,38,39,-1,
            18,17,37,38,-1,
            17,16,36,37,-1,
            16,15,35,36,-1,
            15,14,34,35,-1,
            14,13,33,34,-1,
            13,12,32,33,-1,
            12,11,31,32,-1,
            11,10,30,31,-1,
            10,9,29,30,-1,
            9,8,28,29,-1, 
            8,7,27,28,-1,
            7,6,26,27,-1,
            6,5,25,26,-1,
            5,4,24,25,-1,
            4,3,23,24,-1,
            3,2,22,23,-1,
            2,1,21,22,-1,
            1,0,20,21,-1,
            0,19,39,20,-1 ]; 
    
        if (transform) {
            vertices = transformVertices(vertices, tranform);
        }
        
        var mesh = new JSC3D.Mesh;
        mesh.name = 'token';
        mesh.isDoubleSided = false; 

        mesh.vertexBuffer = vertices;
        mesh.indexBuffer = indicies;
        
        // (name, ambientColor, diffuseColor, transparency, simulateSpecular)
        mesh.setMaterial(new JSC3D.Material('coiny', 0, 0x00cc00));
        
        mesh.init();
        return mesh;
        
    },
    
    AutoDisc = function(transform) {
        var vertices = [-24.26, 0, 0         ,
            -23.073, 7.497, 0    ,
            -19.627, 14.26, 0    ,
            -14.26, 19.627, 0    ,
            -7.497, 23.073, 0    ,
            0, 24.26, 0          ,
            7.497, 23.073, 0     ,
            14.26, 19.627, 0     ,
            19.627, 14.26, 0     ,
            24.26, 0, 0          ,
            23.073, 7.497, 0     ,
            0, -24.26, 0         ,
            23.073, -7.497, 0    ,
            19.627, -14.26, 0    ,
            14.26, -19.627, 0    ,
            7.497, -23.073, 0    ,
            -7.497, -23.073, 0   ,
            -14.26, -19.627, 0   ,
            -19.627, -14.26, 0   ,
            -23.073, -7.497, 0   ,
            -19.627, 14.26, 1.75 ,
            -23.073, 7.497, 1.75 ,
            -24.26, 0, 1.75      ,
            -14.26, 19.627, 1.75 ,
            0, 24.26, 1.75       ,
            -7.497, 23.073, 1.75 ,
            14.26, 19.627, 1.75  ,
            7.497, 23.073, 1.75  ,
            19.627, 14.26, 1.75  ,
            24.26, 0, 1.75       ,
            23.073, 7.497, 1.75  ,
            0, -24.26, 1.75      ,
            19.627, -14.26, 1.75 ,
            23.073, -7.497, 1.75 ,
            14.26, -19.627, 1.75 ,
            7.497, -23.073, 1.75 ,
            -14.26, -19.627, 1.75,
            -7.497, -23.073, 1.75,
            -19.627, -14.26, 1.75,
            -23.073, -7.497, 1.75];

        var indicies = [
            19, 39, 0  ,-1,
            0, 39, 22  ,-1,
            1, 2, 0    ,-1,
            0, 2, 3    ,-1,
            0, 3, 4    ,-1,
            0, 4, 5    ,-1,
            0, 5, 6    ,-1,
            0, 6, 7    ,-1,
            0, 7, 8    ,-1,
            0, 8, 10   ,-1,
            0, 10, 9   ,-1,
            0, 9, 12   ,-1,
            0, 12, 13  ,-1,
            0, 13, 14  ,-1,
            0, 14, 15  ,-1,
            0, 15, 11  ,-1,
            0, 11, 16  ,-1,
            0, 16, 17  ,-1,
            0, 17, 18  ,-1,
            0, 18, 19  ,-1,
            22, 21, 0  ,-1,
            0, 21, 1   ,-1,
            22, 39, 38 ,-1,
            37, 22, 36 ,-1,
            36, 22, 38 ,-1,
            31, 22, 37 ,-1,
            35, 22, 31 ,-1,
            34, 22, 35 ,-1,
            32, 22, 34 ,-1,
            33, 22, 32 ,-1,
            29, 22, 33 ,-1,
            30, 22, 29 ,-1,
            28, 22, 30 ,-1,
            26, 22, 28 ,-1,
            27, 22, 26 ,-1,
            24, 22, 27 ,-1,
            25, 22, 24 ,-1,
            23, 22, 25 ,-1,
            20, 22, 23 ,-1,
            21, 22, 20 ,-1,
            18, 38, 19 ,-1,
            19, 38, 39 ,-1,
            18, 17, 36 ,-1,
            38, 18, 36 ,-1,
            17, 16, 37 ,-1,
            36, 17, 37 ,-1,
            16, 11, 31 ,-1,
            37, 16, 31 ,-1,
            11, 15, 35 ,-1,
            31, 11, 35 ,-1,
            15, 14, 34 ,-1,
            35, 15, 34 ,-1,
            14, 13, 32 ,-1,
            34, 14, 32 ,-1,
            13, 12, 33 ,-1,
            32, 13, 33 ,-1,
            12, 9, 29  ,-1,
            33, 12, 29 ,-1,
            10, 30, 29 ,-1,
            9, 10, 29  ,-1,
            8, 28, 30  ,-1,
            10, 8, 30  ,-1,
            26, 28, 7  ,-1,
            7, 28, 8   ,-1,
            27, 26, 6  ,-1,
            6, 26, 7   ,-1,
            24, 27, 5  ,-1,
            5, 27, 6   ,-1,
            25, 24, 4  ,-1,
            4, 24, 5   ,-1,
            23, 25, 3  ,-1,
            3, 25, 4   ,-1,
            20, 23, 2  ,-1,
            2, 23, 3   ,-1,
            21, 20, 1  ,-1,
            1, 20, 2   ,-1]; 
     
    
        if (transform) {
            vertices = transformVertices(vertices, transform);
        }
        
        var mesh = new JSC3D.Mesh;
        mesh.name = 'token';
        mesh.isDoubleSided = true;

        mesh.vertexBuffer = vertices;
        mesh.indexBuffer = indicies;
        
        // (name, ambientColor, diffuseColor, transparency, simulateSpecular)
        mesh.setMaterial(new JSC3D.Material('coiny', 0, 0xcccccc));
        
        mesh.init();
        return mesh;
        
    },
    
    NewUSOneDollar = function(transform) {
        var frontTexUrl = "assets/textures/sm-dollar-front.jpg";
        var backTexUrl = "assets/textures/sm-dollar-back.jpg";
        
        var front = new JSC3D.Mesh('front');
        front.isDoubleSided = false;
        front.vertexBuffer = [ 0.0, 0.0, .11,
                                66.3, 0.0, .11,
                                66.3, 156, .11,
                                0.0, 156, .11];
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
                                66.3, 0.0, .0,
                                66.3, 156, .0,
                                0.0, 156, .0];
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
            0.0, 0.0, .11,
            66.3, 0.0, 0.0,
            66.3, 0.0, .11,
            0.0, 156 , 0.0,
            0.0, 156, .11,
            66.3, 156, 0.0,
            66.3, 156, .11 ];
        
        sides.indexBuffer = [ 0, 2, 3, 1, -1,
                             2, 6, 7, 3, -1,
                             6, 4, 5, 7, -1,
                             4, 0, 1, 5, -1 ];
        if (transform) {
            sides.vertexBuffer = transformVertices(sides.vertexBuffer, transform);
        }
        sides.init();
                         
        return [front,back,sides]
    }; 

    USOneDollar = function(transform) {
        var vertices = [
            0.0, 0.0, 0.0,
            0.0, 0.0, .11,
            66.3, 0.0, 0.0,
            66.3, 0.0, .11,
            0.0, 156 , 0.0,
            0.0, 156, .11,
            66.3, 156, 0.0,
            66.3, 156, .11 ];
        
        var indicies = [ 0, 2, 3, 1, -1,
                         2, 6, 7, 3, -1,
                         6, 4, 5, 7, -1,
                         4, 0, 1, 5, -1,
                         1, 3, 7, 5, -1,
                         0, 4, 6, 2, -1];
                         
        if (transform) {
            vertices = transformVertices(vertices, transform);
        }
        
        var mesh = new JSC3D.Mesh('comparison');
        mesh.isDoubleSided = false;

        mesh.vertexBuffer = vertices;
        mesh.indexBuffer = indicies;
        
        // var dollarBackTexture = new JSC3D.Texture;
        // dollarBackTexture.onready = function() {
        //     mesh.setTexture(dollarBackText);
        // };
        // dollarBackTexture.createFromUrl('assets/textures/sm-dollar-back.jpg');
        // 
        mesh.init();
        return mesh;
    }; 

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
        token: function(transform) {
        // return USQuarter(transform);
        // return USOneDollar(transform);
        return NewUSOneDollar(transform);
        }
    }
    
}());