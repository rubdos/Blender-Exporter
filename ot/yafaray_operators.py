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
import mathutils
from bpy.types import Operator
from bpy.props import PointerProperty, StringProperty

class OBJECT_OT_get_position(Operator):
    bl_label = "From( get position )"
    bl_idname = "world.get_position"
    bl_description = "Get the position of the sun from the selected lamp location"

    def execute(self, context):
        warning_message = sunPosAngle(mode="get", val="position")
        if warning_message:
            self.report({'WARNING'}, (warning_message))
            return {'CANCELLED'}
        else:
            return{'FINISHED'}


class OBJECT_OT_get_angle(Operator):
    bl_label = "From( get angle )"
    bl_idname = "world.get_angle"
    bl_description = "Get the position of the sun from selected lamp angle"

    def execute(self, context):
        warning_message = sunPosAngle(mode="get", val="angle")
        if warning_message:
            self.report({'WARNING'}, (warning_message))
            return {'CANCELLED'}
        else:
            return{'FINISHED'}


class OBJECT_OT_update_sun(Operator):
    bl_label = "From( update sun )"
    bl_idname = "world.update_sun"
    bl_description = "Update the position and angle of selected lamp in 3D View according to GUI values"

    def execute(self, context):
        warning_message = sunPosAngle(mode="update")
        if warning_message:
            self.report({'WARNING'}, (warning_message))
            return {'CANCELLED'}
        else:
            return{'FINISHED'}


def sunPosAngle(mode="get", val="position"):
    active_object = bpy.context.active_object
    scene = bpy.context.scene
    world = scene.world.bounty

    if active_object and active_object.type == "LAMP":

        if mode == "get":
            # get the position of the sun from selected lamp 'location'
            if val == "position":
                location = mathutils.Vector(active_object.location)

                if location.length:
                    point = location.normalized()
                else:
                    point = location.copy()

                world.bg_from = point
                return
            # get the position of the sun from selected lamps 'angle'
            elif val == "angle":
                matrix = mathutils.Matrix(active_object.matrix_local).copy()
                world.bg_from = (matrix[0][2], matrix[1][2], matrix[2][2])
                return

        elif mode == "update":

            # get gui from vector and normalize it
            bg_from = mathutils.Vector(world.bg_from).copy()
            if bg_from.length:
                bg_from.normalize()

            # set location
            sundist = mathutils.Vector(active_object.location).length
            active_object.location = sundist * bg_from

            # compute and set rotation
            quat = bg_from.to_track_quat("Z", "Y")
            eul = quat.to_euler()

            # update sun rotation and redraw the 3D windows
            active_object.rotation_euler = eul
            return

    else:
        return "No selected LAMP object in the scene!"

def checkSSS():
    for mat in bpy.data.materials:
        if mat.bounty.mat_type == 'translucent':
            return True    
    return False

def checkSceneLights():
    scene = bpy.context.scene
    world = bpy.context.scene.world.bounty
    
    # expand function for include light from 'add sun' or 'add skylight' in sunsky or sunsky2 mode    
    haveLights = False
    # use light create with sunsky, sunsky2 or with use ibl ON
    if world.bg_add_sun or world.bg_background_light or world.bg_use_ibl:
        return True
    # if above is true, this 'for' is not used
    for sceneObj in scene.objects:
        if not sceneObj.hide_render and sceneObj.is_visible(scene): # check lamp, meshlight or portal light object
            if sceneObj.type == "LAMP" or sceneObj.bounty.geometry_type in {'mesh_light', 'portal_light'}:
                haveLights = True
                break
    #
    return haveLights

class TheBounty_OT_render_view(Operator):
    bl_label = "TheBounty render view"
    bl_idname = "bounty.render_view"
    bl_description = "Renders using the view in the active 3d viewport"

    @classmethod
    def poll(cls, context):

        return context.scene.render.engine == 'THEBOUNTY'

    def execute(self, context):
        view3d = context.region_data
        bpy.types.THEBOUNTY.useViewToRender = True
        scene = context.scene
        
        #------------------------------------------------------
        # Get the 3d view under the mouse cursor if the region
        # is not a 3d view then search for the first active one
        #------------------------------------------------------
        if not view3d:
            for area in [a for a in bpy.context.window.screen.areas if a.type == "VIEW_3D"]:
                view3d = area.spaces.active.region_3d
                break

        if not view3d or view3d.view_perspective == "ORTHO":
            self.report({'WARNING'}, ("The selected view is not in perspective mode or there was no 3d view available to render."))
            bpy.types.THEBOUNTY.useViewToRender = False
            return {'CANCELLED'}

        #----------------------------------------------
        # Check first the easiest or lighter question
        # atm, only is need check lights for bidir case
        #---------------------------------------------- 
        if scene.bounty.intg_light_method == "bidirectional":
            if not checkSceneLights():
                self.report({'WARNING'}, ("You use Bidirectional integrator and NOT have lights in the scene!"))
                bpy.types.THEBOUNTY.useViewToRender = False
                return {'CANCELLED'}        
        
        if scene.bounty.intg_useSSS:
            if scene.bounty.intg_light_method in {'directlighting','photonmapping','pathtracing'}:
                if not checkSSS():
                    self.report({'WARNING'}, ("You use SSS integrator and NOT have SSS materials in the scene!"))
                    return {'CANCELLED'}

        bpy.types.THEBOUNTY.viewMatrix = view3d.view_matrix.copy()
        bpy.ops.render.render('INVOKE_DEFAULT')
        return {'FINISHED'}


class TheBounty_OT_render_animation(Operator):
    bl_label = "TheBounty render animation"
    bl_idname = "bounty.render_animation"
    bl_description = "Render active scene"

    @classmethod
    def poll(cls, context):

        return context.scene.render.engine == 'THEBOUNTY'

    def execute(self, context):
        scene = context.scene
        
        #----------------------------------------------
        # check first the easiest or lighter question
        # atm, only is need check lights for bidir case
        #---------------------------------------------- 
        if scene.bounty.intg_light_method == "bidirectional":
            if not checkSceneLights():
                self.report({'WARNING'}, ("You use Bidirectional integrator and NOT have lights in the scene!"))
                return {'CANCELLED'}
        
        if scene.bounty.intg_useSSS:
            # check only for a valid integrator method
            if scene.bounty.intg_light_method in {'directlighting','photonmapping','pathtracing'}:
                if not checkSSS():
                    self.report({'WARNING'}, ("You use SSS integrator and NOT have SSS materials in the scene!"))
                    return {'CANCELLED'}

        bpy.ops.render.render('INVOKE_DEFAULT')
        return {'FINISHED'}


class TheBounty_OT_render_still(Operator):
    bl_label = "TheBounty render still"
    bl_idname = "bounty.render_still"
    bl_description = "Render active scene"

    @classmethod
    def poll(cls, context):

        return context.scene.render.engine == 'THEBOUNTY'

    def execute(self, context):
        scene = context.scene
        
        #----------------------------------------------
        # check first the easiest or lighter question
        # atm, only is need check lights for bidir case
        #---------------------------------------------- 
        if scene.bounty.intg_light_method == "bidirectional":
            if not checkSceneLights():
                self.report({'WARNING'}, ("You use Bidirectional integrator and NOT have lights in the scene!"))
                return {'CANCELLED'}
        
        if scene.bounty.intg_useSSS:
            if scene.bounty.intg_light_method in {'directlighting','photonmapping','pathtracing'}:
                if not checkSSS():
                    self.report({'WARNING'}, ("You use SSS integrator and NOT have SSS materials in the scene!"))
                    return {'CANCELLED'}

        bpy.ops.render.render('INVOKE_DEFAULT')
        return {'FINISHED'}


class TheBounty_OT_presets_ior_list(Operator):
    bl_idname = "material.set_ior_preset"
    bl_label = "IOR presets"
    index = bpy.props.FloatProperty()
    name = bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        mat = context.material
        return mat.bounty.mat_type in {"glass", "rough_glass"}

    def execute(self, context):
        mat = context.material
        bpy.types.TheBounty_presets_ior_list.bl_label = self.name
        mat.bounty.IOR_refraction = self.index
        return {'FINISHED'}

#-------------------------------------------
# Add support for use ibl files
#-------------------------------------------
import re, os
   
class ThebountyParseIBL(Operator):
    bl_idname = "world.parse_ibl"
    bl_label = "Parse IBL"
    iblValues = {}
    
    @classmethod
    def poll(cls, context):
        world = context.world
        return world and (world.bounty.bg_type == "Texture")
    #
    def execute(self, context):
        world = context.world.bounty
        scene = context.scene
        file = world.ibl_file
        # parse..
        self.iblValues = self.parseIbl(file)
        # maybe dirname only work with Win OS ??
        # TODO: test on linux OS
        iblFolder = os.path.dirname(file) 
        print(iblFolder)
        worldTexture = scene.world.active_texture
        if worldTexture.type == "IMAGE" and (worldTexture.image is not None):
            evfile = self.iblValues.get('EV')
            newval = os.path.join(iblFolder, evfile) 
            worldTexture.image.filepath = newval #self.iblValues.get('EV')
        
        return {'FINISHED'}
    
    #---------------------
    # some parse helpers
    #---------------------
    def parseValue(self, linea, valueType):
        items = re.split(" ", linea)
        item = items[2]  # items[1] is '='
        if valueType == 2:
            ext = (len(item) - 2)
            return item[1:ext]            
        elif valueType == 1:
            return int(item)
        elif valueType == 0:
            return float(item)
    
    #---------------------
    # parse .ibl file
    #---------------------
    def parseIbl(self, filename):
        f = open(filename, 'r')
        linea = f.readline()
        while linea != "":
            linea = f.readline()
            if linea[:7] == 'ICOfile':
                self.parseValue(linea, 2) # string
            #
            if linea[:11] == 'PREVIEWfile':
                self.iblValues['PRE']= self.parseValue(linea, 2) #PREVIEWfile          
            #
            if linea[:6] == 'BGfile':
                self.iblValues['BG']= self.parseValue(linea, 2) #BGfile
            #
            if linea[:8] == 'BGheight':
                self.parseValue(linea, 1) # integer
            #
            if linea[:6] == 'EVfile':
                self.iblValues['EV']= self.parseValue(linea, 2) #EVfile
            #
            if linea[:8] == 'EVheight':
                self.parseValue(linea, 1) # integer
            #
            if linea[:7] == 'EVgamma':
                self.parseValue(linea, 0) # float
                
            if linea[:7] == 'REFfile':
                self.iblValues['REF']= self.parseValue(linea, 2) #REFfile
                
            if linea[:9] == 'REFheight':
                self.parseValue(linea, 1) # integer
                
            if linea[:8] == 'REFgamma':
                self.parseValue(linea, 0) # float
                     
        f.close()
        return self.iblValues
# test

def register():
    bpy.utils.register_class(OBJECT_OT_get_position)
    bpy.utils.register_class(OBJECT_OT_get_angle)
    bpy.utils.register_class(OBJECT_OT_update_sun)
    bpy.utils.register_class(TheBounty_OT_render_view)
    bpy.utils.register_class(TheBounty_OT_render_animation)
    bpy.utils.register_class(TheBounty_OT_render_still)
    bpy.utils.register_class(TheBounty_OT_presets_ior_list)
    bpy.utils.register_class(ThebountyParseIBL)
    

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_get_position)
    bpy.utils.unregister_class(OBJECT_OT_get_angle)
    bpy.utils.unregister_class(OBJECT_OT_update_sun)
    bpy.utils.unregister_class(TheBounty_OT_render_view)
    bpy.utils.unregister_class(TheBounty_OT_render_animation)
    bpy.utils.unregister_class(TheBounty_OT_render_still)
    bpy.utils.unregister_class(TheBounty_OT_presets_ior_list)
    bpy.utils.unregister_class(ThebountyParseIBL)

