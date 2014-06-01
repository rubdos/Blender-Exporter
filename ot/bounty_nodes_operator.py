# ---------- BEGIN GPL LICENSE BLOCK -----------------------------------------#
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
'''
Created on 13/05/2014

@author: Pedro
'''
import bpy

# test for nodetree operator
class TheBountyAddNodetree(bpy.types.Operator):
    ''''''
    bl_idname = "bounty.add_nodetree"
    bl_label = "Add Nodetree"
    bl_description = "Add a node tree linked to this material"

    def execute(self, context):
        idtype = 'material'
        context_data = {'material':context.material}
        idblock = context_data[idtype]
        # node_active = context.active_node
        # node_selected = context.selected_nodes
        
        nt = bpy.data.node_groups.new(idblock.name, type='TheBountyShaderTree')
        nt.use_fake_user = True
        idblock.bounty.nodetree = nt.name
        # test
        mat = context.material.bounty
        
        bountyNodeTypes = {
                'shinydiffusemat':'ShinyDiffuseShaderNode',
                'glossy':'GlossyShaderNode',
                'coated_glossy':'GlossyShaderNode',
                'glass':'GlassShaderNode',
                'rough_glass':'GlassShaderNode',
                'blend':'BlendShaderNode',
                'translucent':'TranslucentScattering'}
        
        #--------------------------------------
        if idtype == 'material':            
            shader =  nt.nodes.new(bountyNodeTypes[mat.mat_type])
            shader.location = 100,250
            sh_out = nt.nodes.new('MaterialOutputNode')
            sh_out.location = 300,200
            nt.links.new(shader.outputs[0],sh_out.inputs[0])
        #--------------------------------------            
        
        return {'FINISHED'}


if __name__ == '__main__':
    pass