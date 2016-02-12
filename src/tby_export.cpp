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
#include <sstream>
#include <iomanip>

#ifdef _MSC_VER
#include <direct.h>
#endif

#include <interface/xmlinterface.h>

#include "tby_export.hpp"
#include "blender_scene.hpp"
#include "blender_render_settings.hpp"

render_engine::render_engine(PyObject *self)
    : python_class(self), is_preview(false)
{
}

void render_engine::update(PyObject *data, PyObject *scene)
{
#ifdef _MSC_VER
    //update_stats("Setting up render");
#else
	//update_stats("", "Setting up render");
#endif
    this->scene = std::unique_ptr<blender_scene>(new blender_scene(scene));

    if(is_preview)
    {
        std::cout << "is_preview == True" << std::endl;
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

    auto bounty = this->scene->get_bounty();

    // render type setup
    std::string type_render = bounty.get_gs_type_render();
    std::cout << "Rendering to " << type_render << std::endl;
    if(type_render == "file")
    {
        set_interface(new yafaray::yafrayInterface_t());
        interface->setInputGamma(this->scene->get_bounty().get_gs_gamma_input(),
                this->scene->get_bounty().get_sc_apply_gammaInput());
        decide_output_file_name(filePath, bounty.get_img_output());
        interface->paramsClearAll();
        interface->paramsSetString("type", file_type.c_str());
        interface->paramsSetBool("alpha_channel",
            render.get_image_settings().get_color_mode() == "RGBA");
        interface->paramsSetBool("z_channel",
                this->scene->get_bounty().get_gs_z_channel());
        interface->paramsSetInt("width", resX);
        interface->paramsSetInt("height", resY);
        image_handler = std::unique_ptr<yafaray::imageHandler_t>(
                interface->createImageHandler("outFile"));
        image_output = std::unique_ptr<yafaray::imageOutput_t>(
                new yafaray::imageOutput_t(image_handler.get(),
                    output_file.c_str(), 0, 0));

    }
    else if (type_render == "xml")
    {
        set_interface(new yafaray::xmlInterface_t());
        interface->setInputGamma(this->scene->get_bounty().get_gs_gamma_input(),
                this->scene->get_bounty().get_sc_apply_gammaInput());
        decide_output_file_name(filePath, "XML");
        interface->paramsClearAll();
        image_output = std::unique_ptr<yafaray::imageOutput_t>(
                new yafaray::imageOutput_t());
        ((yafaray::xmlInterface_t *)interface.get())->setOutfile(
            output_file.c_str());
    }
    else
    {
        set_interface(new yafaray::yafrayInterface_t());
        interface->setInputGamma(this->scene->get_bounty().get_gs_gamma_input(),
                this->scene->get_bounty().get_sc_apply_gammaInput());
    }

    interface->startScene();
    export_scene();
    // self.lightIntegrator.exportIntegrator(self.scene.bounty) # lightIntegrator, line 26
    // self.lightIntegrator.exportVolumeIntegrator(self.scene)

    // Must be called last as the params from here will be used by render()
    this->export_render_settings();
}

static std::map<std::string, std::string>
switchFileType = {
    {"PNG", "png"},
    {"TARGA", "tga"},
    {"TIFF", "tif"},
    {"JPEG", "jpg"},
    {"HDR", "hdr"},
    {"OPEN_EXR", "exr"},
    {"XML", "xml"}
};

void make_directory(const char* name)
{
#ifdef __linux__
    mkdir(name, 777);
#else
    mkdir(name);
#endif
}

void render_engine::decide_output_file_name(
        std::string output_path,
        std::string file_type)
{
    this->file_type = file_type = switchFileType[file_type];
    if(file_type == "") // Fallback
    {
        this->file_type = file_type = "png";
    }

    // write image or XML-File with filename from framenumber

    std::stringstream output;
    output << scene->get_frame_end();

    int width = output.str().length();
    output.str( std::string() );
    output.clear();
    output << output_path;
    if(output_path[output_path.length() - 1] != directory_separator[0])
    {
         output << directory_separator;
    }
    output << std::setw(width) << std::setfill('0') <<
        scene->get_frame_current();

    // Create dir if it not exists...
    make_directory(output_path.c_str());

    this->output = output.str();
    output << "." << file_type;
    this->output_file = output.str();

    std::cout << "outputFile: " << this->output_file << std::endl
        << "output: " << this->output << std::endl
        << "filetype: " << this->file_type << std::endl;
}

void render_engine::export_scene()
{
    for(auto obj: scene->get_objects())
    {
        std::cout << obj.get_type() << std::endl;
        this->export_texture(obj);
    }
    // for obj in self.scene.objects:
    //     self.exportTexture(obj)
    //     
    // self.exportMaterials()
    // self.geometry.setScene(self.scene)
    // self.exportObjects()
    // self.geometry.createCamera()
    // self.environment.setEnvironment(self.scene)
}

void render_engine::export_texture(const blender_object& obj)
{

    // return outputFile, output, filetype
    // self.outputFile, self.output, self.file_type = self.decideOutputFileName(filePath, 'foo')
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
    if(render.get_use_border() && cam_data)
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
    // setup specific values for render preview mode
    if(is_preview)
    {
        interface->setVerbosityWarning();
        // to correct alpha problems in preview roughglass
    //    self.scene.bounty.bg_transp = False
    //    self.scene.bounty.bg_transp_refract = False
    }
    else
    {
        verbosity_level();
    }

    this->interface->loadPlugins(get_plugin_path().c_str());

    // # process geometry
    // self.geometry = exportObject(self.yi, self.materialMap, self.is_preview)
    //      
    // # process lights
    // self.lights = exportLight(self.yi, self.is_preview)
    //       
    // # process environment world
    // self.environment = exportWorld(self.yi)
    //       
    // # process lighting integrators..
    // self.lightIntegrator = exportIntegrator(self.yi, self.is_preview)
    //       
    // # textures before materials
    // self.yaf_texture = exportTexture(self.yi)
    //      
    // # and materials
    // self.setMaterial = TheBountyMaterialWrite(self.yi, self.materialMap, self.yaf_texture.loadedTextures)
}

void render_engine::verbosity_level()
{
    auto level = scene->get_bounty().get_gs_verbosity_level();
    if(level == "info")
        interface->setVerbosityInfo();
    else if(level == "warning")
        interface->setVerbosityWarning();
    else if(level == "error")
        interface->setVerbosityError();
    else
        interface->setVerbosityMute();
}

void render_engine::render(PyObject *scene)
{
}
