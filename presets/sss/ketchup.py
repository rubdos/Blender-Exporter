import bpy

material = bpy.context.object.active_material
mat = material.bounty
# colors
mat.diffuse_color = (0.16, 0.01, 0.00)
mat.sssSigmaS = (0.47, 0.06, 0.04)
mat.sssSigmaA = (0.16, 0.01, 0.00)
mat.sssSpecularColor = (1.00, 1.00, 1.00)
# values
mat.sssIOR = 1.3
mat.phaseFuction = 0.9
mat.sssSigmaS_factor = 10
mat.glossy_reflect = 0.7
#
#scene = bpy.context.scene (yafaray)
scene = bpy.context.scene.bounty

if scene.intg_light_method == 'pathtracing':
	exp = 1
else:
	exp = 500
#
mat.exponent = exp
