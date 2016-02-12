/**
 *  Copyright 2016 Ruben De Smet
 *
 *  This program is free software; you can redistribute it and/or
 *  modify it under the terms of the GNU General Public License
 *  as published by the Free Software Foundation; either version 2
 *  of the License, or (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software Foundation,
 *  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
 */

#pragma once

// test
#ifndef __MINGW64__
#include <algorithm>
#endif
//>
#include <Python.h>

#include "python_class.hpp"
#include "blender_render_settings.hpp"
#include "blender_camera.hpp"
#include "blender_bounty.hpp"

class blender_scene : public python_class
{
public:
    blender_scene(PyObject *scene);
    blender_scene(const VarPyObject&);

    blender_scene(const blender_scene &); // Copy c'tor
    blender_scene &operator=(const blender_scene&); // Copy assignment

    void compute_scene_size(long &sizeX, long &sizeY);
    void get_render_coords(long &sizeX,
            long &sizeY,
            long &bStartX,
            long &bStartY,
            long &bsizeX,
            long &bsizeY,
            blender_camera * &cam_data); // void * as placeholder.

    PY_VOID_METHOD(frame_set, frame);

    PY_ATTRIBUTE(frame_current, long);
    PY_ATTRIBUTE(render, blender_render_settings);
    PY_ATTRIBUTE(bounty, blender_bounty);
    PY_ATTRIBUTE(frame_end, long);
};
