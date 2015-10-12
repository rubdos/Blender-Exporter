import bpy

#scene = bpy.context.scene
material = bpy.context.object.active_material
mat = material.bounty

mat.diffuse_color = (0.63, 0.44, 0.34)
mat.sssSigmaS = (0.48, 0.17, 0.10)
mat.sssSigmaA = (0.63, 0.44, 0.34)
mat.sssSpecularColor = (1.00, 1.00, 1.00)
mat.glossy_reflect = 0.5
mat.sssSigmaS_factor = 10
mat.phaseFuction = 0.8
mat.sssIOR = 1.3
#
scene = bpy.context.scene.bounty

if scene.intg_light_method == 'pathtracing':
	exp = 1
else:
	exp = 500
#
mat.exponent = exp


