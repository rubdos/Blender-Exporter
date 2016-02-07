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

#include <Python.h>

#include "blender_scene.hpp"

blender_scene::blender_scene(PyObject *scene)
{
    this->scene = scene;
    Py_INCREF(scene);
}

blender_scene::blender_scene(const blender_scene& other) // Copy c'tor
{
    this->scene = other.scene;
    Py_INCREF(this->scene);
}

blender_scene & blender_scene::operator= (const blender_scene& other) // Copy assignment
{
    if(this != &other)
    {
        Py_DECREF(this->scene);
        this->scene = other.scene;
        Py_INCREF(this->scene);
    }
    return *this;
}

blender_scene::~blender_scene()
{
    Py_DECREF(scene);
}
