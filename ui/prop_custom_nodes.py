# # ---------- BEGIN GPL LICENSE BLOCK -----------------------------------------#
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
# ---------- END GPL LICENSE BLOCK -------------------------------------------#

# <pep8 compliant>

import bpy
from bpy.types import NodeTree, Node, NodeSocket
from bpy.props import FloatProperty
# test move here
from nodeitems_utils import NodeCategory, NodeItem


color_socket = (0.9, 0.9, 0.0, 1.0)
float_socket = (0.63, 0.63, 0.63, 1.0)

# Derived from the NodeTree base type, similar to Menu, Operator, Panel, etc.
class TheBountyShaderTree(NodeTree):
    #
    bl_idname = 'TheBountyShaderTree'
    bl_label = 'TheBounty Shader Tree'
    bl_icon = 'MATERIAL' #NODETREE' # 

    @classmethod
    def poll(cls, context):
        return context.scene.render.engine == 'THEBOUNTY'
    '''    
    @classmethod
    def get_from_context(cls, context):
        ob = context.active_object
        if ob and ob.type not in {'LAMP', 'CAMERA'}:
            ma = ob.active_material
            if ma != None: 
                nt_name = ma.bounty.nodetree #renderman.nodetree
                if nt_name != '':
                    return bpy.data.node_groups[ma.bounty.nodetree], ma, ma
        #elif ob and ob.type == 'LAMP':
        #    la = ob.data
        #    nt_name = la.renderman.nodetree
        #    if nt_name != '':
        #        return bpy.data.node_groups[la.renderman.nodetree], la, la
        return (None, None, None)
    '''    
    # This block updates the preview, when socket links change
    def update(self):
        self.refresh = True
    
    def acknowledge_connection(self, context):
        while self.refresh == True:
            self.refresh = False
            break
    
    refresh = bpy.props.BoolProperty(
                    name='Links Changed', 
                    default=False, 
                    update=acknowledge_connection)

        
# Mix-in class for all custom nodes in this tree type.
# Defines a poll function to enable instantiation. 
class TheBountyNodeTree:
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'TheBountyShaderTree'

# Derived from the Node base type.
class TheBountyMaterialOutputNode(Node, TheBountyNodeTree):
    bl_idname = 'MaterialOutputNode'
    bl_label = 'Material Output'
    bl_icon = 'MATERIAL'
    
    def init(self, context):
        self.inputs.new('NodeSocketShader', "Shader")
        

#- Shiny diffuse sockets ------------->
class diffuse_color_socket(NodeSocket):
    bl_idname = 'diffuse_color_socket'
    bl_label = 'Custom Node Socket'    
    
    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text)
        else:
            # sync values with panels
            mat = context.active_object.active_material
            layout.prop(mat, "diffuse_color", text="Diffuse Color")
    
    # Socket color
    def draw_color(self, context, node):
        return (color_socket)

class yaf_diffuse_reflect_socket(NodeSocket):
    bl_idname = 'yaf_diffuse_reflection'
    bl_label = 'Custom Node Socket'    
    
    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text)
        else:
            # sync values with panels
            mat = context.active_object.active_material
            layout.prop(mat.bounty, "diffuse_reflect", text="Diffuse Reflect")
    
    # Socket color
    def draw_color(self, context, node):
        return (float_socket)

#--------------- mirror ----------------------->
class yaf_mirror_color_socket(NodeSocket):
    bl_idname = 'yaf_mirror_color'
    bl_label = 'Custom Node Socket'    
    
    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text)
        else:
            # sync values with panels
            mat = context.active_object.active_material
            layout.prop(mat.bounty, "mirror_color", text="Mirror Color")
    
    # Socket color
    def draw_color(self, context, node):
        return (color_socket)

#
class yaf_mirror_reflect_socket(NodeSocket):
    bl_idname = 'yaf_specular_reflection'
    bl_label = 'Custom Node Socket'    
    
    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text)
        else:
            # sync values with panels
            mat = context.active_object.active_material
            layout.prop(mat, "specular_reflect", text="Reflection")
    
    # Socket color
    def draw_color(self, context, node):
        return (float_socket)

#----------- fresnel -------------------------->
class yaf_fresnel_socket(NodeSocket):
    bl_idname = "yaf_fresnel"
    bl_label = "Custom Node Socket"
    
    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text)
        else:
            yaf_mat = context.active_object.active_material
            layout.prop(yaf_mat.bounty, "fresnel_effect")
            
    # Socket color
    def draw_color(self, context, node):
        return (float_socket)

# class template.
class bountyDiffuseShader(Node, TheBountyNodeTree):
    # Shiny Diffuse node
    bl_idname = 'ShinyDiffuseComponent'
    bl_label = 'Diffuse Shader'
    bl_icon = 'MATERIAL'
    
    #
    def init(self, context):
        # slots shaders
        self.outputs.new('NodeSocketColor', "Shader")

    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        # test
        
        # import TheBountyShinyDiffuse().draw(context)
        mat = context.active_object.active_material

        split = layout.split()
        col = split.column()
        col.prop(mat, "diffuse_color")
        col.prop(mat, "emit")
        layout.row().prop(mat.bounty, "diffuse_reflect", slider=True)


class TheBountyShinyDiffuseShaderNode(Node, TheBountyNodeTree):
    # Shiny Diffuse node
    bl_idname = 'ShinyDiffuseShaderNode'
    bl_label = 'Shiny Diffuse Shader'
    bl_icon = 'MATERIAL'
    
    #
    def init(self, context):
        # slots shaders
        self.outputs.new('NodeSocketColor', "Shader")
        self.inputs.new('diffuse_color_socket','Shader')

    # Copy function to initialize a copied node from an existing one.
    def copy(self, node):
        print("Copying from node ", node)

    # Free function to clean up on removal.
    def free(self):
        print("Removing node ", self, ", Goodbye!")
        
    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        #
        mat = context.active_object.active_material

        split = layout.split()
        col = split.column()
        col.prop(mat, "diffuse_color")
        col.prop(mat, "emit")
        layout.row().prop(mat.bounty, "diffuse_reflect", slider=True)

        col = split.column()
        sub = col.column()
        sub.label(text="Reflectance model:")
        sub.prop(mat.bounty, "brdf_type", text="")
        brdf = sub.column()
        brdf.enabled = mat.bounty.brdf_type == "oren-nayar"
        brdf.prop(mat.bounty, "sigma")

        layout.separator()

        box = layout.box()
        split = box.split()
        col = split.column()
        col.prop(mat.bounty, "transparency", slider=True)
        col = split.column()
        col.prop(mat, "translucency", slider=True)
        box.row().prop(mat.bounty, "transmit_filter", slider=True)
        
        # specular
        split = layout.split()
        col = split.column()
        col.label(text="Mirror color:")
        col.prop(mat, "mirror_color", text="")

        col = split.column()
        col.prop(mat.bounty, "fresnel_effect")
        sub = col.column()
        sub.enabled = mat.bounty.fresnel_effect
        sub.prop(mat.bounty, "IOR_reflection", slider=True)
        layout.row().prop(mat.bounty, "specular_reflect", slider=True)
        
    # Detail buttons in the sidebar.
    # If this function is not defined, the draw_buttons function is used instead
    def draw_buttons_ext(self, context, layout):
        pass

class TheBountyGlossyShaderNode(Node, TheBountyNodeTree):
    # Glossy shader node
    bl_idname = 'GlossyShaderNode'
    bl_label = 'Glossy Shader'
    bl_icon = 'MATERIAL'

    def init(self, context):
        #
        self.outputs.new('NodeSocketColor', "Shader Out")
    
    def draw_buttons(self, context, layout):
        """ Same design to a UI panels ( column, split, row..) """
        # sync values with panels
        mat = context.active_object.active_material
        
        split = layout.split()
        col = split.column()
        col.prop(mat, "diffuse_color")

        col = split.column()
        ref = col.column(align=True)
        ref.label(text="Reflectance model:")
        ref.prop(mat.bounty, "brdf_type", text="")
        sig = col.column()
        sig.enabled = mat.bounty.brdf_type == "oren-nayar"
        sig.prop(mat.bounty, "sigma")
        layout.row().prop(mat.bounty, "diffuse_reflect", slider=True)

        layout.separator()
        split = layout.split()
        col = split.column()
        col.prop(mat.bounty, "glossy_color")
        exp = col.column()
        exp.enabled = mat.bounty.anisotropic == False
        exp.prop(mat.bounty, "exponent")

        col = split.column()
        sub = col.column(align=True)
        sub.prop(mat.bounty, "anisotropic")
        ani = sub.column()
        ani.enabled = mat.bounty.anisotropic == True
        ani.prop(mat.bounty, "exp_u")
        ani.prop(mat.bounty, "exp_v")
        layout.row().prop(mat.bounty, "glossy_reflect", slider=True)
        layout.row().prop(mat.bounty, "as_diffuse")

        layout.separator()

        if mat.bounty.mat_type == "coated_glossy":
            box = layout.box()
            box.label(text="Coated layer for glossy:")
            split = box.split()
            col = split.column()
            col.prop(mat.bounty, "coat_mir_col")
            col = split.column(align=True)
            col.label(text="Fresnel reflection:")
            col.prop(mat.bounty, "IOR_reflection")
            col.label()
    
    def draw_buttons_ext(self, context, layout):
        # mat = bpy.context.active_object.active_material
        # layout.prop(mat, "brdf_type")
        # layout.prop(mat, "sigma")
        pass

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")
        
               
class TheBountyGlassShaderNode(Node, TheBountyNodeTree):
    # Glass shader node
    bl_idname = 'GlassShaderNode'
    bl_label = 'Glass Shader'
    bl_icon = 'MATERIAL'

    def init(self, context):
        self.inputs.new('NodeSocketColor', "Filter Color")
        #
        self.outputs.new('NodeSocketColor', "Shader")

    def draw_buttons(self, context, layout):
        """ Same design to a UI panels ( column, split, row..) """
        mat = context.active_object.active_material
        
        layout.label(text="Refraction and Reflections:")
        split = layout.split()
        col = split.column()
        col.prop(mat.bounty, "IOR_refraction")

        col = split.column()
        col.menu("YAF_MT_presets_ior_list", text=bpy.types.YAF_MT_presets_ior_list.bl_label)

        split = layout.split()
        col = split.column(align=True)
        col.prop(mat.bounty, "absorption")
        col.prop(mat.bounty, "absorption_dist")

        col = split.column(align=True)
        col.label(text="Dispersion:")
        col.prop(mat.bounty, "dispersion_power")

        if mat.bounty.mat_type == "rough_glass":
            row = layout.row()
            #box.label(text="Glass roughness:")
            row.prop(mat.bounty, "refr_roughness",text="Roughness exponent", slider=True)



        split = layout.split()
        col = split.column()
        col.prop(mat.bounty, "filter_color")
        col = split.column()
        col.prop(mat.bounty, "glass_mir_col")
        layout.row().prop(mat.bounty, "glass_transmit", slider=True)
        layout.row().prop(mat.bounty, "fake_shadows")
            
    def draw_buttons_ext(self, context, layout):
        # many buttons..
        pass

    def copy(self, node):
        print("Copying from node ", node)
        
    def free(self):
        print("Removing node ", self, ", Goodbye!")

class TheBountyBlendShaderNode(Node, TheBountyNodeTree):
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
        # same design to UI
        try:
            mat = context.active_object.active_material
            layout.prop(mat.bounty, "blend_value", text="")
        except:
            print("Nonetype node")
        #layout.prop(self, "blend_amount", text="Blend")

class TheBountyTextureShaderNode(Node, TheBountyNodeTree):
    # Texture shader node
    bl_idname = 'TextureShaderNode'
    bl_label = 'Texture Shader'
    bl_icon = 'TEXTURE'

    def init(self, context):
        #self.inputs.new('NodeSocketColor', "Filter Color")
        #
        self.outputs.new('NodeSocketColor', "Shader")

    def draw_buttons(self, context, layout):
        """ Same design to a UI panels ( column, split, row..) """
        #mat = bpy.context.active_object.active_material
        pass
            
    def draw_buttons_ext(self, context, layout):
        pass

    def copy(self, node):
        print("Copying from node ", node)
        
    def free(self):
        print("Removing node ", self, ", Goodbye!")

# our own base class with an appropriate poll function,
# so the categories only show up in our own tree type
class TheBountyNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type =='TheBountyShaderTree'

# all categories in a list
TheBountyNodeCategories = [
    # identifier, label, items list
    TheBountyNodeCategory("TheBountyMaterial", "Material Output", items=[
        # output node
        NodeItem("MaterialOutputNode"),
        ]),
    TheBountyNodeCategory("TheBountyShaders", "Shaders", items=[
        # shader nodes, use bl_idname's 
        NodeItem("ShinyDiffuseShaderNode"),
        NodeItem("GlossyShaderNode"),
        NodeItem("BlendShaderNode"),
        NodeItem("GlassShaderNode"),
        NodeItem("ShinyDiffuseComponent"), # test
        ]),
    TheBountyNodeCategory("TheBountyTextures", "Textures", items=[
        # texture nodes
        NodeItem("TextureShaderNode"),
        ]),
    ]

def register():
    bpy.utils.register_class(TheBountyNodeTree)
    bpy.utils.register_class(yaf_diffuse_color_socket)
    bpy.utils.register_class(yaf_diffuse_reflect_socket)
    bpy.utils.register_class(yaf_mirror_reflect_socket)
    bpy.utils.register_class(yaf_fresnel_socket)
    bpy.utils.register_class(TheBountyMaterialOutputNode)
    bpy.utils.register_class(TheBountyMaterialOutputNode)
    bpy.utils.register_class(TheBountyGlossyShaderNode)
    bpy.utils.register_class(TheBountyBlendShaderNode)
    bpy.utils.register_class(TheBountyGlassShaderNode)

def unregister():
    bpy.utils.unregister_class(TheBountyNodeTree)
    bpy.utils.unregister_class(yaf_diffuse_color_socket)
    bpy.utils.unregister_class(yaf_diffuse_reflect_socket)
    bpy.utils.unregister_class(yaf_mirror_reflect_socket)
    bpy.utils.unregister_class(yaf_fresnel_socket)
    bpy.utils.unregister_class(TheBountyMaterialOutputNode)
    bpy.utils.unregister_class(TheBountyShinyDiffuseShaderNode)
    bpy.utils.unregister_class(TheBountyGlossyShaderNode)
    bpy.utils.unregister_class(TheBountyBlendShaderNode)
    bpy.utils.unregister_class(TheBountyGlassShaderNode)


if __name__ == "__main__":
    register()