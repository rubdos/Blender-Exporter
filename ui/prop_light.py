# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

from bpy.types import Panel

class DataButtonsPanel():
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    COMPAT_ENGINES = {'THEBOUNTY'}

    @classmethod
    def poll(cls, context):
        engine = context.scene.render.engine
        return context.lamp and (engine in cls.COMPAT_ENGINES)

# Inherit Lamp data block
from bl_ui.properties_data_lamp import DATA_PT_context_lamp
DATA_PT_context_lamp.COMPAT_ENGINES.add('THEBOUNTY')
del DATA_PT_context_lamp

class THEBOUNTY_PT_preview(Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    bl_label = "Preview"
    COMPAT_ENGINES = {'THEBOUNTY'}

    @classmethod
    def poll(cls, context):
        engine = context.scene.render.engine
        return context.lamp and (engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        self.layout.template_preview(context.lamp)


class THEBOUNTY_PT_lamp(DataButtonsPanel, Panel):
    bl_label = "Lamp"
    COMPAT_ENGINES = {'THEBOUNTY'}
    
    def draw_spot_shape(self, context):
        layout = self.layout
        lamp = context.lamp.bounty
        
        layout.label("Spot shape settings:")
        
        row = layout.row()
        row.prop(context.lamp, "spot_size", text="Size")
        row.prop(context.lamp, "spot_blend", text="Blend", slider=True)
        
        split = layout.split()
        col = split.column(align=True)
        col.prop(lamp, "yaf_show_dist_clip", toggle=True)
        if lamp.yaf_show_dist_clip:
            col.prop(context.lamp, "distance")
            col.prop(context.lamp, "shadow_buffer_clip_start", text="Clip Start")
            col.prop(context.lamp, "shadow_buffer_clip_end", text=" Clip End")

        col = split.column()
        col.prop(context.lamp, "show_cone", toggle=True)
    
    def draw_area_shape(self, context):
        layout = self.layout
        lamp = context.lamp
        
        layout.label("Area shape settings:")
        col = layout.column()
        col.row().prop(lamp, "shape", expand=True)
        sub = col.row(align=True)

        if lamp.shape == 'SQUARE':
            sub.prop(lamp, "size")
        elif lamp.shape == 'RECTANGLE':
            sub.prop(lamp, "size", text="Size X")
            sub.prop(lamp, "size_y", text="Size Y")
        col = layout.row()
        col.prop(lamp, "distance")
        
    def draw(self, context):
        layout = self.layout
        # use context.lamp for 'blender' Lamp properties
        # and context.lamp.bounty for a exporter Lamp properties
        lamp = context.lamp.bounty
        
        # commons values
        layout.prop(lamp, "lamp_type", expand=True)
        layout.prop(context.lamp, "color")
        layout.prop(lamp, "yaf_energy", text="Power")

        if lamp.lamp_type == "AREA":
            layout.prop(lamp, "yaf_samples")
            layout.prop(lamp, "create_geometry", toggle=True)
            #
            self.draw_area_shape(context)

        elif lamp.lamp_type == "SPOT":
            layout.prop(lamp, "photon_only", toggle=True)
            col = layout.column(align=True)
            if not lamp.photon_only:
                col.prop(lamp, "spot_soft_shadows", toggle=True)
                if lamp.spot_soft_shadows:
                    col.prop(lamp, "yaf_samples")
                    col.prop(lamp, "shadow_fuzzyness")
            #
            self.draw_spot_shape(context)            

        elif lamp.lamp_type == "SUN":
            layout.prop(lamp, "yaf_samples")
            layout.prop(lamp, "angle")

        elif lamp.lamp_type == "DIRECTIONAL":
            layout.prop(lamp, "infinite")
            if not lamp.infinite:
                layout.prop(context.lamp, "shadow_soft_size", text="Radius of directional cone")

        elif lamp.lamp_type == "POINT":
            col = layout.column(align=True)
            col.prop(lamp, "use_sphere", toggle=True)
            if lamp.use_sphere:
                col.prop(lamp, "yaf_sphere_radius")
                col.prop(lamp, "yaf_samples")
                col.prop(lamp, "create_geometry", toggle=True)

        elif lamp.lamp_type == "IES":
            layout.prop(lamp, "ies_file")
            col = layout.column(align=True)            
            col.prop(lamp, "ies_soft_shadows", toggle=True)
            if lamp.ies_soft_shadows:
                col.prop(lamp, "yaf_samples")


if __name__ == "__main__":  # only for live edit.
    import bpy
    bpy.utils.register_module(__name__)
