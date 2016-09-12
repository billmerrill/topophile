


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
		texture ImageTexture { url "terrain.png" }
        textureTransform TextureTransform{
            scale 1 -1
            rotation 0
            center 0 0
            translation 0 0
        }
    }'''

ElevationGrid = '''Shape {
    # $comment
	$appearance
	geometry ElevationGrid {
		solid TRUE
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
    # $comment
	appearance Appearance {
		material Material { }
	}

	geometry IndexedFaceSet {
		convex $convex
		solid $solid
        ccw $ccw
		coord Coordinate { point [ $points ] }
		coordIndex [ $coordinates ]
	}
}'''

DisplayAxes = '''

PROTO SimpleAxis [field SFNode axisAppearance NULL] {
  Transform {
    translation 0 5 0
    children [
      Shape {
        appearance IS axisAppearance
        geometry Cylinder {radius 0.1 height 10}
      }
      Transform {
        translation 0 5.5 0
        children [
          Shape {
            appearance IS axisAppearance
            geometry Cone {bottomRadius 0.25 height 1}
          }
        ]
      }

    ]
  }
}

# Red X-axis

Transform {
  rotation 0 0 1 -1.57080
  children [
    SimpleAxis {
      axisAppearance Appearance {material Material {diffuseColor 1 0 0}}
    }
    Transform {
        translation 0 11 0
        children [
            Shape {
              appearance Appearance {
                  material Material {
                        diffuseColor 1 1 0
                  }
              }
              geometry Text {
                string "X Axis"
                fontStyle FontStyle {
                    size 1
                }
              }
          }
      ]
    }
  ]
}

# Green Y-axis

Transform {
  children [
    SimpleAxis {
      axisAppearance Appearance {material Material {diffuseColor 0 1 0}}
    }
        Transform {
            translation 0 11 0
            children [
                Shape {
                  appearance Appearance {
                      material Material {
                            diffuseColor 1 1 0
                      }
                  }
                  geometry Text {
                    string "Y Axis"
                    fontStyle FontStyle {
                        size 1
                    }
                  }
              }
          ]
        }
  ]
}

# Blue Z-axis

Transform {
  rotation 1 0 0 1.57080
  children [
    SimpleAxis {
      axisAppearance Appearance {material Material {diffuseColor 0 0 1}}
    }
        Transform {
            translation 0 11 0
            children [
                Shape {
                  appearance Appearance {
                      material Material {
                            diffuseColor 1 1 0
                      }
                  }
                  geometry Text {
                    string "Z Axis"
                    fontStyle FontStyle {
                        size 1
                    }
                  }
              }
          ]
        }
  ]
}

# Sphere at origin

Shape {geometry Sphere{}}
'''
