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

static PyObject *
tby_construct(PyObject *self, PyObject *args) {
    std::cout << "Hello world" << std::endl;
    return Py_BuildValue("i", 1);
}

static PyMethodDef tby_methods[] = {
    {"construct_render_engine", tby_construct, METH_VARARGS,
        "Construct the render_engine referenc"},
    {"destruct_render_engine", tby_construct, METH_VARARGS,
        "Destruct the render_engine referenc"},
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
