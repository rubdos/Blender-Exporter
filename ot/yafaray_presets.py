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


# review for fix error with path
#from bl_operators.presets import AddPresetBase
#from bpy.types import Operator

import os
from bpy.props import StringProperty, EnumProperty, BoolProperty
from bpy.types import Menu, Operator
import bpy

def updatePresetsPath(target):
    """ Use install folder for presets """
    ver1 = str(bpy.app.version[0])
    ver2 = str(bpy.app.version[1])
    version = ver1 +'.'+ ver2
    target_path = os.path.join(os.getcwd(),version,"scripts", target)
    #fix missings paths, you only needs create an new presets    
    if not os.path.exists(target_path):
        os.mkdir(target_path)
    #
    return target_path

class TheBountyPresetBase():
    """Base preset class, only for subclassing
    subclasses must define
     - preset_values
     - preset_subdir """
    # bl_idname = "script.preset_base_add"
    # bl_label = "Add a Python Preset"

    # only because invoke_props_popup requires. Also do not add to search menu.
    bl_options = {'REGISTER', 'INTERNAL'}

    name = StringProperty(
            name="Name",
            description="Name of the preset, used to make the path name",
            maxlen=64,
            options={'SKIP_SAVE'},
            )
    remove_active = BoolProperty(
            default=False,
            options={'HIDDEN', 'SKIP_SAVE'},
            )

    @staticmethod
    def as_filename(name):  # could reuse for other presets
        for char in " !@#$%^&*(){}:\";'[]<>,.\\/?":
            name = name.replace(char, '_')
        return name.lower().strip()

    def execute(self, context):
        #import os

        if hasattr(self, "pre_cb"):
            self.pre_cb(context)

        preset_menu_class = getattr(bpy.types, self.preset_menu)

        is_xml = getattr(preset_menu_class, "preset_type", None) == 'XML'

        if is_xml:
            ext = ".xml"
        else:
            ext = ".py"

        if not self.remove_active:
            name = self.name.strip()
            if not name:
                return {'FINISHED'}

            filename = self.as_filename(name)
            #target_path = os.path.join("presets", self.preset_subdir)            
            preset_subdir = os.path.join("presets", self.preset_subdir)            
            target_path = updatePresetsPath(preset_subdir)
            if not os.path.exists(target_path):
                os.mkdir(target_path)
            #target_path = bpy.utils.user_resource('SCRIPTS', target_path, create=True)
            
            if not target_path:
                self.report({'WARNING'}, "Failed to create presets path")
                return {'CANCELLED'}

            filepath = os.path.join(target_path, filename) + ext

            if hasattr(self, "add"):
                self.add(context, filepath)
            else:
                print("Writing Preset: %r" % filepath)

                if is_xml:
                    import rna_xml
                    rna_xml.xml_file_write(context,
                                           filepath,
                                           preset_menu_class.preset_xml_map)
                else:

                    def rna_recursive_attr_expand(value, rna_path_step, level):
                        if isinstance(value, bpy.types.PropertyGroup):
                            for sub_value_attr in value.bl_rna.properties.keys():
                                if sub_value_attr == "rna_type":
                                    continue
                                sub_value = getattr(value, sub_value_attr)
                                rna_recursive_attr_expand(sub_value, "%s.%s" % (rna_path_step, sub_value_attr), level)
                        elif type(value).__name__ == "bpy_prop_collection_idprop":  # could use nicer method
                            file_preset.write("%s.clear()\n" % rna_path_step)
                            for sub_value in value:
                                file_preset.write("item_sub_%d = %s.add()\n" % (level, rna_path_step))
                                rna_recursive_attr_expand(sub_value, "item_sub_%d" % level, level + 1)
                        else:
                            # convert thin wrapped sequences
                            # to simple lists to repr()
                            try:
                                value = value[:]
                            except:
                                pass

                            file_preset.write("%s = %r\n" % (rna_path_step, value))

                    file_preset = open(filepath, 'w')
                    file_preset.write("import bpy\n")

                    if hasattr(self, "preset_defines"):
                        for rna_path in self.preset_defines:
                            exec(rna_path)
                            file_preset.write("%s\n" % rna_path)
                        file_preset.write("\n")

                    for rna_path in self.preset_values:
                        value = eval(rna_path)
                        rna_recursive_attr_expand(value, rna_path, 1)

                    file_preset.close()

            preset_menu_class.bl_label = bpy.path.display_name(filename)

        else:
            preset_active = preset_menu_class.bl_label

            # fairly sloppy but convenient.
            filepath = bpy.utils.preset_find(preset_active,
                                             self.preset_subdir,
                                             ext=ext)

            if not filepath:
                filepath = bpy.utils.preset_find(preset_active,
                                                 self.preset_subdir,
                                                 display_name=True,
                                                 ext=ext)

            if not filepath:
                return {'CANCELLED'}

            if hasattr(self, "remove"):
                self.remove(context, filepath)
            else:
                try:
                    os.remove(filepath)
                except:
                    import traceback
                    traceback.print_exc()

            # XXX, stupid!
            preset_menu_class.bl_label = "Presets"

        if hasattr(self, "post_cb"):
            self.post_cb(context)

        return {'FINISHED'}

    def check(self, context):
        self.name = self.as_filename(self.name.strip())

    def invoke(self, context, event):
        if not self.remove_active:
            wm = context.window_manager
            return wm.invoke_props_dialog(self)
        else:
            return self.execute(context)


class TheBountyOperatorSettingsPresets(TheBountyPresetBase, bpy.types.Operator):
    # Add render presets
    bl_idname = "bounty.render_preset_add"
    bl_label = "TheBounty Settings Presets"
    preset_menu = "THEBOUNTY_MT_render_presets"
    
    preset_defines = [
        "scene = bpy.context.scene.bounty",
        "render = bpy.context.scene.render"
    ]
    preset_values = [
        "render.resolution_x",
        "render.resolution_y",
        "scene.gs_ray_depth",
        "scene.gs_shadow_depth",
        "scene.gs_threads",
        "scene.gs_gamma",
        "scene.gs_gamma_input",
        "scene.gs_tile_size",
        "scene.gs_tile_order",
        "scene.gs_auto_threads",
        "scene.gs_clay_render",
        "scene.gs_draw_params",
        "scene.gs_custom_string",
        "scene.gs_premult",
        "scene.gs_transp_shad",
        "scene.gs_clamp_rgb",
        "scene.gs_show_sam_pix",
        "scene.gs_z_channel",
        "scene.gs_type_render",
        "scene.intg_light_method",
        "scene.intg_use_caustics",
        "scene.intg_photons",
        "scene.intg_caustic_mix",
        "scene.intg_caustic_depth",
        "scene.intg_caustic_radius",
        "scene.intg_use_AO",
        "scene.intg_AO_samples",
        "scene.intg_AO_distance",
        "scene.intg_AO_color",
        "scene.intg_bounces",
        "scene.intg_diffuse_radius",
        "scene.intg_cPhotons",
        "scene.intg_search",
        "scene.intg_final_gather",
        "scene.intg_fg_bounces",
        "scene.intg_fg_samples",
        "scene.intg_show_map",
        "scene.intg_caustic_method",
        "scene.intg_path_samples",
        "scene.intg_no_recursion",
        "scene.intg_debug_type",
        "scene.intg_show_perturbed_normals",
        "scene.intg_pm_ire",
        "scene.intg_pass_num",
        "scene.intg_times",
        "scene.intg_photon_radius",
        "scene.AA_min_samples",
        "scene.AA_inc_samples",
        "scene.AA_passes",
        "scene.AA_threshold",
        "scene.AA_pixelwidth",
        "scene.AA_filter_type"
    ]

    preset_subdir = "thebounty/render"

    
class TheBountyOperatorMaterialPresets(TheBountyPresetBase, bpy.types.Operator):
    # Add material presets
    bl_idname = "bounty.material_preset_add"
    bl_label = "Material Presets"
    preset_menu = "TheBountyMaterialPresets"
    
    preset_defines = [
        "material = bpy.context.object.active_material",
        "mat = material.bounty"
    ]    
    preset_values = [    
        "mat.absorption",
        "material.diffuse_color",
        "mat.absorption_dist",
        "mat.anisotropic",
        "mat.as_diffuse",
        "mat.brdf_type",
        "mat.coat_mir_col",
        "mat.coated",
        "mat.diffuse_reflect",
        "mat.dispersion_power",
        "mat.exp_u",
        "mat.exp_v",
        "mat.exponent",
        "mat.fake_shadows",
        "mat.filter_color",
        "mat.fresnel_effect",
        "mat.glass_mir_col",
        "mat.glass_transmit",
        "mat.glossy_color",
        "mat.glossy_reflect",
        "mat.IOR_reflection",
        "mat.IOR_refraction",
        "mat.mat_type",
        # "mat.material1", # blend material not work
        # "mat.material2",
        # "mat.blend_value",
        "mat.refr_roughness",
        "mat.rough",
        "mat.sigma",
        "mat.specular_reflect",
        "mat.transmit_filter",
        "mat.transparency",
        # sss
        "mat.phaseFuction",
        "mat.sss_transmit",
        "mat.sssColor",
        "mat.sssIOR",
        "mat.sssSigmaA",
        "mat.sssSigmaS",
        "mat.sssSigmaS_factor",
        "mat.sssSpecularColor"
    ]
    preset_subdir = "thebounty/material"    
                
    
def register():
    #pass
    bpy.utils.register_class(TheBountyOperatorSettingsPresets)
    bpy.utils.register_class(TheBountyOperatorMaterialPresets)
    
def unregister():
    #pass
    bpy.utils.unregister_class(TheBountyOperatorSettingsPresets)
    bpy.utils.unregister_class(TheBountyOperatorMaterialPresets)
    
if __name__ == "__main__":
    register()
