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
import os
import threading
import time
import yafrayinterface

from thebounty import PLUGIN_PATH
from .yaf_object import yafObject
from .yaf_light  import yafLight
from .yaf_world  import yafWorld
from .yaf_integrator import yafIntegrator
from . import yaf_scene
from .yaf_texture import yafTexture
from .yaf_material import TheBountyMaterialWrite

switchFileType = {
    'PNG': 'png',
    'TARGA': 'tga',
    'TIFF': 'tif',
    'JPEG': 'jpg',
    'HDR': 'hdr',
    'OPEN_EXR': 'exr',
    'XML': 'xml',
}

class YafaRayRenderEngine(bpy.types.RenderEngine):
    bl_idname = 'THEBOUNTY'
    bl_use_preview = True
    bl_label = "TheBounty Render"
    prog = 0.0
    tag = ""
    useViewToRender = False
    viewMatrix = None
    sceneMat = []
    
    # TODO: make more options from UI
    def verbositylevel(self, level):
        if level =='info':
            self.yi.setVerbosityInfo()
        else:
            self.yi.setVerbosityMute()   
    
    ##-----------------------------------------------------     

    def setInterface(self, yi):
        self.materialMap = {}
        self.materials = set()
        self.yi = yi
        # setup specific values for render preview mode
        if self.is_preview:
            self.yi.setVerbosityMute()
            self.scene.bounty.bg_transp = False         #to correct alpha problems in preview roughglass
            self.scene.bounty.bg_transp_refract = False #to correct alpha problems in preview roughglass
        else:
            self.verbositylevel('info')
        
        # export go.. load plugins
        self.yi.loadPlugins(PLUGIN_PATH)
                
        # process geometry
        self.yaf_object = yafObject(self.yi, self.materialMap, self.is_preview)
             
        # process lights
        self.yaf_lamp = yafLight(self.yi, self.is_preview)
              
        # process environment world
        self.yaf_world = yafWorld(self.yi)
              
        # process lighting integrators..
        self.yaf_integrator = yafIntegrator(self.yi)
              
        # textures before materials
        self.yaf_texture = yafTexture(self.yi)
             
        # and materials
        self.yaf_material = TheBountyMaterialWrite(self.yi, self.materialMap, self.yaf_texture.loadedTextures)

    def exportScene(self):
        #
        for obj in self.scene.objects:
            self.exportTexture(obj)
            
        self.exportMaterials()
        self.yaf_object.setScene(self.scene)
        self.exportObjects()
        self.yaf_object.createCamera()
        self.yaf_world.exportWorld(self.scene)

    def exportTexture(self, obj):
        # First export the textures of the materials type 'blend'
        for mat_slot in [m for m in obj.material_slots if m.material is not None]:#.bounty is not None]:
            if mat_slot.material.bounty.mat_type == 'blend':
                try:
                    mat1 = bpy.data.materials[mat_slot.material.bounty.blendmaterial1]
                    mat2 = bpy.data.materials[mat_slot.material.bounty.blendmaterial2]
                except:
                    self.yi.printWarning("Exporter: Problem with blend material {0}."
                                         " Could not find one of the two blended materials".format(mat_slot.material.name))
                    continue
                for blendMat in [mat1, mat2]:
                    for blendTex in [bt for bt in blendMat.texture_slots if (bt and bt.texture and bt.use)]:
                        if self.is_preview and blendTex.texture.name == 'fakeshadow':
                            continue
                        self.yaf_texture.writeTexture(self.scene, blendTex.texture)
            else:
                continue
        #
        for mat_slot in [m for m in obj.material_slots if m.material is not None]:
            for tex in [t for t in mat_slot.material.texture_slots if (t and t.texture and t.use)]:
                if self.is_preview and tex.texture.name == "fakeshadow":
                    continue
                self.yaf_texture.writeTexture(self.scene, tex.texture)

    def object_on_visible_layer(self, obj):
        obj_visible = False
        for layer_visible in [object_layers and scene_layers for object_layers, scene_layers in zip(obj.layers, self.scene.layers)]:
            obj_visible |= layer_visible
        return obj_visible

    def exportObjects(self):
        self.yi.printInfo("Exporter: Processing Lamps...")

        #---------------------------
        # export only visible lamps
        #---------------------------
        for obj in [o for o in self.scene.objects if not o.hide_render and o.is_visible(self.scene) and o.type == 'LAMP']:
            if obj.is_duplicator:
                obj.create_dupli_list(self.scene)
                for obj_dupli in obj.dupli_list:
                    matrix = obj_dupli.matrix.copy()
                    self.yaf_lamp.createLight(self.yi, obj_dupli.object, matrix)

                if obj.dupli_list:
                    obj.free_dupli_list()
            else:
                if obj.parent and obj.parent.is_duplicator:
                    continue
                self.yaf_lamp.createLight(self.yi, obj, obj.matrix_world)

        self.yi.printInfo("Exporter: Processing Geometry...")

        # export only visible objects
        baseIds = {}
        dupBaseIds = {}

        for obj in [o for o in self.scene.objects if not o.hide_render and (o.is_visible(self.scene) or o.hide) \
        and self.object_on_visible_layer(o) and (o.type in {'MESH', 'SURFACE', 'CURVE', 'FONT', 'EMPTY'})]:
            # Exporting dupliObjects as instances, also check for dupliObject type 'EMPTY' and don't export them as geometry
            if obj.is_duplicator:
                self.yi.printInfo("Processing duplis for: {0}".format(obj.name))
                obj.dupli_list_create(self.scene)

                for obj_dupli in [od for od in obj.dupli_list if not od.object.type == 'EMPTY']:
                    self.exportTexture(obj_dupli.object)
                    for mat_slot in obj_dupli.object.material_slots:
                        if mat_slot.material not in self.materials:
                            self.exportMaterial(mat_slot.material)

                    if not self.scene.render.use_instances:
                        matrix = obj_dupli.matrix.copy()
                        self.yaf_object.writeMesh(obj_dupli.object, matrix)
                    else:
                        if obj_dupli.object.name not in dupBaseIds:
                            dupBaseIds[obj_dupli.object.name] = self.yaf_object.writeInstanceBase(obj_dupli.object)
                        matrix = obj_dupli.matrix.copy()
                        self.yaf_object.writeInstance(dupBaseIds[obj_dupli.object.name], matrix, obj_dupli.object.name)

                if obj.dupli_list is not None:
                    obj.dupli_list_clear()

                # check if object has particle system and uses the option for 'render emitter'
                if hasattr(obj, 'particle_systems'):
                    for pSys in obj.particle_systems:
                        check_rendertype = pSys.settings.render_type in {'OBJECT', 'GROUP'}
                        if check_rendertype and pSys.settings.use_render_emitter:
                            matrix = obj.matrix_world.copy()
                            self.yaf_object.writeMesh(obj, matrix)

            # no need to write empty object from here on, so continue with next object in loop
            elif obj.type == 'EMPTY':
                continue

            # Exporting objects with shared mesh data blocks as instances
            elif obj.data.users > 1 and self.scene.render.use_instances:
                self.yi.printInfo("Processing shared mesh data node object: {0}".format(obj.name))
                if obj.data.name not in baseIds:
                    baseIds[obj.data.name] = self.yaf_object.writeInstanceBase(obj)

                if obj.name not in dupBaseIds:
                    matrix = obj.matrix_world.copy()
                    self.yaf_object.writeInstance(baseIds[obj.data.name], matrix, obj.data.name)

            elif obj.data.name not in baseIds and obj.name not in dupBaseIds:
                self.yaf_object.writeObject(obj)

    def handleBlendMat(self, mat):
        #
        try:
            mat1 = bpy.data.materials[mat.bounty.blendmaterial1]
            mat2 = bpy.data.materials[mat.bounty.blendmaterial2]
        except:
            self.yi.printWarning("Exporter: Problem with blend material {0}. Could not find one of the two blended materials".format(mat.name))
            return
            
        if mat1.name == mat2.name:
            self.yi.printWarning("Exporter: Problem with blend material {0}. {1} and {2} to blend are the same materials".format(mat.name, mat1.name, mat2.name))
            return
        #----------------------------------------------------------------
        # This is not needed atm because 'blend' materials are excluded 
        # themselves from list. Recursive blend materials aren't allowed. 
        # Now Property sync method is excluded
        #----------------------------------------------------------------
        
        #if mat1.bounty.mat_type == 'blend':
        #    self.handleBlendMat(mat1)        
        if mat1 not in self.materials:
            self.materials.add(mat1)
            self.yaf_material.writeMaterial(mat1)

        #if mat2.bounty.mat_type == 'blend':
        #    self.handleBlendMat(mat2)
        if mat2 not in self.materials:
            self.materials.add(mat2)
            self.yaf_material.writeMaterial(mat2)

        if mat not in self.materials:
            self.materials.add(mat)
            self.yaf_material.writeMaterial(mat)

    def exportMaterials(self):
        self.yi.printInfo("Exporter: Processing Materials...")
        self.materials = set()

        # create a default shiny diffuse material -> it will be assigned, if object has no material(s)
        self.yi.paramsClearAll()
        self.yi.paramsSetString("type", "shinydiffusemat")
        self.yi.paramsSetColor("color", 0.8, 0.8, 0.8)
        self.yi.printInfo("Exporter: Creating Material \"defaultMat\"")
        ymat = self.yi.createMaterial("defaultMat")
        self.materialMap["default"] = ymat
        #--------------------------------------------------
        # create a shinydiffuse material for "Clay Render"
        # exception: don't create for material preview mode
        #--------------------------------------------------
        if not self.is_preview:
            self.yi.paramsClearAll()
            self.yi.paramsSetString("type", "shinydiffusemat")
            cCol = self.scene.bounty.gs_clay_col
            self.yi.paramsSetColor("color", cCol[0], cCol[1], cCol[2])
            self.yi.printInfo("Exporter: Creating Material \"clayMat\"")
            cmat = self.yi.createMaterial("clayMat")
            self.materialMap["clay"] = cmat
        #---------------------------------------------
        # override all materials in 'clay render' mode
        #---------------------------------------------
        for obj in [o for o in self.scene.objects if not self.scene.bounty.gs_clay_render]:
            for mat_slot in obj.material_slots:
                if mat_slot.material not in self.materials:
                    self.exportMaterial(mat_slot.material)

    def exportMaterial(self, material):
        if material:
            # must make sure all materials used by a blend mat
            # are written before the blend mat itself                
            if material.bounty.mat_type == 'blend':
                self.handleBlendMat(material)
            else:
                self.materials.add(material)
                self.yaf_material.writeMaterial(material, self.is_preview)

    def decideOutputFileName(self, output_path, filetype):
                
        filetype = switchFileType.get(filetype, 'png')
        # write image or XML-File with filename from framenumber
        frame_numb_str = "{:0" + str(len(str(self.scene.frame_end))) + "d}"
        output = os.path.join(output_path, frame_numb_str.format(self.scene.frame_current))
        # try to create dir if it not exists...
        if not os.path.exists(output_path):
            try:
                os.makedirs(output_path)
            except:
                print("Unable to create directory...")
                import traceback
                traceback.print_exc()
                output = ""
        outputFile = output + "." + filetype

        return outputFile, output, filetype

    
    def update(self, data, scene):
        # callback to export the scene
        self.update_stats("", "Setting up render")
        if not self.is_preview:
            scene.frame_set(scene.frame_current)

        self.scene = scene
        render = scene.render

        filePath = bpy.path.abspath(render.filepath)
        filePath = os.path.realpath(filePath)
        filePath = os.path.normpath(filePath)

        [self.sizeX, self.sizeY, self.bStartX, self.bStartY, self.bsizeX, self.bsizeY, camDummy] = yaf_scene.getRenderCoords(scene)

        if render.use_border:
            self.resX = self.bsizeX
            self.resY = self.bsizeY
        else:
            self.resX = self.sizeX
            self.resY = self.sizeY
        # render type setup
        if scene.bounty.gs_type_render == "file":
            self.setInterface(yafrayinterface.yafrayInterface_t())
            self.yi.setInputGamma(scene.bounty.gs_gamma_input, scene.bounty.sc_apply_gammaInput)
            self.outputFile, self.output, self.file_type = self.decideOutputFileName(filePath, scene.bounty.img_output)
            self.yi.paramsClearAll()
            self.yi.paramsSetString("type", self.file_type)
            self.yi.paramsSetBool("alpha_channel", render.image_settings.color_mode == "RGBA")
            self.yi.paramsSetBool("z_channel", scene.bounty.gs_z_channel)
            self.yi.paramsSetInt("width", self.resX)
            self.yi.paramsSetInt("height", self.resY)
            self.ih = self.yi.createImageHandler("outFile")
            self.co = yafrayinterface.imageOutput_t(self.ih, str(self.outputFile), 0, 0)

        elif scene.bounty.gs_type_render == "xml":
            self.setInterface(yafrayinterface.xmlInterface_t())
            self.yi.setInputGamma(scene.bounty.gs_gamma_input, scene.bounty.sc_apply_gammaInput)
            self.outputFile, self.output, self.file_type = self.decideOutputFileName(filePath, 'XML')
            self.yi.paramsClearAll()
            self.co = yafrayinterface.imageOutput_t()
            self.yi.setOutfile(self.outputFile)

        else:
            #
            self.setInterface(yafrayinterface.yafrayInterface_t()) # to line 68
            self.yi.setInputGamma(scene.bounty.gs_gamma_input, scene.bounty.sc_apply_gammaInput)
        
        #.. process scene
        self.yi.startScene()
        self.exportScene()# to above, line 92
        self.yaf_integrator.exportIntegrator(self.scene.bounty) # yaf_integrator, line 26
        self.yaf_integrator.exportVolumeIntegrator(self.scene)

        # must be called last as the params from here will be used by render()
        yaf_scene.exportRenderSettings(self.yi, self.scene)

    def render_preview(self, scene):
        # callback to render scene
        self.is_preview = True
        #scene = scene.bounty
        self.bl_use_postprocess = False
        #
        
        def progressCallback(command, *args):
            #
            if not self.test_break():
                if command == "tag":
                    self.tag = args[0]
                elif command == "progress":
                    self.prog = args[0]
                self.update_stats("TheBounty Render: ", "{0}".format(self.tag))
                #
                self.update_progress(self.prog)
        
        def drawAreaCallback(*args):
            x, y, w, h, tile = args
            res = self.begin_result(x, y, w, h)
            try:
                lay = res.layers[0]
                lay.rect, lay.passes[0].rect = tile
            except:
                pass

            self.end_result(res)

        def flushCallback(*args):
            w, h, tile = args
            res = self.begin_result(0, 0, w, h)
            try:
                lay = res.layers[0]
                lay.rect, lay.passes[0].rect = tile
            except BaseException as e:
                pass

            self.end_result(res)
                
        # define thread
        thread = threading.Thread(target = self.yi.render, 
                                  args=(self.resX, self.resY, 
                                        self.bStartX, self.bStartY, 
                                        self.is_preview, drawAreaCallback, 
                                        flushCallback, progressCallback))

        # run..
        thread.start()
    
        #while thread.isAlive() and not self.test_break():
        while thread.is_alive() and not self.test_break():
            time.sleep(0.5) #2)
            
        #if thread.isAlive():
        if thread.is_alive():
            self.update_stats("", "Aborting...")
            self.yi.abort()
            thread.join()
    
        self.yi.clearAll()
        del self.yi
        self.update_stats("", "Done!")
        self.bl_use_postprocess = True
    
    def render_scene(self, scene):
        # callback to render scene
        self.is_preview = False
        scene = scene.bounty
        # test for keep postprocess state
        postprocess = self.bl_use_postprocess
        #
        if self.bl_use_postprocess:
            self.bl_use_postprocess = False        

        if scene.gs_type_render == "file":
            self.yi.printInfo("Exporter: Rendering to file {0}".format(self.outputFile))
            
            self.yi.render(self.co)
            result = self.begin_result(0, 0, self.resX, self.resY)
            lay = result.layers[0]

            # exr format has z-buffer included, so no need to load '_zbuffer' - file
            if scene.gs_z_channel and not scene.img_output == 'OPEN_EXR':
                lay.load_from_file("{0}_zbuffer.{1}".format(self.output, self.file_type))
            else:
                lay.load_from_file(self.outputFile)
            self.end_result(result)

        elif scene.gs_type_render == "xml":
            self.yi.printInfo("Exporter: Writing XML to file {0}".format(self.outputFile))
            self.yi.render(self.co)

        else:

            def progressCallback(command, *args):
                if not self.test_break():
                    if command == "tag":
                        self.tag = args[0]
                    elif command == "progress":
                        self.prog = args[0]
                    self.update_stats("TheBounty Render: ", "{0}".format(self.tag))
                    #
                    self.update_progress(self.prog)

            def drawAreaCallback(*args):
                x, y, w, h, tile = args
                res = self.begin_result(x, y, w, h)
                try:
                    lay = res.layers[0]
                    lay.rect, lay.passes[0].rect = tile
                except:
                    pass

                self.end_result(res)

            def flushCallback(*args):
                w, h, tile = args
                res = self.begin_result(0, 0, w, h)
                try:
                    lay = res.layers[0]
                    lay.rect, lay.passes[0].rect = tile
                except BaseException as e:
                    pass

                self.end_result(res)
                
            # define thread
            thread = threading.Thread(target=self.yi.render,
                                 args=(self.resX, self.resY,
                                       self.bStartX, self.bStartY,
                                       self.is_preview,
                                       drawAreaCallback,
                                       flushCallback,
                                       progressCallback)
                                 )
            # run..
            thread.start()

            while thread.isAlive() and not self.test_break():
                time.sleep(0.2)

            if thread.isAlive():
                self.update_stats("", "Aborting...")
                self.yi.abort()
                thread.join()
        #
        self.yi.clearAll()
        del self.yi
        self.update_stats("", "Done!")
        self.bl_use_postprocess = postprocess #True

    def render(self, scene):
        #
        if not scene.name == 'preview':
            self.render_scene(scene)
        else:
            self.render_preview(scene)
