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

render_engine::render_engine(PyObject *self)
{
    this->self = self;
    Py_INCREF(self);
}
render_engine::~render_engine()
{
    Py_DECREF(self);
}

void render_engine::update(PyObject *data, PyObject *scene)
{
    Py_DECREF(update_stats("", "Setting up render"));
}

void render_engine::render(PyObject *scene)
{
}

PyObject *render_engine::call_python_method(const char *method, size_t count, ...)
{
    PyObject *python_method = PyObject_GetAttrString(self, method);
    if(python_method == NULL)
    {
        std::cerr << "I have no attribute `" << method << "'" << std::endl;
        return Py_None;
    }
    if (!PyCallable_Check(python_method))
    {
        std::cerr << "Python method `" << method << "' not callable" << std::endl;
        return Py_None;
    }
    std::cout << "Calling underlying Python method `" << method << "'" << std::endl;

    va_list args;
    va_start(args, count);
    PyObject *method_args = PyTuple_New(count);
    for(size_t i = 0; i < count; ++i)
    {
        PyObject *o = va_arg(args, VarPyObject).get_PyObject();
        if(PyTuple_SetItem(method_args, i, o))
        {
            std::cerr << "Setting variable " << i << " of callback `" << method << "' failed" << std::endl;
        }
    }
    va_end(args);
    PyObject * result = PyObject_CallObject(python_method, method_args);
    Py_DECREF(method_args);
    Py_DECREF(python_method);
    return result;
}
