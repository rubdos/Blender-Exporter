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

#include <interface/yafrayinterface.h>

#include "python_class.hpp"
#include "blender_scene.hpp"

class render_engine : public python_class
{
public:
    render_engine(PyObject *self);
    render_engine(const render_engine&);
    render_engine &operator=(const render_engine& other);
    void update(PyObject *data, PyObject *scene);
    void render(PyObject *scene);
    virtual ~render_engine();

private:
    std::unique_ptr<blender_scene> scene;
    std::unique_ptr<yafaray::yafrayInterface_t> interface;

    void set_interface(yafaray::yafrayInterface_t *yi);

    // Python methods
    PY_VOID_METHOD(update_stats, stats, info);
    
    // Python attributes
    PY_ATTRIBUTE(is_preview, bool)

    long sizeX;
    long sizeY;
    long bStartX;
    long bStartY;
    long bsizeX;
    long bsizeY;
    long resX;
    long resY;
};
