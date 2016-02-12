#  Copyright 2015 Pedro Alcaide
#  Copyright 2016 Ruben De Smet
#                 Pedro Alcaide
#
#  This file is part of TheBounty Renderer
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

import bpy
from .. import PLUGIN_PATH
import tby_blender

class TheBountyRenderEngine(bpy.types.RenderEngine):
    bl_idname = 'THEBOUNTY'
    bl_use_preview = True
    bl_label = "TheBounty Render"
    prog = 0.0
    tag = ""

    def __init__(self):
        self.backend = tby_blender.construct_render_engine(self)
        self.plugin_path = PLUGIN_PATH

    def __del__(self):
        if hasattr(self, 'backend'):
            tby_blender.destruct_render_engine(self.backend)

    def update(self, data, scene):
        tby_blender.render_engine_update(self.backend, data, scene)

    def render(self, scene):
        tby_blender.render_engine_render(self.backend, scene)
