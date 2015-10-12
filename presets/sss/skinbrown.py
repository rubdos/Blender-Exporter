import bpy

#scene = bpy.context.scene
material = bpy.context.object.active_material
mat = material.bounty

mat.diffuse_color = (0.44, 0.23, 0.13)
mat.sssSigmaS = (0.37, 0.14, 0.06)
mat.sssSigmaA = (0.44, 0.23, 0.13)
mat.sssSpecularColor = (1.00, 1.00, 1.00)
# values
mat.glossy_reflect = 0.5
mat.sssSigmaS_factor = 1.0
mat.phaseFuction = 0.8
mat.sssIOR = 1.3
