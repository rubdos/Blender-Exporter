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

#include <Python.h>
#include <memory>

#include "magic.hpp"
#include "blender_scene.hpp"

#define APPLY_TYPE(x) VarPyObject x
#define APPLY_TYPES(...) FOR_EACH(APPLY_TYPE, __VA_ARGS__)
#define PY_METHOD(x, ...) inline PyObject * x(APPLY_TYPES(__VA_ARGS__)) \
{\
    return this->call_python_method(#x, VA_NUM_ARGS(__VA_ARGS__), __VA_ARGS__);\
}

#define PY_ATTRIBUTE(x) inline PyObject * get_ ## x () \
{\
    return PyObject_GetAttrString(self, #x);\
}

class render_engine
{
public:
    render_engine(PyObject *self);
    void update(PyObject *data, PyObject *scene);
    void render(PyObject *scene);
    virtual ~render_engine();

private:
    PyObject *self;

    std::unique_ptr<blender_scene> scene;

    // Python methods
    PyObject *call_python_method(const char *name, size_t count, ...);
    PY_METHOD(update_stats, stats, info);
    
    // Python attributes
    PY_ATTRIBUTE(is_preview)
};
