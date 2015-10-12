import bpy

material = bpy.context.object.active_material
mat = material.bounty
# colors
mat.diffuse_color = (0.81, 0.81, 0.68)
mat.sssSigmaS = (0.92, 0.52, 0.18)
mat.sssSigmaA = (0.81, 0.81, 0.68)
mat.sssSpecularColor = (1.00, 1.00, 1.00)
# values
mat.sssIOR = 1.3
mat.phaseFuction = 0.8
mat.sssSigmaS_factor = 1.0
mat.glossy_reflect = 0.8
#
#scene = bpy.context.scene (yafaray)
scene = bpy.context.scene.bounty

if scene.intg_light_method == 'pathtracing':
	exp = 1
else:
	exp = 500
#
mat.exponent = exp
