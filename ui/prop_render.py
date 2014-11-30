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

import bpy, bl_ui
from bpy.types import Panel

class RenderButtonsPanel():
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    COMPAT_ENGINES = {'THEBOUNTY'}
    
    @classmethod
    def poll(cls, context):
        scene = context.scene
        return scene and (scene.render.engine in cls.COMPAT_ENGINES)


class TheBounty_PT_render(RenderButtonsPanel, Panel):
    bl_label = "Render"

    def draw(self, context):
        layout = self.layout

        rd = context.scene.render

        row = layout.row(align=True)
        row.operator("bounty.render_still", text="Render", icon='RENDER_STILL')
        row.operator("bounty.render_animation", text="Animation", icon='RENDER_ANIMATION')
        #row.operator("sound.mixdown", text="Audio", icon='PLAY_AUDIO')
        layout.operator("bounty.render_view", text="Render 3D View", icon='RENDER_STILL')

        split = layout.split(percentage=0.33)

        split.label(text="Display:")
        row = split.row(align=True)
        row.prop(rd, "display_mode", text="")
        row.prop(rd, "use_lock_interface", icon_only=True)


class BOUNTY_PT_dimensions(RenderButtonsPanel, Panel):
    bl_label = "Dimensions"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout

        scene = context.scene
        rd = scene.render

        row = layout.row(align=True)
        row.menu("RENDER_MT_presets", text=bpy.types.RENDER_MT_presets.bl_label)
        row.operator("render.preset_add", text="", icon='ZOOMIN')
        row.operator("render.preset_add", text="", icon='ZOOMOUT').remove_active = True

        split = layout.split()

        col = split.column()
        sub = col.column(align=True)
        sub.label(text="Resolution:")
        sub.prop(rd, "resolution_x", text="X")
        sub.prop(rd, "resolution_y", text="Y")
        sub.prop(rd, "resolution_percentage", text="")

        sub.label(text="Aspect Ratio:")
        sub.prop(rd, "pixel_aspect_x", text="X")
        sub.prop(rd, "pixel_aspect_y", text="Y")

        row = col.row()
        row.prop(rd, "use_border", text="Border")
        sub = row.row()
        sub.active = rd.use_border
        sub.prop(rd, "use_crop_to_border", text="Crop")

        col = split.column()
        sub = col.column(align=True)
        sub.label(text="Frame Range:")
        sub.prop(scene, "frame_start")
        sub.prop(scene, "frame_end")
        sub.prop(scene, "frame_step")

        #sub.label(text="Frame Rate:")
        #self.draw_framerate(sub, rd)

        subrow = sub.row(align=True)
        subrow.label(text="Time Remapping:")
        subrow = sub.row(align=True)
        subrow.prop(rd, "frame_map_old", text="Old")
        subrow.prop(rd, "frame_map_new", text="New")

#
from . import prop_general_settings
from . import prop_integrator
from . import prop_AA_settings

class TheBounty_PT_output(RenderButtonsPanel, Panel):
    bl_label = "Output"
    
    @classmethod
    def poll(cls, context):
        scene = context.scene
        engine = context.scene.render.engine
        #toimagefile = scene.bounty.gs_type_render == 'file'
        return engine in cls.COMPAT_ENGINES

    def draw(self, context):
        layout = self.layout

        rd = context.scene.render
        #sc = context.scene
        scene = context.scene.bounty
        image_settings = rd.image_settings

        layout.prop(rd, "filepath", text="")

        split = layout.split(percentage=0.6)
        col = split.column()
        col.prop(scene, "img_output", text="", icon='IMAGE_DATA')
        col = split.column()
        col.row().prop(image_settings, "color_mode", text="Color", expand=True)
        if scene.img_output == 'OPEN_EXR':
            row = layout.row()
            row.label("Color Depth")
            row.prop(image_settings, "color_depth", expand=True)
            layout.prop(image_settings, "exr_codec")
            row = layout.row()
            row.active = scene.gs_z_channel
            row.prop(image_settings, "use_zbuffer", text ='Save Z depth', toggle=True)


class TheBounty_PT_post_processing(RenderButtonsPanel, Panel):
    bl_label = "Post Processing"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        rd = context.scene.render

        split = layout.split()

        col = split.column()
        col.prop(rd, "use_compositing")
        col.prop(rd, "use_sequencer")

        col = split.column()
        col.prop(rd, "dither_intensity", text="Dither", slider=True)

'''
class YAF_PT_convert(RenderButtonsPanel, Panel):
    bl_label = "Convert old YafaRay Settings"

    def draw(self, context):
        layout = self.layout
        layout.column().operator("data.convert_yafaray_properties", text="Convert data from 2.4x")
'''

if __name__ == "__main__":  # only for live edit.
    #import bpy
    bpy.utils.register_module(__name__)
