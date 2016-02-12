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
#include <string>

#include "blender_image_settings.hpp"

blender_image_settings::blender_image_settings(PyObject *image_settings)
    : python_class(image_settings)
{
}

blender_image_settings::blender_image_settings(const VarPyObject& image_settings)
    : python_class((PyObject *)image_settings)
{
}

blender_image_settings::blender_image_settings(const blender_image_settings& other) // Copy c'tor
    : python_class(other)
{
}

blender_image_settings & blender_image_settings::operator= (const blender_image_settings& other) // Copy assignment
{
    python_class::operator=(other);
    return *this;
}

