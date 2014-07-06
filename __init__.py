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

import sys
import os
import ctypes

PLUGIN_PATH = os.path.join(__path__[0], 'bin', 'plugins')
BIN_PATH = os.path.join(__path__[0], 'bin')
# allowed branchs..
#branchs=('master','volumegrid','merge_SSS')
EXP_BRANCH = (("master"),)

sys.path.append(BIN_PATH)

bl_info = {
    "name": "TheBounty",
    "description": "TheBounty Renderer for Blender (based on YafaRay Exporter)",
    "author": "Pedro Alcaide (povmaniaco)",
    "version": (0, 1, 6, 'Transitional'),
    "blender": (2, 7, 0),
    "location": "Info Header > Engine dropdown menu",
    "wiki_url": "https://github.com/TheBounty/Blender-Exporter/wiki",
    "tracker_url": "https://github.com/TheBounty/Blender-Exporter/issues",
    "category": "Render"
    }

# Loading order of the dlls is sensible, please do not alter it.
if sys.platform == 'win32':
    for file in os.listdir(BIN_PATH):
        # load dll's from a MSVC build's
        if file in {'yafaraycore.dll'}:
            dllArray = ['zlib1', 'iconv', 'zlib', 'libpng15', 'libxml2', 'yafaraycore', 'yafarayplugin']
            break
        # load dll's from a MinGW build's
        else:
            dllArray = ['zlib', 'libxml2-2', 'libgcc_s_sjlj-1', 'libHalf', 'libIex-2_1', 'libImath-2_1', \
                        'libIlmThread-2_1', 'libIlmImf-2_1', 'libjpeg-8', 'libpng14', 'libtiff-3', \
                        'libfreetype-6', 'libstdc++-6', 'libyafaraycore', 'libyafarayplugin']

elif sys.platform == 'darwin':
    dllArray = ['libyafaraycore.dylib', 'libyafarayplugin.dylib']
    
else: # linux
    dllArray = ['libyafaraycore.so', 'libyafarayplugin.so']
    # test
    for file in os.listdir(PLUGIN_PATH):
        if file in {'libGridVolume.so'}:
            EXP_BRANCH +=(("volumegrid"),)
        if file in {'libtranslucent.so'}:
            EXP_BRANCH +=(("merge_SSS"),)

for dll in dllArray:
    try:
        ctypes.cdll.LoadLibrary(os.path.join(BIN_PATH, dll))
    except Exception as e:
        print("ERROR: Failed to load library {0}, {1}".format(dll, repr(e)))


if "bpy" in locals():
    import imp
    imp.reload(prop)
    imp.reload(io)
    imp.reload(ui)
    imp.reload(ot)
else:
    import bpy
    from bpy.app.handlers import persistent
    from . import prop
    from . import io
    from . import ui
    from . import ot
# for nodes
import nodeitems_utils

@persistent
def load_handler(dummy):
    for tex in bpy.data.textures:
        if tex is not None:
            # set the correct texture type on file load....
            # converts old files, where propertie yaf_tex_type wasn't defined
            print("Load Handler: Convert old texture \"{0}\" with texture type: \"{1}\" to \"{2}\"".format(tex.name, tex.yaf_tex_type, tex.type))
            tex.yaf_tex_type = tex.type
    # convert image output file type setting from blender to yafaray's file type setting on file load, so that both are the same...
    if bpy.context.scene.render.image_settings.file_format is not bpy.context.scene.bounty.img_output:
        bpy.context.scene.bounty.img_output = bpy.context.scene.render.image_settings.file_format


def register():
    prop.register()
    bpy.utils.register_module(__name__)
    
    bpy.app.handlers.load_post.append(load_handler)
    # register keys for 'render 3d view', 'render still' and 'render animation'
    km = bpy.context.window_manager.keyconfigs.addon.keymaps.new(name='Screen')
    kmi = km.keymap_items.new('render.render_view', 'F12', 'PRESS', False, False, False, True)
    kmi = km.keymap_items.new('render.render_animation', 'F12', 'PRESS', False, False, True, False)
    kmi = km.keymap_items.new('render.render_still', 'F12', 'PRESS', False, False, False, False)
    
    for branch in EXP_BRANCH:
        if branch == "custom_nodes":
            nodeitems_utils.register_node_categories("TheBountyMaterial", ui.prop_custom_nodes.TheBountyNodeCategories)
    

def unregister():
    prop.unregister()
    
    # unregister keys for 'render 3d view', 'render still' and 'render animation'
    kma = bpy.context.window_manager.keyconfigs.addon.keymaps['Screen']
    for kmi in kma.keymap_items:
        #if kmi.idname == 'render.render_view' or kmi.idname == 'render.render_animation' or kmi.idname == 'render.render_still':
        if kmi.idname in {'render.render_view','render.render_animation','render.render_still'}:
            kma.keymap_items.remove(kmi)
    bpy.utils.unregister_module(__name__)
    bpy.app.handlers.load_post.remove(load_handler)
    
    for branch in EXP_BRANCH:
        if branch == "custom_nodes":
            nodeitems_utils.unregister_node_categories("TheBountyMaterial")


if __name__ == '__main__':
    register()
