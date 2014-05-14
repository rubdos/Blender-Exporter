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
        
        nt = bpy.data.node_groups.new(idblock.name, type='TheBountyShaderTree')
        nt.use_fake_user = True
        idblock.bounty.nodetree = nt.name

        if idtype == 'material':
            nt.nodes.new('MaterialOutputNode')
        
        #
        mat = context.material.bounty
        
        if mat.mat_type == 'shinydiffusemat':
            nt.nodes.new('ShinyDiffuseShaderNode')
        
        if mat.mat_type == 'glossy':
            nt.nodes.new('GlossyShaderNode')
            
        if mat.mat_type == 'coated_glossy':
            nt.nodes.new('GlossyShaderNode')
            
        if mat.mat_type == 'glass':
            nt.nodes.new('GlassShaderNode')
            
        if mat.mat_type == 'rough_glass':
            nt.nodes.new('GlassShaderNode')
            
        if mat.mat_type == 'blend':
            pass
        
        if mat.mat_type == 'translucent':
            pass
            
        
        return {'FINISHED'}


if __name__ == '__main__':
    pass