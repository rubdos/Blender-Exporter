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
from bpy.types import NodeTree, Node, NodeSocket
from bpy.props import FloatProperty
# test move here
import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem, NodeItemCustom
# end test

color_socket = (0.9, 0.9, 0.0, 1.0)
float_socket = (0.63, 0.63, 0.63, 1.0)

# Derived from the NodeTree base type, similar to Menu, Operator, Panel, etc.
class TheBountyShaderTree(NodeTree): #YAF_MT_MaterialNodeTree(NodeTree):
        #
        bl_idname = 'TheBountyShaderTree'
        bl_label = 'TheBounty Shader Tree'
        bl_icon = 'NODETREE' # MATERIAL

        @classmethod
        def poll(cls, context):
            return context.scene.render.engine == 'YAFA_RENDER'
        '''
        @classmethod
        def get_from_context(cls, context):
            ob = context.active_object
            if ob and ob.type not in {'LAMP', 'CAMERA'}:
                ma = ob.active_material
                if ma != None: 
                    nt_name = ma.renderman.nodetree
                    if nt_name != '':
                        return bpy.data.node_groups[ma.renderman.nodetree], ma, ma
            elif ob and ob.type == 'LAMP':
                la = ob.data
                nt_name = la.renderman.nodetree
                if nt_name != '':
                    return bpy.data.node_groups[la.renderman.nodetree], la, la
            return (None, None, None)
        '''
# Mix-in class for all custom nodes in this tree type.
# Defines a poll function to enable instantiation. 
class TheBountyNodeTree: #YAF_MT_NodeTree:
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'TheBountyShaderTree'

# Derived from the Node base type.
class YAF_MT_MaterialOutputNode(Node, TheBountyNodeTree):
    # Glossy shader node
    bl_idname = 'MaterialOutputNode'
    bl_label = 'Material Output'
    bl_icon = 'MATERIAL'
    
    def init(self, context):
        self.inputs.new('NodeSocketShader', "Shader")

#- Shiny diffuse sockets ------------------>
class yaf_diffuse_color_socket(NodeSocket):
    bl_idname = 'yaf_diffuse_color'
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
            layout.prop(mat, "diffuse_reflect", text="Diffuse Reflect")
    
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
            layout.prop(mat, "mirror_color", text="Mirror Color")
    
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
            layout.prop(yaf_mat, "fresnel_effect")
            
    # Socket color
    def draw_color(self, context, node):
        return (float_socket)

class YAF_MT_ShinyShaderNode(Node, TheBountyNodeTree):
    # Shiny Diffuse node
    bl_idname = 'ShinyDiffuseShaderNode'
    bl_label = 'Shiny Diffuse Shader'
    bl_icon = 'MATERIAL'

class YAF_MT_ShinyDiffuseShaderNode(Node, TheBountyNodeTree):
    # Shiny Diffuse node
    bl_idname = 'ShinyDiffuseShaderNode'
    bl_label = 'Shiny Diffuse Shader'
    bl_icon = 'MATERIAL'
    
    #
    def init(self, context):
        # slots shaders
        #self.inputs.new('yaf_diffuse_color', "Diffuse Color")
        #self.inputs.new('yaf_diffuse_reflection', "Diffuse Reflect")
        #self.inputs.new('yaf_mirror_color', "Mirror Color")
        #self.inputs.new('yaf_specular_reflection', "Specular Reflect")
        #self.inputs.new('yaf_fresnel', "Fresnel")
        #
        self.outputs.new('NodeSocketColor', "Shader")

    # Copy function to initialize a copied node from an existing one.
    def copy(self, node):
        print("Copying from node ", node)

    # Free function to clean up on removal.
    def free(self):
        print("Removing node ", self, ", Goodbye!")
        
    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        # 
        yaf_mat = context.active_object.active_material
        #layout = self.layout
        #yaf_mat = active_node_mat(context.material)

        split = layout.split()
        col = split.column()
        col.prop(yaf_mat, "diffuse_color")
        col.prop(yaf_mat, "emit")
        layout.row().prop(yaf_mat, "diffuse_reflect", slider=True)

        col = split.column()
        sub = col.column()
        sub.label(text="Reflectance model:")
        sub.prop(yaf_mat, "brdf_type", text="")
        brdf = sub.column()
        brdf.enabled = yaf_mat.brdf_type == "oren-nayar"
        brdf.prop(yaf_mat, "sigma")

        layout.separator()

        box = layout.box()
        #box.label(text="Transparency and translucency:")
        split = box.split()
        col = split.column()
        col.prop(yaf_mat, "transparency", slider=True)
        col = split.column()
        col.prop(yaf_mat, "translucency", slider=True)
        box.row().prop(yaf_mat, "transmit_filter", slider=True)
        
        # specular
        split = layout.split()
        col = split.column()
        col.label(text="Mirror color:")
        col.prop(yaf_mat, "mirror_color", text="")

        col = split.column()
        col.prop(yaf_mat, "fresnel_effect")
        sub = col.column()
        sub.enabled = yaf_mat.fresnel_effect
        sub.prop(yaf_mat, "IOR_reflection", slider=True)
        layout.row().prop(yaf_mat, "specular_reflect", slider=True)
        
    # Detail buttons in the sidebar.
    # If this function is not defined, the draw_buttons function is used instead
    def draw_buttons_ext(self, context, layout):
        pass

class YAF_MT_GlossyShaderNode(Node, TheBountyNodeTree):
    # Glossy shader node
    bl_idname = 'GlossyShaderNode'
    bl_label = 'Glossy Shader'
    bl_icon = 'MATERIAL'

    def init(self, context):
        self.inputs.new('NodeSocketColor', "Glossy Color")
        self.inputs.new('NodeSocketFloat', "Glossy Amount")
        #
        self.outputs.new('NodeSocketColor', "Shader Out")

    def draw_buttons(self, context, layout):
        """ Same design to a UI panels ( column, split, row..) """
        # sync values with panels
        yaf_mat = context.active_object.active_material
        split = layout.split()
        col = split.column()
        col.prop(yaf_mat, "diffuse_color")

        col = split.column()
        ref = col.column(align=True)
        ref.label(text="Reflectance model:")
        ref.prop(yaf_mat, "brdf_type", text="")
        sig = col.column()
        sig.enabled = yaf_mat.brdf_type == "oren-nayar"
        sig.prop(yaf_mat, "sigma")
        layout.row().prop(yaf_mat, "diffuse_reflect", slider=True)

        layout.separator()
    
    def draw_buttons_ext(self, context, layout):
        # mat = bpy.context.active_object.active_material
        # layout.prop(mat, "brdf_type")
        # layout.prop(mat, "sigma")
        pass

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")
               
class YAF_MT_GlassShaderNode(Node, TheBountyNodeTree):
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
        #mat = bpy.context.active_object.active_material
        pass
            
    def draw_buttons_ext(self, context, layout):
        #mat = bpy.context.active_object.active_material
        #layout.prop(mat, "brdf_type")
        #layout.prop(mat, "sigma")
        pass

    def copy(self, node):
        print("Copying from node ", node)
        
    def free(self):
        print("Removing node ", self, ", Goodbye!")

class YAF_MT_BlendShaderNode(Node, TheBountyNodeTree):
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
        #mat = bpy.context.active_object.active_material
        #layout.prop(mat, "blend_value", text="")
        layout.prop(self, "blend_value", text="Blend")

class YAF_MT_TextureShaderNode(Node, TheBountyNodeTree):
    # Texture shader node
    bl_idname = 'TextureShaderNode'
    bl_label = 'Texture Shader'
    bl_icon = 'TEXTURE'

    def init(self, context):
        self.inputs.new('NodeSocketColor', "Filter Color")
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
class YAF_NodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type =='TheBountyShaderTree'

# all categories in a list
yaf_node_categories = [
    # identifier, label, items list
    YAF_NodeCategory("YAF_OUTPUT", "Material Output", items=[
        # output node
        NodeItem("MaterialOutputNode"),
        ]),
    YAF_NodeCategory("YAF_SHADERS", "Shaders", items=[
        # shader nodes, use bl_idname's 
        NodeItem("ShinyDiffuseShaderNode"),
        NodeItem("GlossyShaderNode"),
        NodeItem("BlendShaderNode"),
        NodeItem("GlassShaderNode"),
        ]),
    YAF_NodeCategory("YAF_TEXTURES", "Textures", items=[
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
    bpy.utils.register_class(YAF_MT_MaterialOutputNode)
    bpy.utils.register_class(YAF_MT_ShinyDiffuseShaderNode)
    bpy.utils.register_class(YAF_MT_GlossyShaderNode)
    bpy.utils.register_class(YAF_MT_BlendShaderNode)
    bpy.utils.register_class(YAF_MT_GlassShaderNode)

def unregister():
    bpy.utils.unregister_class(TheBountyNodeTree)
    bpy.utils.unregister_class(yaf_diffuse_color_socket)
    bpy.utils.unregister_class(yaf_diffuse_reflect_socket)
    bpy.utils.unregister_class(yaf_mirror_reflect_socket)
    bpy.utils.unregister_class(yaf_fresnel_socket)
    bpy.utils.unregister_class(YAF_MT_MaterialOutputNode)
    bpy.utils.unregister_class(YAF_MT_ShinyDiffuseShaderNode)
    bpy.utils.unregister_class(YAF_MT_GlossyShaderNode)
    bpy.utils.unregister_class(YAF_MT_BlendShaderNode)
    bpy.utils.unregister_class(YAF_MT_GlassShaderNode)


if __name__ == "__main__":
    register()
