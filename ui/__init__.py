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

from . import properties_yaf_render
from . import properties_yaf_camera
from . import properties_yaf_material
from . import properties_yaf_texture
from . import properties_yaf_world
from . import properties_yaf_strand
from . import properties_yaf_object
from . import properties_yaf_light

from . import prop_scene
from . import prop_render_layer

# test for custom nodes..
from .. import EXP_BRANCH
if EXP_BRANCH=="custom_nodes":
    from . import prop_custom_nodes

from bl_ui import properties_object as properties_object
for member in dir(properties_object):  # add all "object" panels from blender
    subclass = getattr(properties_object, member)
    try:
        subclass.COMPAT_ENGINES.add('THEBOUNTY')
    except:
        pass
del properties_object

from bl_ui import properties_particle as properties_particle
for member in dir(properties_particle):  # add all "particle" panels from blender
    subclass = getattr(properties_particle, member)
    try:
        subclass.COMPAT_ENGINES.add('THEBOUNTY')
    except:
        pass
del properties_particle

from bl_ui import properties_data_mesh as properties_data_mesh
for member in dir(properties_data_mesh):  # add all "object data" panels from blender
    subclass = getattr(properties_data_mesh, member)
    try:
        subclass.COMPAT_ENGINES.add('THEBOUNTY')
    except:
        pass
del properties_data_mesh

from bl_ui import properties_data_speaker as properties_data_speaker
for member in dir(properties_data_speaker):  # add all "speaker (SOC 2011, pepper branch)" panels from blender
    subclass = getattr(properties_data_speaker, member)
    try:
        subclass.COMPAT_ENGINES.add('THEBOUNTY')
    except:
        pass
del properties_data_speaker
