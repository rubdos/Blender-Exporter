#---------- BEGIN GPL LICENSE BLOCK ------------------------------------------#
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
#  or visit https://www.fsf.org for more info.
#
#---------- END GPL LICENSE BLOCK --------------------------------------------#

# <pep8 compliant>

import bpy
from bpy.types import Node, NodeSocket
from bpy.props import (FloatProperty, 
                       FloatVectorProperty, 
                       StringProperty, 
                       BoolProperty,
                       EnumProperty)
# test move here
from nodeitems_utils import NodeCategory, NodeItem, NodeItemCustom

from ..prop.yaf_material import TheBountyMaterialProperties as MatProperty


color_socket = (0.9, 0.9, 0.0, 1.0)
float_socket = (0.63, 0.63, 0.63, 1.0)
enum_sockect = (0.0, 0.0, 1.0, 1.0)

bounty_node_class=[]
# Derived from the NodeTree base type, similar to Menu, Operator, Panel, etc.
class TheBountyNodeTree(bpy.types.NodeTree):
    #
    
    bl_idname = 'TheBountyNodeTree'
    bl_label = 'TheBounty Node Tree'
    bl_icon = 'MATERIAL'

    @classmethod
    def poll(cls, context):
        return context.scene.render.engine == 'THEBOUNTY'
    
    # code orignally from Matt Ebb's 3Delight exporter   
    @classmethod
    def get_from_context(cls, context):
        ob = context.active_object
        if ob and ob.type not in {'LAMP', 'CAMERA'}:
            active_mat = ob.active_material
            if active_mat != None: 
                nt_name = active_mat.bounty.nodetree
                if nt_name != '':
                    return bpy.data.node_groups[active_mat.bounty.nodetree], active_mat, active_mat
        #elif ob and ob.type == 'LAMP':
        #    la = ob.data
        #    nt_name = la.bounty.nodetree
        #    if nt_name != '':
        #        return bpy.data.node_groups[la.bounty.nodetree], la, la
        return (None, None, None)
        
    # This block updates the preview, when socket links change
    def update(self):
        self.refresh = True
    
    def acknowledge_connection(self, context):
        while self.refresh == True:
            self.refresh = False
            break
    
    refresh = BoolProperty(
                name='Links Changed', 
                default=False, 
                update=acknowledge_connection)
#    
bounty_node_class.append(TheBountyNodeTree)
  
class TheBountyNode:
    @classmethod
    def poll( cls, context):
        engine = context.scene.render.engine 
        return context.bl_idname == "TheBountyNodeTree" and engine == 'THEBOUNTY'

    def draw_buttons( self, context, layout):
        pass
        
    def draw_buttons_ext(self, context, layout):
        pass
    
    def copy( self, node):
        pass
    
    def free( self):
        print("Removing node ", self, ", Goodbye!")
    
    def draw_label( self):
        return self.bl_label
#
bounty_node_class.append(TheBountyNode)

#
#
class diffuse_color_socket(NodeSocket):
    #-----------------------
    # Diffuse color sockets 
    #-----------------------
    bl_idname = 'diffuse_color'
    bl_label = 'Custom Node Socket'    
    
    diff_color = MatProperty.diff_color
    
    # useful helper functions
    def default_value_get(self):
        return self.diff_color
    
    def default_value_set(self, value):
        self.diff_color = value
        
    default_value =  bpy.props.FloatVectorProperty( subtype='COLOR', get=default_value_get, set=default_value_set)
    
    #         
    def draw(self, context, layout, node, text):
        if self.is_linked and not self.is_output:
            layout.label('Diffuse Layer')
        else:
            layout.prop(self, "diff_color", text="Diffuse")    
    #
    def draw_color(self, context, node):
        return (color_socket)

#
bounty_node_class.append(diffuse_color_socket)

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
            layout.label(text)
        else:
            layout.prop(self, "diffuse_reflect", slider=True)    
    #
    def draw_color(self, context, node):
        return (float_socket)
#
bounty_node_class.append(diffuse_reflect_socket)

#-----------------------
# Emission socket 
#-----------------------    
class emitt_socket(NodeSocket):
    bl_idname = 'emittance'
    bl_label = 'Emission Socket'  
    
    emittance = MatProperty.emittance
    
    # default values
    def default_value_get(self):
        return self.emittance
    
    def default_value_set(self, value):
        self.emittance = value
    
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
bounty_node_class.append(emitt_socket)
#-----------------------
# BRDF socket
#-----------------------
class brdf_socket(NodeSocket):
    bl_idname = 'brdf'
    bl_label = 'BRDF Socket'
    enabled = False
    
    #brdf_type = MatProperty.brdf_type
    
    enum_reflectance_mode = [
        ('lambert', "Lambert", "Reflectance Model",0),
        ('oren-nayar', "Oren-Nayar", "Reflectance Model",1),
        
    ]
    # small trick..
    enum_reflectance_default_mode = (('lambert', "Lambert", "Reflectance Model"),)
        
    # default values for socket's
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
    default_value =  EnumProperty(items=enum_reflectance_default_mode, set=default_value_set)#enum_reflectance_mode[1])
    #
    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text)
        else:
            layout.prop(self, "brdf_type", slider=True)    
    #
    def draw_color(self, context, node):
        return (float_socket)
#
bounty_node_class.append(brdf_socket)

class TheBountyBrdfNode(Node, TheBountyNode):
    #    
    bl_idname = 'brdf'
    bl_label = 'BRDF Node'
    bl_width_min = 160  
    
    brdf_type = MatProperty.brdf_type
    sigma = MatProperty.sigma
   
    #
    def init(self, context):
        self.outputs.new('NodeSocketColor', 'Color')
        
    def draw_buttons(self, context, layout):
        layout.prop(self, 'brdf_type', text='')
        layout.prop(self,'sigma', text='', slider=True)       
#
bounty_node_class.append(TheBountyBrdfNode)

class sigma_socket(NodeSocket):
    bl_idname = 'sigma'
    bl_label = 'Sigma Socket'
    hide_value = True 
    
    sigma = MatProperty.sigma
    
    # default values for socket's
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
bounty_node_class.append(sigma_socket)

#----------------
# trans. sockec
#----------------
class translucency_socket(NodeSocket):
    bl_idname = 'translucency'
    bl_label = 'Translucency Socket'  
    
    translucency = MatProperty.translucency
    
    # default values for socket's
    def default_value_get(self):
        return self.translucency
    
    def default_value_set(self, value):
        self.translucency = value
        
    default_value =  bpy.props.FloatProperty( get=default_value_get, set=default_value_set)
    #    
    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text)
        else:
            layout.prop(self, "translucency", slider=True)    
    # 
    def draw_color(self, context, node):
        return (float_socket)
#
bounty_node_class.append(translucency_socket)
    
class transparency_socket(NodeSocket):
    bl_idname = 'transparency'
    bl_label = 'Transparency Socket'  
    
    transparency = MatProperty.transparency
    
    # default values for socket's
    def default_value_get(self):
        return self.transparency
    
    def default_value_set(self, value):
        self.transparency = value
    
    default_value =  bpy.props.FloatProperty( get=default_value_get, set=default_value_set)
            
    # draw socket
    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text)
        else:
            layout.prop(self, "transparency", slider=True)    
    #
    def draw_color(self, context, node):
        return (float_socket)
#
bounty_node_class.append(transparency_socket)

class transmit_socket(NodeSocket):
    bl_idname = 'transmit'
    bl_label = 'Transmittance Socket'  
    
    transmit_filter = MatProperty.transmit_filter
    
    # default values for socket's
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
bounty_node_class.append(transmit_socket)
#--------------------
# specular sockects
#--------------------
class mirror_color_socket(NodeSocket):
    bl_idname = 'mirror'
    bl_label = 'Mirror Socket'
    
    mirror_color = FloatVectorProperty(
        name="Mirror", description="Mirror color reflection",
        subtype='COLOR', min=0.0, max=1.0, default=(1.0, 1.0, 1.0)
    )
    
    # default values for socket's
    def default_value_get(self):
        return self.mirror_color
    
    def default_value_set(self, value):
        self.mirror_color = value
    
    default_value =  bpy.props.FloatVectorProperty( subtype='COLOR', get=default_value_get, set=default_value_set)
    #        
    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text)
        else:
            layout.prop(self, "mirror_color")    
    #
    def draw_color(self, context, node):
        return (color_socket)
#
bounty_node_class.append(mirror_color_socket)

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
bounty_node_class.append(mirror_reflect_socket)

class fresnel_socket(NodeSocket):
    bl_idname = "fresnel"
    bl_label = "Fresnel Socket"
    hide_value = True
    
    fresnel_effect = MatProperty.fresnel_effect
    
    # default values for socket's
    def default_value_get(self):
        return self.fresnel_effect
    
    def default_value_set(self, value):
        self.fresnel_effect = value
    
    default_value =  bpy.props.BoolProperty( get=default_value_get, set=default_value_set)
    
    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text)
        else:
            layout.prop(self, "fresnel_effect")            
    #
    def draw_color(self, context, node):
        return (float_socket)
#
bounty_node_class.append(fresnel_socket)    

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
bounty_node_class.append(ior_socket)    
       
#------------------------
# Imagemap node
#------------------------
class TheBountyImageMapNode(Node, TheBountyNode):
    # for register category
    bl_idname = 'TheBountyImageMapNode'
    # for name on node editor tab
    bl_label = 'ImageMap Node'
    # 
    bl_width_min = 160
    
    #-----------------------------------------------
    # test for re-use definitions from 'prop' folder
    #-----------------------------------------------
    diff_color = MatProperty.diff_color
    diff_reflect = MatProperty.diffuse_reflect
    
    #----------------------------------------------- 
    # but also is possible create a next properties
    #-----------------------------------------------
    influence = FloatProperty(
        name="Influence", description="Amount of texture/color influence on a  material ( 0 : color, 1: texture)",
        min=0.0, max=1.0, step=1, precision=3,
        soft_min=0.0, soft_max=1.0, default=1.00
    )
    image_map = StringProperty(
        name="", description="Image File to be used on texture",
        subtype='FILE_PATH', default=""
    )
    #
    def init(self, context):
        self.outputs.new('NodeSocketColor', 'Color')
        
    def draw_buttons(self, context, layout):
        layout.prop(self, 'diff_color', text='Color')
        layout.prop(self,'diff_reflect', text='Influence', slider=True)
        layout.prop(self, "image_map")        
#
bounty_node_class.append(TheBountyImageMapNode)        
        
class TheBountyMirrorNode(Node, TheBountyNode):
    bl_idname = 'TheBountyMirrorNode'
    bl_label = 'Mirror Node'    
    
    mirror_color = MatProperty.mirror_color
    specular_reflect = MatProperty.specular_reflect
    
    def init(self, context):
        self.outputs.new('NodeSocketColor', "Color")
        
    def draw_buttons(self, context, layout):
        col = layout.column()
        col.prop(self, 'mirror_color')
        col.prop(self, 'specular_reflect', slider=True)
#
bounty_node_class.append(TheBountyMirrorNode)    

class TheBountyMaterialOutputNode(Node, TheBountyNode):
    bl_idname = 'MaterialOutputNode'
    bl_label = 'Material Output'
    bl_icon = 'NODETREE'
    bl_width_min = 120
    
    def init(self, context):
        self.inputs.new('NodeSocketShader', "ShaderTree")
    
    def draw_buttons(self, context, layout):
        try:
            layout.label(context.active_object.active_material.name)
        except:
            layout.label(context.material.name)
#
bounty_node_class.append(TheBountyMaterialOutputNode)
        
#---------------------------
# Shiny Diffuse shader node
#---------------------------               
class TheBountyShinyDiffuseShaderNode(Node, TheBountyNode):
    # Shiny Diffuse node
    bl_idname = 'ShinyDiffuseShaderNode'
    bl_label = 'ShinyDiffuseMat'
    bl_icon = 'MATERIAL'
    bl_width_min = 160
    
    #
    def init(self, context):
        # slots shaders
        self.outputs.new('NodeSocketColor', "Shader")
        
        self.inputs.new('diffuse_color',"Color")
        self.inputs.new('diffuse_reflection', 'Reflection')
        self.inputs.new('emittance', 'Emission')
        
        self.inputs.new('brdf', 'BRDF')
        self.inputs.new('sigma', 'Sigma')
        
        self.inputs.new('transparency', 'Alpha')
        self.inputs.new('translucency', 'Translucency')
        self.inputs.new('transmit', 'Transmit')
        
        self.inputs.new('mirror', 'Mirror')
        self.inputs.new('specular', 'Specular')
        
        #self.inputs.new('fresnel', 'Fresnel Effect')
        #self.inputs.new('IOR', 'IOR')
        
        self.inputs.new('NodeSocketColor', "BumpMap")
    
    def copy(self, node):
        # Copy function to initialize a copied node from an existing one.
        print("Copying from node ", node)

    def free(self):
        # Free function to clean up on removal.
        print("Removing node ", self, ", Goodbye!")
    #
    # Non socket properties
    fresnel_effect = MatProperty.fresnel_effect
    brdf_type = MatProperty.brdf_type
    sigma = MatProperty.sigma
    
    IOR_reflection = MatProperty.IOR_reflection
    
    def draw_buttons(self, context, layout):
        # Additional buttons displayed on the node.
        #mat = context.active_object.active_material
        #box = layout.box()
        #box.prop(self, 'brdf_type', text='')
        #box.prop(self, 'sigma')
        #
        box = layout.box()
        box.prop(self, 'fresnel_effect', toggle=True)
        box.prop(self, 'IOR_reflection')
        

        
    def draw_buttons_ext(self, context, layout):
        # Detail buttons in the sidebar.
        # If this function is not defined, the draw_buttons function is used instead
        pass
#
bounty_node_class.append(TheBountyShinyDiffuseShaderNode)

class TheBountyTranslucenShaderNode(Node, TheBountyNode):
    # Shiny Diffuse node
    bl_idname = 'TranslucentScattering'
    bl_label = 'Scattering Shader'
    bl_icon = 'MATERIAL'
    bl_width_min = 180
    
    #
    def init(self, context):
        # slots shaders
        self.outputs.new('NodeSocketColor', "Shader")
    
    def draw_buttons(self, context, layout):
        #
        mat = context.active_object.active_material
                
        col = layout.column()
        col.prop(mat, "diffuse_color")
        col.prop(mat.bounty, "diffuse_reflect", text="Diff. Reflect",slider=True)
        col.prop(mat.bounty, "glossy_color")#Glossy color")
        col.prop(mat.bounty, "glossy_reflect", text="Gloss. Reflect",slider=True)
        col.prop(mat.bounty, "sssSpecularColor")
        col.prop(mat.bounty, "exponent", text="Specular Exponent")
        
        row = layout.row()
        row.label("SSS Presets")
        row.menu("TheBountyScatteringPresets", text=bpy.types.TheBountyScatteringPresets.bl_label)
        
        col = layout.column()        
        
        col.prop(mat.bounty, "sssSigmaS", text="Scatter color")
        col.prop(mat.bounty, "sssSigmaS_factor")
        col.prop(mat.bounty, "phaseFuction")
                
        col.prop(mat.bounty, "sssSigmaA", text="Absorption color")
        col.prop(mat.bounty, "sss_transmit", text="Transmit")
        col.prop(mat.bounty, "sssIOR")
#
bounty_node_class.append(TheBountyTranslucenShaderNode)

class TheBountyGlossyShaderNode(Node, TheBountyNode):
    # Glossy shader node
    bl_idname = 'GlossyShaderNode'
    bl_label = 'Glossy Shader'
    bl_icon = 'MATERIAL'
    
    def init(self, context):
        #
        self.outputs.new('NodeSocketColor', "Shader")
        
        self.inputs.new('diffuse_color',"Diffuse Color")
        self.inputs.new('diffuse_reflection', 'Diffuse Reflection')
        
        self.inputs.new('brdf', 'BRDF Type')
        self.inputs.new('sigma', 'Sigma')
    
    def draw_buttons(self, context, layout):
        """ Same design to a UI panels ( column, split, row..) """
        # sync values with panels
        mat = context.active_object.active_material
        
        col = layout.column()
        
        col = layout.column()
        col.prop(mat.bounty, "glossy_color")
        exp = col.column()
        exp.enabled = mat.bounty.anisotropic == False
        exp.prop(mat.bounty, "exponent")

        #col = split.column()
        sub = col.column(align=True)
        sub.prop(mat.bounty, "anisotropic")
        ani = sub.column()
        ani.enabled = mat.bounty.anisotropic == True
        ani.prop(mat.bounty, "exp_u")
        ani.prop(mat.bounty, "exp_v")
        col= layout.column()
        col.prop(mat.bounty, "glossy_reflect", slider=True)
        col.row().prop(mat.bounty, "as_diffuse")

        layout.separator()

        if mat.bounty.mat_type == "coated_glossy":
            box = layout.box()
            box.label(text="Coated layer")
            col = layout.column()
            col.prop(mat.bounty, "coat_mir_col")
            col.label(text="Fresnel reflection:")
            col.prop(mat.bounty, "IOR_reflection")
    
    def draw_buttons_ext(self, context, layout):
        # many buttons..
        pass

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")
#
bounty_node_class.append(TheBountyGlossyShaderNode)
                       
class TheBountyGlassShaderNode(Node, TheBountyNode):
    # Glass shader node
    bl_idname = 'GlassShaderNode'
    bl_label = 'Glass Shader'
    bl_icon = 'MATERIAL'

    def init(self, context):
        #
        self.outputs.new('NodeSocketColor', "Shader")

    def draw_buttons(self, context, layout):
        """ Same design to a UI panels ( column, split, row..) """
        mat = context.active_object.active_material
        
        layout.label(text="Refraction and Reflections:")
        col = layout.column()
        col.prop(mat.bounty, "IOR_refraction")

        # TODO: need review..
        #col.menu("YAF_MT_presets_ior_list", text=bpy.types.YAF_MT_presets_ior_list.bl_label)

        col.prop(mat.bounty, "absorption")
        col.prop(mat.bounty, "absorption_dist")

        col.prop(mat.bounty, "dispersion_power")

        if mat.bounty.mat_type == "rough_glass":
            col = layout.column()
            #box.label(text="Glass roughness:")
            col.prop(mat.bounty, "refr_roughness",text="Roughness exponent", slider=True)

        col.prop(mat.bounty, "filter_color")
        col.prop(mat.bounty, "glass_mir_col")
        col.prop(mat.bounty, "glass_transmit", slider=True)
        col.prop(mat.bounty, "fake_shadows")
            
    def draw_buttons_ext(self, context, layout):
        # many buttons..
        pass

    def copy(self, node):
        print("Copying from node ", node)
        
    def free(self):
        print("Removing node ", self, ", Goodbye!")
#
bounty_node_class.append(TheBountyGlassShaderNode)

class TheBountyBlendShaderNode(Node, TheBountyNode):
    # Glossy custom node
    bl_idname = 'BlendShaderNode'
    bl_label = 'Blend Shader'
    bl_icon = 'MATERIAL'
        
    # test
    # TODO: is need find the methode for acces to this parameter for exporter
    blend_amount = FloatProperty(
        name="Blend value",
        description="Amount of blending materials",
        default=0.5, min=0.0, max=1.0)

    def init(self, context):
        self.inputs.new('NodeSocketShader', "Material One")
        self.inputs.new('NodeSocketShader', "Material Two")
        # outputs
        self.outputs.new('NodeSocketShader', "Out")

    def draw_buttons(self, context, layout):
        try:
            mat = context.active_object.active_material
            layout.prop(self, "blend_amount", text="")
        except:
            print("Nonetype node")
#
bounty_node_class.append(TheBountyBlendShaderNode)

class TheBountyTextureShaderNode(Node, TheBountyNode):
    # Texture shader node
    bl_idname = 'TextureShaderNode'
    bl_label = 'Texture Shader'
    bl_icon = 'TEXTURE'

    def init(self, context):
        #self.inputs.new('NodeSocketColor', "Filter Color")
        #
        self.outputs.new('NodeSocketColor', "Shader")

    def draw_buttons(self, context, layout):
        #
        pass
            
    def draw_buttons_ext(self, context, layout):
        pass

    def copy(self, node):
        print("Copying from node ", node)
        
    def free(self):
        print("Removing node ", self, ", Goodbye!")
#
bounty_node_class.append(TheBountyTextureShaderNode)

# our own base class with an appropriate poll function,
# so the categories only show up in our own tree type
class TheBountyNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        engine = context.scene.render.engine
        return context.space_data.tree_type =='TheBountyNodeTree' and engine == 'THEBOUNTY'

# all categories in a list
TheBountyNodeCategories = [
    # identifier, label, items list
    #TheBountyNodeCategory("TheBountyLight", "Light Output", items=[
    #    # output node
    #    NodeItem("LampOutputNode"),
    #    ]),
    TheBountyNodeCategory("TheBountyMaterial", "Material", items=[
        # output node
        NodeItem("MaterialOutputNode"),
        ]),
    TheBountyNodeCategory("TheBountyShaders", "Shaders", items=[
        # shader nodes, use bl_idname's 
        NodeItem(TheBountyShinyDiffuseShaderNode.bl_idname),
        NodeItem(TheBountyBrdfNode.bl_idname),
        NodeItem(TheBountyGlossyShaderNode.bl_idname),
        NodeItem(TheBountyBlendShaderNode.bl_idname),
        NodeItem(TheBountyGlassShaderNode.bl_idname),
        NodeItem(TheBountyTranslucenShaderNode.bl_idname),
        ]),
    TheBountyNodeCategory("TheBountyTextures", "Textures", items=[
        # texture nodes
        NodeItem(TheBountyImageMapNode.bl_idname),
        #NodeItem(TheBountyBrdfNode.bl_idname)
        ]),
    ]
#
bounty_node_class.append(TheBountyNodeCategory)


def register():
    for bclass in bounty_node_class:
        bpy.utils.register_class(bclass)
    
def unregister():
    for bclass in bounty_node_class:
        bpy.utils.unregister_class(bclass)


if __name__ == "__main__":
    register()
