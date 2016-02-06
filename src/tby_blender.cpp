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

#include "tby_export.hpp"

static PyObject *
tby_construct(PyObject *self, PyObject *py_render_engine) {
    std::cout << "Constructing new render_engine" << std::endl;
    PyObject *result = NULL;
    render_engine *re = new render_engine(py_render_engine);
    return PyCapsule_New((void *)re, NULL, NULL);
}

static PyObject *
tby_destruct(PyObject *self, PyObject *arg) {
    std::cout << "Destructing render_engine" << std::endl;
    auto *re = (render_engine *) PyCapsule_GetPointer(arg, NULL);
    delete re;
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *
tby_update(PyObject *self, PyObject *args)
{
    PyObject *re_obj;
    PyObject *data;
    PyObject *scene;
    if(!PyArg_UnpackTuple(args, "tby_update", 3, 3, &re_obj, &data, &scene))
    {
        Py_INCREF(Py_None);
        return Py_None;
    }
    auto *re = (render_engine*) PyCapsule_GetPointer(re_obj, NULL);
    re->update(data, scene);
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *
tby_render(PyObject *self, PyObject *args)
{
    PyObject *re_obj;
    PyObject *scene;
    if(!PyArg_UnpackTuple(args, "tby_render", 2, 2, &re_obj, &scene))
    {
        Py_INCREF(Py_None);
        return Py_None;
    }
    auto *re = (render_engine*) PyCapsule_GetPointer(re_obj, NULL);
    re->render(scene);
    Py_INCREF(Py_None);
    return Py_None;
}

static PyMethodDef tby_methods[] = {
    {"construct_render_engine", tby_construct, METH_O,
        "Construct the render_engine reference"},
    {"destruct_render_engine", tby_destruct, METH_O,
        "Destruct the render_engine reference"},
    {"render_engine_update", tby_update, METH_VARARGS,
        "Update the render_engine."},
    {"render_engine_render", tby_render, METH_VARARGS,
        "Render, using the render_engine."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef tby_module = {
    PyModuleDef_HEAD_INIT,
    "tby_blender",   /* name of module */
    NULL,            /* module documentation, may be NULL */
    -1,              /* size of per-interpreter state of the module,
                        or -1 if the module keeps state in global variables. */
    tby_methods
};


PyMODINIT_FUNC
PyInit_tby_blender(void)
{
    PyObject *m;

    m = PyModule_Create(&tby_module);
    if (m == NULL)
        return NULL;

    return m;
}
