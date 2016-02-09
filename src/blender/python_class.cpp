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

#include "python_class.hpp"

python_class::python_class()
{
}

python_class::python_class(PyObject *_self)
{
    this->self = _self;
    Py_INCREF(self);
}

python_class::python_class(const python_class& other) //copy c'tor
{
    this->self = other.self;
    Py_INCREF(this->self);
}

python_class &python_class::operator=(const python_class& other) // Copy assignment
{
    if(this != &other)
    {
        Py_DECREF(this->self);
        this->self = other.self;
        Py_INCREF(this->self);
    }
    return *this;
}
python_class::~python_class()
{
    Py_DECREF(self);
}

PyObject *python_class::call_python_method(const char *method, size_t count, ...)
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
