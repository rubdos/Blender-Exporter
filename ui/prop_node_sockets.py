#---------- BEGIN GPL LICENSE BLOCK ------------------------------------------#
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
#  or visit https://www.fsf.org for more info.
#
#---------- END GPL LICENSE BLOCK --------------------------------------------#

# <pep8 compliant>

#-------------------------------------------------
# This file is part of TheBounty Blender exporter
# Created by povmaniac at 20/01/15
#-------------------------------------------------
import bpy
from bpy.types import Node, NodeSocket
from bpy.props import (FloatProperty, 
                       FloatVectorProperty, 
                       StringProperty, 
                       BoolProperty,
                       EnumProperty)

from ..prop.yaf_material import TheBountyMaterialProperties as MatProperty

color_socket = (0.9, 0.9, 0.0, 1.0)
float_socket = (0.63, 0.63, 0.63, 1.0)
enum_sockect = (0.0, 0.0, 1.0, 1.0)
#
bounty_socket_class=[]
#
class diffuse_color_socket(NodeSocket):
    #-----------------------
    # Diffuse color sockets 
    #-----------------------
    bl_idname = 'diffuse_color'
    bl_label = 'Color Socket'    
    
    diff_color = MatProperty.diff_color
    diffuse_reflect = MatProperty.diffuse_reflect
    emittance = MatProperty.emittance
    
    # useful helper functions
    def default_value_get(self):
        return self.diff_color
    
    def default_value_set(self, value):
        self.diff_color = value
        
    default_value =  bpy.props.FloatVectorProperty( subtype='COLOR', get=default_value_get, set=default_value_set)
    
    #         
    def draw(self, context, layout, node, text):
        col = layout.column()
        label = 'Diffuse Color'
        if self.is_linked and not self.is_output:
            label = 'Diffuse Layer'
        #                     
        col.prop(self, "diff_color", text= label )
        col.prop(self, "diffuse_reflect", text="Diffuse Reflection")
        col.prop(self, "emittance", slider=True)
    #
    def draw_color(self, context, node):
        return (color_socket)

#
bounty_socket_class.append(diffuse_color_socket)

class diffuse_reflect_socket(NodeSocket):
    bl_idname = 'diffuse_reflection'
    bl_label = 'Reflection Socket'
    
    diffuse_reflect = MatProperty.diffuse_reflect
    
    # helper property
    def default_value_get(self):
        return self.diffuse_reflect
    
    def default_value_set(self, value):
        self.diffuse_reflect  = value
        
    default_value =  bpy.props.FloatProperty( get=default_value_get, set=default_value_set)
    #    
    def draw(self, context, layout, node, text):
        if self.is_linked and not self.is_output:
            layout.label('Diffuse reflection')
        else:
            layout.prop(self, "diffuse_reflect", slider=True)    
    #
    def draw_color(self, context, node):
        return (float_socket)
#
bounty_socket_class.append(diffuse_reflect_socket)

#-------------------------------------------
# Emission socket for shinydiffuse material
#-------------------------------------------
class emitt_socket(NodeSocket):
    bl_idname = 'emittance'
    bl_label = 'Emission Socket'  
    
    emittance = MatProperty.emittance
    
    # get/set default values
    def default_value_get(self):
        return self.emittance
    
    def default_value_set(self, value):
        self.emittance = value
    #
    default_value =  bpy.props.FloatProperty( get=default_value_get, set=default_value_set)
    #    
    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text)
        else:
            layout.prop(self, "emittance", slider=True)    
    #
    def draw_color(self, context, node):
        return (float_socket)
#
bounty_socket_class.append(emitt_socket)

#-----------------------
# BRDF socket
#-----------------------
class brdf_socket(NodeSocket):
    bl_idname = 'brdf'
    bl_label = 'BRDF Socket'    
    
    #brdf_type = MatProperty.brdf_type
    sigma = MatProperty.sigma
    
    enum_reflectance_mode = [
        ('lambert', "Lambert", "Reflectance Model",0),
        ('oren-nayar', "Oren-Nayar", "Reflectance Model",1),
        
    ]
    # small trick..
    enum_reflectance_default_mode = (('lambert', "Lambert", "Reflectance Model"),)
        
    # default values for a socket
    def default_value_get(self):
        return self.brdf_type
    
    def default_value_set(self, value):
        self.brdf_type = 'lambert'
        
    brdf_type = EnumProperty(
            name="BRDF",
            description="Reflectance model",
            items=enum_reflectance_mode,
            default='lambert',
    )        
    default_value =  EnumProperty(items=enum_reflectance_mode, set=default_value_set)
    #
    def draw(self, context, layout, node, text):
        col = layout.column()
        if self.is_linked:
            col.label("Reflectance model")
        else:
            col.prop(self, "brdf_type")
            col.prop(self, "sigma", text='Sigma', slider=True)
    #
    def draw_color(self, context, node):
        return (float_socket)
#
bounty_socket_class.append(brdf_socket)

class sigma_socket(NodeSocket):
    bl_idname = 'sigma'
    bl_label = 'Sigma Socket'
    hide_value = True 
    
    sigma = MatProperty.sigma
    
    # default values for socket
    def default_value_get(self):
        return self.sigma
    
    def default_value_set(self, value):
        self.sigma = value
        
    default_value =  FloatProperty( get=default_value_get, set=default_value_set)
    #
    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text)
        else:
            layout.prop(self, "sigma", slider=True)    
    #
    def draw_color(self, context, node):
        return (float_socket)
#
bounty_socket_class.append(sigma_socket)

#---------------
# translucency
#--------------
class translucency_socket(NodeSocket):
    bl_idname = 'translucency'
    bl_label = 'Translucency Socket'  
    
    translucency = MatProperty.translucency
    transmit = MatProperty.transmit_filter
    
    # default values for socket
    def default_value_get(self):
        return self.translucency
    
    def default_value_set(self, value):
        self.translucency = value
        
    default_value =  bpy.props.FloatProperty( get=default_value_get, set=default_value_set)
    #    
    def draw(self, context, layout, node, text):
        col = layout.column()
        if self.is_linked:
            col.label('Translucency Layer')
        else:
            col.prop(self, "translucency", slider=True)
        col.prop(self, "transmit", slider=True)    
    # 
    def draw_color(self, context, node):
        return (float_socket)
#
bounty_socket_class.append(translucency_socket)
    
class transparency_socket(NodeSocket):
    bl_idname = 'transparency'
    bl_label = 'Transparency Socket'  
    
    transparency = MatProperty.transparency
    
    # default values for socket
    def default_value_get(self):
        return self.transparency
    
    def default_value_set(self, value):
        self.transparency = value
    
    default_value =  bpy.props.FloatProperty( get=default_value_get, set=default_value_set)
            
    # draw socket
    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label('Transparency Layer')
        else:
            layout.prop(self, "transparency", slider=True)    
    #
    def draw_color(self, context, node):
        return (float_socket)
#
bounty_socket_class.append(transparency_socket)

class transmit_socket(NodeSocket):
    bl_idname = 'transmit'
    bl_label = 'Transmittance Socket'  
    
    transmit_filter = MatProperty.transmit_filter
    
    # default values for socket
    def default_value_get(self):
        return self.transmit_filter
    
    def default_value_set(self, value):
        self.transmit_filter = value
    
    default_value =  bpy.props.FloatProperty( get=default_value_get, set=default_value_set)
    
    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text)
        else:
            layout.prop(self, "transmit_filter", slider=True) 
    #
    def draw_color(self, context, node):
        return (float_socket)
#
bounty_socket_class.append(transmit_socket)

#--------------------
# specular sockect
#--------------------
class mirror_color_socket(NodeSocket):
    bl_idname = 'mirror'
    bl_label = 'Mirror Socket'
    enabled = False
    
    mirror_color = FloatVectorProperty(
        name="Mirror", description="Mirror color reflection",
        subtype='COLOR', min=0.0, max=1.0, default=(1.0, 1.0, 1.0)
    )
    specular_reflect = MatProperty.specular_reflect
    
    # default values for socket's
    def default_value_get(self):
        return self.mirror_color
    
    def default_value_set(self, value):
        self.mirror_color = value
    
    default_value =  bpy.props.FloatVectorProperty( subtype='COLOR', get=default_value_get, set=default_value_set)
    #        
    def draw(self, context, layout, node, text):
        col = layout.column()
        label="Mirror color"
        if self.is_linked:
            label="Mirror layer"
        #else:
        col.prop(self, "mirror_color", text=label)
        col.prop(self, "specular_reflect", text='Mirror reflection')   
    #
    def draw_color(self, context, node):
        return (color_socket)
#
bounty_socket_class.append(mirror_color_socket)
'''
class mirror_reflect_socket(NodeSocket):
    bl_idname = 'specular'
    bl_label = 'Custom Node Socket'
    
    specular_reflect = MatProperty.specular_reflect
    
    # default values for socket's
    def default_value_get(self):
        return self.specular_reflect
    
    def default_value_set(self, value):
        self.specular_reflect = value
    
    default_value =  bpy.props.FloatProperty( get=default_value_get, set=default_value_set)
    
    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text)
        else:
            layout.prop(self, "specular_reflect", slider=True)    
    #
    def draw_color(self, context, node):
        return (float_socket)
#
bounty_socket_class.append(mirror_reflect_socket)
'''
class fresnel_socket(NodeSocket):
    bl_idname = "fresnel"
    bl_label = "Fresnel Socket"
    
    
    fresnel_effect = MatProperty.fresnel_effect
    IOR_reflection = MatProperty.IOR_reflection
    
    # default values for socket's
    def default_value_get(self):
        return self.fresnel_effect
    
    def default_value_set(self, value):
        self.fresnel_effect = value
    
    default_value =  bpy.props.BoolProperty( get=default_value_get, set=default_value_set)
    
    def draw(self, context, layout, node, text):
        col = layout.column()
        if self.is_linked:
            col.label(text)
        else:
            col.prop(self, "fresnel_effect", toggle=True)
            col.prop(self, "IOR_reflection")               
    #
    def draw_color(self, context, node):
        return (float_socket)
#
bounty_socket_class.append(fresnel_socket)    

class ior_socket(NodeSocket):
    bl_idname = "IOR"
    bl_label = "IOR Socket"
    
    IOR_reflection = MatProperty.IOR_reflection
    
    # default values for socket's
    def default_value_get(self):
        return self.IOR_reflection
    
    def default_value_set(self, value):
        self.IOR_reflection = value
    
    default_value =  FloatProperty( get=default_value_get, set=default_value_set)
        
    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text)
        else:
            layout.prop(self, "IOR_reflection")            
    #
    def draw_color(self, context, node):
        return (float_socket)
#
bounty_socket_class.append(ior_socket)

class mapping_socket(NodeSocket):
    bl_idname = 'mapping'
    bl_label = 'Texture Mapping Socket'
    enabled = False
    
    enum_texture_mapping_mode = [
        ('ORCO','Generated',""),
        ('OBJECT','Object',""),
        ('GLOBAL','Global',""),
        ('UV','UV',""),
        ('STRAND','Strand',""),
        ('WINDOW','Window',""),
        ('NORMAL','Normal',""),
        ('REFLECTION','Reflection',""),
        ('STRESS','Stress',""),
        ('TANGENT','Tangent',""),
    ]

    
    # small trick..
    enum_default_texture_mapping_mode = (('UV', 'UV',"UV texture mapping"),)
        
    # default values for socket's
    def default_value_get(self):
        return self.mapping_type
    
    def default_value_set(self, value):
        self.mapping_type = 'UV'
        
    mapping_type = EnumProperty(
            name="Mapping",
            description="Texture coordinates mapping mode",
            items=enum_texture_mapping_mode,
            default='UV',
    )
    default_value =  EnumProperty(items=enum_default_texture_mapping_mode, set=default_value_set)
    #
    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label('Mapping Coord.')
        else:
            layout.prop(self, "mapping_type")   
    #
    def draw_color(self, context, node):
        return (float_socket)
#
bounty_socket_class.append(mapping_socket)

#-----------------------
# BRDF socket
#-----------------------
class projection_socket(NodeSocket):
    bl_idname = 'projection'
    bl_label = 'Texture Projection Socket'

    enum_texture_projection_mode = [
        ('FLAT', 'Flat',"Flat texture projection"),
        ('CUBE', 'Cube',"Cube texture projection"),
        ('TUBE', 'Tube',"Cylindrical texture projection"),
        ('SPHERE', 'Sphere',"Spherical texture projection"),        
    ]
    # small trick..
    enum_default_texture_projection_mode = (('FLAT', 'Flat',"Flat texture mapping"),)
        
    # default values for socket's
    def default_value_get(self):
        return self.projection_type
    
    def default_value_set(self, value):
        self.projection_type = 'FLAT'
        
    projection_type = EnumProperty(
            name="Projection",
            description="Texture projection mode",
            items=enum_texture_projection_mode,
            default='FLAT',
    )    
    default_value =  EnumProperty(items=enum_default_texture_projection_mode, set=default_value_set)
    #
    def draw(self, context, layout, node, text):
        col = layout.column()
        if self.is_linked:
            col.label('Texture projection')
        else:
            col.prop(self, "projection_type")  
    #
    def draw_color(self, context, node):
        return (float_socket)
#
bounty_socket_class.append(projection_socket)


def register():
    for bountyclasses in bounty_socket_class:
        bpy.utils.register_class(bountyclasses)
    
def unregister():
    for bountyclasses in bounty_socket_class:
        bpy.utils.unregister_class(bountyclasses)


if __name__ == "__main__":
    register()
    