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
#include "blender_render_settings.hpp"

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

    if(get_is_preview())
    {
        std::cout << "get_is_preview == True" << std::endl;
        Py_DECREF(this->scene->frame_set(this->scene->get_frame_current()));
    }

    blender_render_settings render = this->scene->get_render();
    std::string filePath = render.get_filepath();

    std::cout << "Filepath: " << filePath << std::endl;

    // TODO: Implement these.
    // filePath = bpy.path.abspath(render.filepath)
    // filePath = os.path.realpath(filePath)
    // filePath = os.path.normpath(filePath)

    // [self.sizeX, self.sizeY, self.bStartX, self.bStartY, self.bsizeX, self.bsizeY, camDummy] = tby_scene.getRenderCoords(scene)
    //
    
    if(render.get_use_border())
    {
        std::cout << "Using border" << std::endl;
    //     self.resX = self.bsizeX
    //     self.resY = self.bsizeY
    }
    else
    {
        std::cout << "Not using border" << std::endl;
    //     self.resX = self.sizeX
    //     self.resY = self.sizeY
    }
    // # render type setup
    // if scene.bounty.gs_type_render == "file":
    //     self.setInterface(yafrayinterface.yafrayInterface_t())
    //     self.yi.setInputGamma(scene.bounty.gs_gamma_input, scene.bounty.sc_apply_gammaInput)
    //     self.outputFile, self.output, self.file_type = self.decideOutputFileName(filePath, scene.bounty.img_output)
    //     self.yi.paramsClearAll()
    //     self.yi.paramsSetString("type", self.file_type)
    //     self.yi.paramsSetBool("alpha_channel", render.image_settings.color_mode == "RGBA")
    //     self.yi.paramsSetBool("z_channel", scene.bounty.gs_z_channel)
    //     self.yi.paramsSetInt("width", self.resX)
    //     self.yi.paramsSetInt("height", self.resY)
    //     self.ih = self.yi.createImageHandler("outFile")
    //     self.co = yafrayinterface.imageOutput_t(self.ih, str(self.outputFile), 0, 0)

    // elif scene.bounty.gs_type_render == "xml":
    //     self.setInterface(yafrayinterface.xmlInterface_t())
    //     self.yi.setInputGamma(scene.bounty.gs_gamma_input, scene.bounty.sc_apply_gammaInput)
    //     self.outputFile, self.output, self.file_type = self.decideOutputFileName(filePath, 'XML')
    //     self.yi.paramsClearAll()
    //     self.co = yafrayinterface.imageOutput_t()
    //     self.yi.setOutfile(self.outputFile)

    // else:
    //     self.setInterface(yafrayinterface.yafrayInterface_t())
    //     self.yi.setInputGamma(scene.bounty.gs_gamma_input, scene.bounty.sc_apply_gammaInput)

    // self.yi.startScene()
    // self.exportScene()# to above, line 92
    // self.lightIntegrator.exportIntegrator(self.scene.bounty) # lightIntegrator, line 26
    // self.lightIntegrator.exportVolumeIntegrator(self.scene)

    // # must be called last as the params from here will be used by render()
    // tby_scene.exportRenderSettings(self.yi, self.scene)
}

void render_engine::render(PyObject *scene)
{
}
