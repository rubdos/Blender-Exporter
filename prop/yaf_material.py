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

import bpy
from bpy.props import (FloatProperty,
                       BoolProperty,
                       EnumProperty,
                       FloatVectorProperty,
                       PointerProperty,
                       StringProperty)

enum_material_types = (
    ('shinydiffusemat', "Shiny Diffuse",    ""),
    ('glossy',          "Glossy",           ""),
    ('coated_glossy',   "Coated Glossy",    ""),
    ('glass',           "Glass",            ""),
    ('rough_glass',     "Rough Glass",      ""),
    ('blend',           "Blend",            ""),
    ('translucent',     "Translucent(SSS)", ""),
)

enum_reflectance_mode = (
    ('oren-nayar', "Oren-Nayar", "Reflectance Model"),
    ('lambert', "Lambert", "Reflectance Model"),
)

Material = bpy.types.Material
#-----------------------------------------
# syncronize some colors with Blender
# for better visualization on viewport
#-----------------------------------------
def syncBlenderColors(self, context):
    context.material.diffuse_color = context.material.bounty.diff_color
    

def items_mat1(self, context):
    a = []
    for mat in [m for m in bpy.data.materials if m.name not in self.name]:
        if mat.bounty.mat_type not in 'blend':
        a.append((mat.name, mat.name, "First blend material"))
    return(a)

def items_mat2(self, context):
    a = []
    for mat in [m for m in bpy.data.materials if m.name not in self.name]:
        if mat.bounty.mat_type not in 'blend':
        a.append((mat.name, mat.name, "Second blend material"))
    return(a)

class TheBountyMaterialProperties(bpy.types.PropertyGroup):
    
    @classmethod
    def register(cls):
        # 
        # add subclasse to Material class
        bpy.types.Material.bounty = PointerProperty(
            name="TheBounty Material properties",
            description="",
            type=cls,
        )
        #---------------------------
        # list of material properies
        #---------------------------
        cls.nodetree = StringProperty(
            name="Node Tree",
            description="Name of the shader node tree for this material",
            default=""
        )
        cls.mat_type = EnumProperty(
                name="Material type",
                items=enum_material_types,
                default='shinydiffusemat'
        )
        cls.diff_color = FloatVectorProperty(
            name="Diffuse color",
            description="Diffuse albedo color material",
            subtype='COLOR',
            min=0.0, max=1.0,
            default=(0.8, 0.8, 0.8),
            update = syncBlenderColors
        )
        cls.emittance = FloatProperty(
            name="Emit",
            description="Amount of emissive property",
            min=0.0, max=1.0,
            step=1, precision=3,
            soft_min=0.0, soft_max=1.0,
            default=0.00
        )    
        cls.diffuse_reflect = FloatProperty(
                name="Reflection strength",
                description="Amount of diffuse reflection",
                min=0.0, max=1.0,
                step=1, precision=3,
                soft_min=0.0, soft_max=1.0,
                default=1.000
        )    
        cls.specular_reflect = FloatProperty(
                name="Reflection strength",
                description="Amount of perfect specular reflection (mirror)",
                min=0.0, max=1.0,
                step=1, precision=3,
                soft_min=0.0, soft_max=1.0,
                default=0.000
        )    
        cls.transparency = FloatProperty(
                name="Transparency",
                description="Material transparency",
                min=0.0, max=1.0,
                step=1, precision=3,
                soft_min=0.0, soft_max=1.0,
                default=0.000
        )    
        cls.transmit_filter = FloatProperty(
                name="Transmit filter",
                description="Amount of tinting of light passing through the Material",
                min=0.0, max=1.0,
                step=1, precision=3,
                soft_min=0.0, soft_max=1.0,
                default=1.000
        )    
        cls.fresnel_effect = BoolProperty(
                name="Fresnel effect",
                description="Apply a fresnel effect to specular reflection",
                default=False
        )    
        cls.brdf_type = EnumProperty(
                name="Reflectance model",
                items= enum_reflectance_mode,
                default='lambert'
        )    
                items= enum_reflectance_mode,
                default='lambert'
        )
        cls.mirr_color = FloatVectorProperty(
                name="Mirror color",
                description="Mirror Color",
                subtype='COLOR',
                min=0.0, max=1.0,
                default=(1.0, 1.0, 1.0)
        )   
        cls.glossy_color = FloatVectorProperty(
                name="Glossy color",
                description="Glossy Color",
                subtype='COLOR',
                min=0.0, max=1.0,
                default=(1.0, 1.0, 1.0)
        )
        cls.coat_mir_col = FloatVectorProperty(
                name="Mirror color",
                description="Reflection color of coated layer",
                subtype='COLOR',
                min=0.0, max=1.0,
                default=(1.0, 1.0, 1.0)
        )
        cls.glass_mir_col = FloatVectorProperty(
                name="Reflection color",
                description="Reflection color of glass material",
                subtype='COLOR',
                min=0.0, max=1.0,
                default=(1.0, 1.0, 1.0)
        )
        cls.glossy_reflect = FloatProperty(
                name="Reflection strength",
                description="Amount of glossy reflection",
                min=0.0, max=1.0,
                step=1, precision=3,
                soft_min=0.0, soft_max=1.0,
                default=0.000
        )    
        cls.exp_u = FloatProperty(
                name="Exponent U",
                description="Horizontal anisotropic exponent value",
                min=1.0, max=10000.0,
                step=10, precision=2,
                soft_min=1.0, soft_max=10000.0,
                default=50.00
        )    
        cls.exp_v = FloatProperty(
                name="Exponent V",
                description="Vertical anisotropic exponent value",
                min=1.0, max=10000.0,
                step=10, precision=2,
                soft_min=1.0, soft_max=10000.0,
                default=50.00
        )    
        cls.exponent = FloatProperty(
                name="Exponent",
                description="Blur of the glossy reflection, higher exponent = sharper reflections",
                min=1.0, max=10000.0,
                step=10, precision=2,
                soft_min=1.0, soft_max=10000.0,
                default=500.00
        )    
        cls.as_diffuse = BoolProperty(
                name="Use photon map",
                description="Treat glossy component as diffuse",
                default=False
        )    
        cls.anisotropic = BoolProperty(
                name="Anisotropic",
                description="Use anisotropic reflections",
                default=False
        )    
        cls.IOR_refraction = FloatProperty(
                name="IOR",
                description="Index of refraction",
                min=0.0, max=30.0,
                step=1, precision=3,
                soft_min=0.0, soft_max=30.0,
                default=1.520
        )    
        cls.IOR_reflection = FloatProperty(
                name="IOR",
                description="Fresnel reflection strength",
                min=1.0, max=30.0,
                step=1, precision=3,
                soft_min=1.0, soft_max=30.0,
                default=1.800
        )    
        cls.absorption = FloatVectorProperty(
                name="Color and absorption",
                description="Glass volumetric absorption color. White disables absorption",
                subtype='COLOR',
                min=0.0, max=1.0,
                default=(1.0, 1.0, 1.0)
        )    
        cls.absorption_dist = FloatProperty(
                name="Abs. distance",
                description="Absorption distance scale",
                min=0.0, max=100.0,
                step=1, precision=4,
                soft_min=0.0, soft_max=100.0,
                default=1.0000
        )    
        cls.glass_transmit = FloatProperty(
                name="Transmit filter",
                description="Filter strength applied to refracted light",
                min=0.0, max=1.0,
                step=1, precision=3,
                soft_min=0.0, soft_max=1.0,
                default=1.000
        )    
        cls.filter_color = FloatVectorProperty(
                name="Filter color",
                description="Filter color for refracted light of glass, also tint transparent shadows if enabled",
                subtype='COLOR',
                min=0.0, max=1.0,
                default=(1.0, 1.0, 1.0)
        )    
        cls.dispersion_power = FloatProperty(
                name="Disp. power",
                description="Strength of dispersion effect, disabled when 0",
                min=0.0, max=5.0,
                step=1, precision=4,
                soft_min=0.0, soft_max=5.0,
                default=0.0000
        )    
        cls.refr_roughness = FloatProperty(
                name="Exponent",
                description="Refraction factor on rough glass material",
                min=0.0, max=1.0,
                step=1, precision=3,
                soft_min=0.0, soft_max=1.0,
                default=0.200
        )    
        cls.fake_shadows = BoolProperty(
                name="Fake shadows",
                description="Let light straight through for shadow calculation. Not to be used with dispersion",
                default=False
        )    
        cls.blend_value = FloatProperty(
                name="Blend value",
                description="The mixing balance: 0 -> only material 1, 1.0 -> only material 2",
                min=0.0, max=1.0,
                step=3, precision=3,
                soft_min=0.0, soft_max=1.0,
                default=0.500
        )    
        cls.sigma = FloatProperty(
                name="Sigma",
                description="Roughness of the surface",
                min=0.0, max=1.0,
                step=1, precision=5,
                soft_min=0.0, soft_max=1.0,
                default=0.10000
        )    
        cls.blendmaterial1 = EnumProperty(
                name="Material one",
                description="First blend material",
                items=items_mat1)
    
        cls.blendmaterial2 = EnumProperty(
                name="Material two",
                description="Second blend material",
                items=items_mat2
        )        
        #--------------------------------------------
        #  Translucent SubSurface Scattering settings
        #--------------------------------------------
        cls.sssColor = FloatVectorProperty(
                name="Diffuse color",
                description="Diffuse color",
                subtype='COLOR',
                min=0.0, max=1.0,
                default=(1.0, 1.0, 1.0)
        )            
        cls.sssSpecularColor = FloatVectorProperty(
                name="Specular Color",
                description="Specular Color",
                subtype='COLOR',
                min=0.0, max=1.0,
                default=(1.0, 1.0, 1.0)
        )    
        cls.sssSigmaA = FloatVectorProperty(
                name="Absorption Color",
                description="Absorption Color",
                subtype='COLOR',
                min=0.0, max=1.0,
                default=(0.0, 0.0, 0.0)
        )    
        cls.sssSigmaS = FloatVectorProperty(
                name="Scatter color",
                description="Scatter color",
                subtype='COLOR',
                min=0.0, max=1.0,
                default=(0.7, 0.7, 0.7)
        )        
        cls.sssSigmaS_factor = FloatProperty(
                name="SigmaS factor",
                description="Sigma factor for SSS",
                min=0.1, max=100.0,
                step=0.01, precision=3,
                default=1.0
        )    
        cls.sss_transmit = FloatProperty(
                name="Transmittance",
                description="Transmittance",
                min=0.0, max=1.0,
                step=0.01, precision=3,
                default=1.0
        )        
        cls.sssIOR = FloatProperty(
                name="IOR",
                description="Index of refraction for SSS",
                min=0.0, max=3.0,
                step=1, precision=3,
                soft_min=1.0, soft_max=30.0,
                default=1.300
        )
        cls.phaseFuction = FloatProperty(
                name="Phase Function",
                description="Difference between diffuse reflection (+ values) and glossy reflection (- values)",
                min=-0.99, max=0.99,
                step=0.01, precision=2,
                default=0.0)
    #
    @classmethod
    def unregister(cls):
        del bpy.types.Material.bounty

def register():
    bpy.utils.register_class(TheBountyMaterialProperties)
    
def unregister():
    bpy.utils.unregister_class(TheBountyMaterialProperties)
