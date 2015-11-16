


Header  = '''#VRML V2.0 utf8

Viewpoint {position 10 20 10 }

WorldInfo {
    title "Topophile Terrain Model"
    info  [ "Build your own terrain model at topophile.com" ]
}
'''

BasicAppearance = '''
    appearance Appearance {
		material Material { }
    }'''

TerrainAppearance = '''
    appearance Appearance {
		material Material { }
		texture ImageTexture { url "terrain.png" }
    }'''

ElevationGrid = '''Shape {
	$appearance
	geometry ElevationGrid {
		solid FALSE
		xDimension $x_dimension
		zDimension $z_dimension
		xSpacing $x_spacing
		zSpacing $z_spacing
		height [
			$height_scalar
		]
	}
}'''

IndexedFaceSet =''' Shape {
	appearance Appearance {
		material Material { }
	}

	geometry IndexedFaceSet {
		convex $convex
		solid FALSE
		coord Coordinate { point [ $points ] }
		coordIndex [ $coordinates ]
	}
}'''
