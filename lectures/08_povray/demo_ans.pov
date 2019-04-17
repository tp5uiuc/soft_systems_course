#include "colors.inc"
#include "stones.inc"
#include "textures.inc"

camera {
	location <0, 2, -3>
	look_at <0, 1, 2>
}

sphere {
	// <center>, radius
	<0, 1, 2>, 2
	texture {
		pigment { color Yellow }
		// pigment { color red 1.0 green 0.8 blue 0.8 }
		// pigment { color rgb <1.0, 0.8, 0.8> }
		// pigment { rgb <1.0, 0.8, 0.8> }
	}
}

box {
	<-1, 0, -1>, // Near lower left corner
	< 1, 0.5, 3> // Far upper right corner
	texture {
		T_Stone25 // Pre-defined from stones.inc
		scale 4 // Scale by the same amount in all
		// directions
	}
	rotate y*20 // Equivalent to ’’rotate <0,20,0>’’
}

light_source { <2, 4, -3> color White}
