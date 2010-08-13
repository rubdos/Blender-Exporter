import bpy


FloatProperty = bpy.types.Lamp.FloatProperty
IntProperty = bpy.types.Lamp.IntProperty
BoolProperty = bpy.types.Lamp.BoolProperty
CollectionProperty = bpy.types.Lamp.CollectionProperty
EnumProperty = bpy.types.Lamp.EnumProperty
FloatVectorProperty = bpy.types.Lamp.FloatVectorProperty
StringProperty = bpy.types.Lamp.StringProperty
IntVectorProperty = bpy.types.Lamp.IntVectorProperty


EnumProperty(attr="lamp_type",
	items = (
		("Light Type","Light Type",""),
		("Area","Area",""),
		("Directional","Directional",""),
		#("MeshLight","MeshLight",""),
		("Point","Point",""),
		("Sphere","Sphere",""),
		("Spot","Spot",""),
		("Sun","Sun",""),
		("IES","IES",""),
),default="Sun")
BoolProperty(attr="create_geometry")
BoolProperty(attr="infinite")
BoolProperty(attr="spot_soft_shadows")
FloatProperty(attr="shadow_fuzzyness")
BoolProperty(attr="photon_only")
IntProperty(attr="angle",
		max = 80,
		min = 0)
StringProperty(attr="ies_file",subtype = 'FILE_PATH')
IntProperty(attr="ies_samples", default = 1000)
FloatProperty(attr="ies_cone_angle", default = 10.0)
BoolProperty(attr="ies_soft_shadows")


class YAF_PT_lamp(bpy.types.Panel):

	bl_label = 'Lamp'
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'data'
	COMPAT_ENGINES =['YAFA_RENDER']


	def poll(self, context):

		engine = context.scene.render.engine

		import properties_data_lamp

		if (context.lamp and  (engine in self.COMPAT_ENGINES) ) :
			try :
				properties_data_lamp.unregister()
			except: 
				pass
		else:
			try:
				properties_data_lamp.register()
			except: 
				pass
		return (context.lamp and  (engine in self.COMPAT_ENGINES) ) 


	def draw(self, context):

		layout = self.layout
		split = layout.split()
		col = split.column()

		col.prop(context.lamp,"lamp_type", text= "Light Type")
		row = layout.row()
		split = row.split()
		col = row.column()

		if context.lamp.lamp_type == 'Area':
			
			col.prop(context.lamp,"shadow_ray_samples_x", text= "Samples")
			if context.lamp.type != 'AREA':
				context.lamp.type = 'AREA'
			col.prop(context.lamp,"size", text= "SizeX")
			col.prop(context.lamp,"size_y", text= "SizeY")
			col.prop(context.lamp,"create_geometry", text= "Create Geometry")


		elif context.lamp.lamp_type == 'Directional':
			if context.lamp.type != 'SUN':
				context.lamp.type = 'SUN'
			col.prop(context.lamp,"shadow_soft_size", text= "Radius")
			col.prop(context.lamp,"infinite", text= "Infinite")

		elif context.lamp.lamp_type == 'Sphere':
			if context.lamp.type != 'POINT':
				context.lamp.type = 'POINT'
			col.prop(context.lamp,"shadow_soft_size", text= "Radius")
			col.prop(context.lamp,"shadow_ray_samples", text= "Samples")
			col.prop(context.lamp,"create_geometry", text= "Create Geometry")


		elif context.lamp.lamp_type == 'Spot':
			
			if context.lamp.type != 'SPOT':
				context.lamp.type = 'SPOT'
			
			col.prop(context.lamp,"spot_size", text= "Cone Angle")
			col.prop(context.lamp,"shadow_ray_samples", text= "Samples")
			col.prop(context.lamp,"spot_blend", text= "Blend")
			col.prop(context.lamp,"distance", text= "Distance")

			col.prop(context.lamp,"shadow_fuzzyness", text= "Shadow Fuzzyness")
			col = split.column()
			col.prop(context.lamp,"photon_only", text= "Photon Only")
			col.prop(context.lamp,"spot_soft_shadows", text= "Soft Shadow")
			
		elif context.lamp.lamp_type == 'Sun':
			
			if context.lamp.type != 'SUN':
				context.lamp.type = 'SUN'
			col.prop(context.lamp,"angle", text= "Angle")
			col.prop(context.lamp,"shadow_ray_samples", text= "Samples")
		
		elif context.lamp.lamp_type == 'Point':
			
			if context.lamp.type != 'POINT':
				context.lamp.type = 'POINT'
			
		
		elif context.lamp.lamp_type == 'IES':
			col.prop(context.lamp,"ies_file",text = "IES File")
			if context.lamp.ies_soft_shadows:
				col.prop(context.lamp,"ies_samples",text = "IES Samples")
			col.prop(context.lamp,"ies_cone_angle",text = "IES Cone Angle")
			col.prop(context.lamp,"ies_soft_shadows",text = "IES Soft Shadows")




		col.prop(context.lamp,"color", text= "Color")
		col.prop(context.lamp,"energy", text= "Power")


from properties_data_lamp import DATA_PT_preview
from properties_data_lamp import DATA_PT_context_lamp

classes = [
	YAF_PT_lamp,
]

def register():
	YAF_PT_lamp.prepend( DATA_PT_preview.draw )
	YAF_PT_lamp.prepend( DATA_PT_context_lamp.draw )
	register = bpy.types.register
	for cls in classes:
		register(cls)


def unregister():
	bpy.types.YAF_PT_lamp.remove( DATA_PT_preview.draw )
	bpy.types.YAF_PT_lamp.remove( DATA_PT_context_lamp.draw )
	unregister = bpy.types.unregister
	for cls in classes:
		unregister(cls)


if __name__ == "__main__":
	register()
