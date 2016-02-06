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
from .. import PLUGIN_PATH
from .tby_object import exportObject
from .tby_light  import exportLight
from .tby_world  import exportWorld
from .tby_integrator import exportIntegrator
from . import tby_scene
from .tby_texture import exportTexture
from .tby_material import TheBountyMaterialWrite
from bpy import context
from . import tby_blender

class TheBountyRenderEngine(bpy.types.RenderEngine):
    bl_idname = 'THEBOUNTY'
    bl_use_preview = True
    bl_label = "TheBounty Render"
    prog = 0.0
    tag = ""

    def __init__(self):
        self.backend = tby_blender.construct_render_engine(self)

    def __del__(self):
        if hasattr(self, 'backend'):
            tby_blender.destruct_render_engine(self.backend)

    def update(self, data, scene):
        tby_blender.render_engine_update(self.backend, data, scene)

    def render(self, scene):
        tby_blender.render_engine_render(self.backend, scene)
