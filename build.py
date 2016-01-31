#!/usr/bin/env python3

# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# This script will build the native `io` library, which serves as
# a faster replacement for the Python `io` library.
# It uses cffipp for generating C++ bindings:
# https://gitlab.com/rubdos/cffipp
# pip3 install cffipp --user

from cffipp import FFIpp

def readfile(name):
    with open(name, 'r') as f:
        return f.read().decode()

def compile():
    parent_map = "native"
    sources = []
    export_headers = []

    ffi = FFIpp()
    sources = "\n".join(map(readfile, sources))
    export_headers = "\n".join(map(readfile, export_headers))
    ffi.cdef(export_headers)
    
    ffi.set_source("io", sources)
    ffi.compile()

if __name__ == "__main__":
    compile()
