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

#include <interface/xmlinterface.h>

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
    update_stats("", "Setting up render");
    this->scene = std::unique_ptr<blender_scene>(new blender_scene(scene));

    if(get_is_preview())
    {
        std::cout << "get_is_preview == True" << std::endl;
        this->scene->frame_set(this->scene->get_frame_current());
    }

    blender_render_settings render = this->scene->get_render();
    std::string filePath = render.get_filepath();

    std::cout << "Filepath: " << filePath << std::endl;

    // TODO: Implement these.
    // filePath = bpy.path.abspath(render.filepath)
    // filePath = os.path.realpath(filePath)
    // filePath = os.path.normpath(filePath)
    
    blender_camera *camDummy; // Placeholder
    this->scene->get_render_coords(sizeX, sizeY, bStartX, bStartY, bsizeX, bsizeY, camDummy);
    delete camDummy;
    
    if(render.get_use_border())
    {
        std::cout << "Using border" << std::endl;
        resX = bsizeX;
        resY = bsizeY;
    }
    else
    {
        std::cout << "Not using border" << std::endl;
        resX = sizeX;
        resY = sizeY;
    }

    // render type setup
    std::string type_render = this->scene->get_bounty().get_gs_type_render();
    std::cout << "Rendering to " << type_render << std::endl;
    if(type_render == "file")
    {
        set_interface(new yafaray::yafrayInterface_t());
        interface->setInputGamma(this->scene->get_bounty().get_gs_gamma_input(),
                this->scene->get_bounty().get_sc_apply_gammaInput());
    //     self.outputFile, self.output, self.file_type = self.decideOutputFileName(filePath, scene.bounty.img_output)
        interface->paramsClearAll();
        interface->paramsSetString("type", get_file_type().c_str());
        //interface->paramsSetBool("alpha_channel",
        //    render.image_settings.color_mode == "RGBA");
        interface->paramsSetBool("z_channel",
                this->scene->get_bounty().get_gz_z_channel());
        interface->paramsSetInt("width", resX);
        interface->paramsSetInt("height", resY);
    //     self.ih = self.yi.createImageHandler("outFile")
    //     self.co = yafrayinterface.imageOutput_t(self.ih, str(self.outputFile), 0, 0)

    }
    else if (type_render == "xml")
    {
        set_interface(new yafaray::xmlInterface_t());
        interface->setInputGamma(this->scene->get_bounty().get_gs_gamma_input(),
                this->scene->get_bounty().get_sc_apply_gammaInput());
    //     self.outputFile, self.output, self.file_type = self.decideOutputFileName(filePath, 'XML')
        interface->paramsClearAll();
    //     self.co = yafrayinterface.imageOutput_t()
    //     self.yi.setOutfile(self.outputFile)

    }
    else
    {
        set_interface(new yafaray::yafrayInterface_t());
        interface->setInputGamma(this->scene->get_bounty().get_gs_gamma_input(),
                this->scene->get_bounty().get_sc_apply_gammaInput());
    }

    interface->startScene();
    // self.exportScene()# to above, line 92
    // self.lightIntegrator.exportIntegrator(self.scene.bounty) # lightIntegrator, line 26
    // self.lightIntegrator.exportVolumeIntegrator(self.scene)

    // Must be called last as the params from here will be used by render()
    // tby_scene.exportRenderSettings(self.yi, self.scene)
    this->export_render_settings();
}

void render_engine::export_render_settings()
{
    interface->printInfo("Exporting Render Settings");

    auto render = scene->get_render();
    auto bounty = scene->get_bounty();

    long sizeX;
    long sizeY;
    long bStartX;
    long bStartY;
    long bsizeX;
    long bsizeY;
    long resX;
    long resY;

    blender_camera *cam_data;

    this->scene->get_render_coords(sizeX, sizeY,
            bStartX, bStartY,
            bsizeX, bsizeY,
            cam_data);

    interface->paramsSetString("camera_name", "cam");
    interface->paramsSetString("integrator_name", "default");
    interface->paramsSetString("volintegrator_name", "volintegr");

    // Gamma output
    interface->paramsSetFloat("gamma", bounty.get_gs_gamma());
    // TODO: AA
    // exportAA(yi, scene)

    interface->paramsSetInt("xstart", bStartX);
    interface->paramsSetInt("ystart", bStartY);

    // no border when rendering to view
    if(render.get_use_border() and cam_data)
    {
        interface->paramsSetInt("width", bsizeX);
        interface->paramsSetInt("height", bsizeY);
    }
    else
    {
        interface->paramsSetInt("width", sizeX);
        interface->paramsSetInt("height", sizeY);
    }

    interface->paramsSetBool("clamp_rgb", bounty.get_gs_clamp_rgb());
    interface->paramsSetBool("show_sam_pix", bounty.get_gs_show_sam_pix());
    // TODO: review
    interface->paramsSetBool("premult", false);

    // TODO: automatic best size mode calculation based on render size
    interface->paramsSetInt("tile_size", bounty.get_gs_tile_size());
    interface->paramsSetString("tiles_order",
            bounty.get_gs_tile_order().c_str());

    interface->paramsSetBool("z_channel", bounty.get_gs_z_channel());

    if(bounty.get_gs_type_render() == "into_blender")
    {
        interface->paramsSetBool("normalize_z_channel", false);
    }

    interface->paramsSetBool("drawParams", bounty.get_gs_draw_params());
    interface->paramsSetString("customString",
            bounty.get_gs_custom_string().c_str());

    // by default is -1, for use all allowed threads
    int threads = -1;
    if(bounty.get_gs_threads() > 0)
        threads = bounty.get_gs_threads();
    interface->paramsSetInt("threads", threads);

    interface->paramsSetString("background_name", "world_background");
}

void render_engine::set_interface(yafaray::yafrayInterface_t *yi)
{
    this->interface = std::unique_ptr<yafaray::yafrayInterface_t>(yi);
    //self.materialMap = {}
    //self.exportedMaterials = set()
    //self.yi = yi
    //# setup specific values for render preview mode
    if(get_is_preview())
    {
    //    self.yi.setVerbosityWarning()
    //    #to correct alpha problems in preview roughglass
    //    self.scene.bounty.bg_transp = False
    //    self.scene.bounty.bg_transp_refract = False
    }
    else
    {
    //    self.verbositylevel(self.scene.bounty.gs_verbosity_level)
    }
}

void render_engine::render(PyObject *scene)
{
}
