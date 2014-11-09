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
from bpy.props import (EnumProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       StringProperty,
                       PointerProperty
                       )

enum_lamp_type = (
    ('POINT', "Point", "Omnidirectional point light source"),
    ('SUN',   "Sun",   "Constant direction parallel ray light source"),
    ('SPOT',  "Spot",  "Directional cone light source"),
    ('IES',   "IES",   "Directional cone light source from ies file"),
    ('AREA',  "Area",  "Directional area light source"),
    ('DIRECTIONAL', "Directional", "Directional Sun light"),
)

def call_lighttype_update(self, context):
    lamp = context.lamp
    bounty = context.lamp.bounty
    if lamp is not None:
        if bounty.lamp_type in {'IES','DIRECTIONAL'}:
            switchLampType = {'IES': 'SPOT','DIRECTIONAL': 'SUN'}
            lamp.type = switchLampType.get(bounty.lamp_type)
        else:
            lamp.type = bounty.lamp_type

def set_shadow_method(self, context):
    lamp = context.lamp
    if context.lamp.bounty.yaf_show_dist_clip:
        lamp.shadow_method = 'BUFFER_SHADOW'
    else:
        lamp.shadow_method = 'RAY_SHADOW'

def call_update_sphere(self, context):
    lamp = context.lamp
    if context.lamp.bounty.use_sphere:
        lamp.use_sphere = True
        lamp.distance = 1
    else:
        lamp.use_sphere = False

def sync_with_distance(self, context):
    #lamp = context.lamp
    if context.lamp.bounty.yaf_sphere_radius != context.lamp.distance:
        context.lamp.distance = context.lamp.bounty.yaf_sphere_radius
       
class TheBountyLightSettings(bpy.types.PropertyGroup):
    #
    @classmethod
    def register(cls):
        bpy.types.Lamp.bounty = PointerProperty(
            name="TheBounty Light Settings",
            description="TheBounty light settings",
            type=cls,
        )
        cls.nodetree = StringProperty(
            name="Node Tree",
            description="Name of the node tree for this light",
            default=""
        ) 
        cls.lamp_type = EnumProperty(
            name="Light type",
            description="Type of lamp",
            items=enum_lamp_type,
            default="POINT", 
            update=call_lighttype_update
        )    
        cls.yaf_energy = FloatProperty(
            name="Power",
            description="Intensity multiplier for color",
            min=0.0, max=10000.0,
            default=1.0
        )
        cls.use_sphere = BoolProperty(
            name="Use Sphere",
            description="Use sphere object for light",
            default=False,
            update = call_update_sphere
        )    
        cls.yaf_sphere_radius = FloatProperty(
            name="Radius",
            description="Radius of the sphere light",
            min=0.01, max=10000.0,
            soft_min=0.01, soft_max=100.0,
            default=1.0, update=sync_with_distance
        )    
        cls.directional = BoolProperty(
            name="Directional",
            description="Directional sunlight type, like 'spot' (for concentrate photons at area)",
            default=False
        )
        cls.create_geometry = BoolProperty(
            name="Create and show geometry",
            description="Creates a visible geometry in the dimensions of the light during the render",
            default=False
        )    
        cls.infinite = BoolProperty(
            name="Infinite",
            description="Determines if light is infinite or filling a semi-infinite cylinder",
            default=True
        )    
        cls.spot_soft_shadows = BoolProperty(
            name="Soft shadows (unused with photon only)",
            description="Use soft shadows(turn disabled with 'photon only')",
            default=False
        )    
        cls.shadow_fuzzyness = FloatProperty(
            name="Shadow fuzzyness",
            description="Fuzzyness of the soft shadows (0 - hard shadow, 1 - fuzzy shadow)",
            min=0.0, max=1.0,
            default=1.0
        )    
        cls.photon_only = BoolProperty(
            name="Photon only",
            description="This spot will only throw photons, not direct light",
            default=False
        )    
        cls.angle = FloatProperty(
            name="Angle",
            description="Angle of the cone in degrees (shadow softness)",
            min=0.0, max=80.0,
            default=0.5
        )    
        cls.ies_soft_shadows = BoolProperty(
            name="IES Soft shadows",
            description="Use soft shadows for IES light type",
            default=False
        )    
        cls.ies_file = StringProperty(
            name="IES File",
            description="File to be used as the light projection",
            subtype='FILE_PATH',
            default=""
        )    
        cls.yaf_samples = IntProperty(
            name="Samples",
            description="Number of samples to be taken for direct lighting",
            min=0, max=512,
            default=16
        )    
        cls.yaf_show_dist_clip = BoolProperty(
            name="Show clipping",
            description="Show clip start and clip end settings for spot lamp in 3D view",
            default=False, 
            update=set_shadow_method
        )
    #    
    @classmethod
    def unregister(cls):
        del bpy.types.Lamp.bounty
        
def register():
    bpy.utils.register_class(TheBountyLightSettings)
    
def unregister():
    bpy.utils.unregister_class(TheBountyLightSettings)