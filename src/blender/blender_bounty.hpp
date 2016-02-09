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
#include <string>
#include "python_class.hpp"

class blender_bounty : public python_class
{
public:
    blender_bounty(PyObject *bounty);
    blender_bounty(const VarPyObject& bounty);

    blender_bounty(const blender_bounty &); // Copy c'tor
    blender_bounty &operator=(const blender_bounty&); // Copy assignment

    PY_ATTRIBUTE(gs_type_render, std::string);
};

