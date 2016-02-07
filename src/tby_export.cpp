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
#include <iostream>
#include <cstdarg>

#include "tby_export.hpp"
#include "blender_scene.hpp"

render_engine::render_engine(PyObject *self)
    : python_class(self)
{
}

render_engine::render_engine(const render_engine& other)
    : python_class(other)
{
    this->scene = std::unique_ptr<blender_scene>(new blender_scene(*other.scene));
}

render_engine &render_engine::operator=(const render_engine& other)
{
    python_class::operator=(other);
    this->scene = std::unique_ptr<blender_scene>(new blender_scene(*other.scene));
}

render_engine::~render_engine()
{
}

void render_engine::update(PyObject *data, PyObject *scene)
{
    Py_DECREF(update_stats("", "Setting up render"));
    this->scene = std::unique_ptr<blender_scene>(new blender_scene(scene));

    if(get_is_preview() == Py_True)
    {
        std::cout << "get_is_preview == True" << std::endl;
        this->scene->frame_set(this->scene->get_frame_current());
    }
}

void render_engine::render(PyObject *scene)
{
}
