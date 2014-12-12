import bpy
# 			sigma_S, 			sigmaA				diff reflect color
# "Cream", { 7.38, 5.47, 3.15 }, { 0.0002, 0.0028, 0.0163 }, },
# Cream  7.38 5.47 3.15    0.0002 0.0028 0.0163 	 0.98 0.90 0.73
material = bpy.context.object.active_material
mat = material.bounty
# colors
mat.diffuse_color = (0.87, 0.78, 0.46)
mat.sssSigmaS = (.738, .547, .315)
mat.sssSigmaA = (0.0002, 0.0028, 0.0163) #0.87, 0.78, 0.46)
mat.sssSpecularColor = (1.00, 1.00, 1.00)

# values
mat.sssIOR = 1.3
mat.phaseFuction = 0.8
mat.sssSigmaS_factor = 10
mat.glossy_reflect = 0.6

#scene = bpy.context.scene (yafaray)
scene = bpy.context.scene.bounty
if scene.intg_light_method == 'pathtracing':
	exp = 1
else:
	exp = 500
#
mat.exponent = exp
