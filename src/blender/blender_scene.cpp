/**
 *  Copyright 2016 Ruben De Smet
 *                 Pedro Alcaide
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

#include <Python.h>
#include <iostream>

#include "blender_scene.hpp"
#include "blender_camera.hpp"

blender_scene::blender_scene(PyObject *scene)
    : python_class(scene)
{
}

blender_scene::blender_scene(const VarPyObject& scene)
    : python_class((PyObject *)scene)
{
}

blender_scene::blender_scene(const blender_scene& other) // Copy c'tor
    : python_class(other)
{
}

blender_scene & blender_scene::operator= (const blender_scene& other) // Copy assignment
{
    python_class::operator=(other);
    return *this;
}

void blender_scene::compute_scene_size(long &sizeX, long &sizeY)
{
    auto render = get_render();
    sizeX = (render.get_resolution_x() * render.get_resolution_percentage())/100;
    sizeY = (render.get_resolution_y() * render.get_resolution_percentage())/100;
}

void blender_scene::get_render_coords(long &sizeX,
        long &sizeY,
        long &bStartX,
        long &bStartY,
        long &bsizeX,
        long &bsizeY,
        blender_camera * &cam_data)
{
    auto render_settings = this->get_render();
    compute_scene_size(sizeX, sizeY);

    bStartX = 0;
    bStartY = 0;
    bsizeX = 0;
    bsizeY = 0;

    cam_data = nullptr;

    // if scene.objects:
    //     for item in scene.objects:
    //         if item.type == 'CAMERA':
    //             cam_data = item.data
    //             break

    //  Shift only available if camera is selected
    // if not cam_data:
    long shiftX = 0;
    long shiftY = 0;

    if(cam_data != nullptr)
    {
         long maxsize = std::max(sizeX, sizeY);
         shiftX = cam_data->get_shift_x() * maxsize;
         shiftY = cam_data->get_shift_y() * maxsize;
    }

    // # no border when rendering to view
    if((cam_data != nullptr) && render_settings.get_use_border())
    {
         long minX = render_settings.get_border_min_x() * sizeX;
         long minY = render_settings.get_border_min_y() * sizeY;
         long maxX = render_settings.get_border_max_x() * sizeX;
         long maxY = render_settings.get_border_max_y() * sizeY;
         bStartX = minX;
         bStartY = sizeY - maxY;
         bsizeX = maxX - minX;
         bsizeY = maxY - minY;
    }

    bStartX += shiftX;
    bStartY -= shiftY;
}
