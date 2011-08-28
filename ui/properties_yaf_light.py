import bpy
#import types and props ---->
from bpy.props import (EnumProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       StringProperty)
from bpy.types import Panel

Lamp = bpy.types.Lamp


def call_lighttype_update(self, context):
        lamp = context.scene.objects.active
        if lamp.type == 'LAMP':
            switchLampType = {'area': 'AREA', 'spot': 'SPOT', 'sun': 'SUN', 'point': 'POINT', 'ies': 'SPOT'}
            lamp.data.type = switchLampType.get(lamp.data.lamp_type)

Lamp.lamp_type = EnumProperty(
    name="Light type",
    items=(
        ('point', "Point", "Assign light type to the selected light"),
        ('sun', "Sun", "Assign light type to the selected light"),
        ('spot', "Spot", "Assign light type to the selected light"),
        ('ies', "IES", "Assign light type to the selected light"),
        ('area', "Area", "Assign light type to the selected light")
    ),
    default="point", update=call_lighttype_update)

Lamp.yaf_energy = FloatProperty(
    name="Power",
    description="Intensity multiplier for color",
    min=0.0, max=10000.0,
    default=1.0)

Lamp.directional = BoolProperty(
    name="Directional",
    description="",
    default=False)

Lamp.create_geometry = BoolProperty(
    name="Create geometry",
    description="Creates a visible geometry in the dimensions of the light during the render",
    default=False)

Lamp.infinite = BoolProperty(
    name="Infinite",
    description="Determines if light is infinite or filling a semi-infinite cylinder",
    default=True)

Lamp.spot_soft_shadows = BoolProperty(
    name="Soft shadows",
    description="Use soft shadows",
    default=False)

Lamp.shadow_fuzzyness = FloatProperty(
    name="Shadow fuzzyness",
    description="Fuzzyness of the soft shadows (0 - hard shadow, 1 - fuzzy shadow)",
    min=0.0, max=1.0,
    default=1.0)

Lamp.photon_only = BoolProperty(
    name="Photon only",
    description="This spot will only throw photons not direct light",
    default=False)

Lamp.angle = FloatProperty(
    name="Angle",
    description="Angle of the cone in degrees (shadow softness)",
    min=0.0, max=80.0,
    default=0.5)

Lamp.ies_soft_shadows = BoolProperty(
    name="IES Soft shadows",
    description="Use soft shadows for IES light type",
    default=False)

Lamp.ies_file = StringProperty(
    name="IES File",
    description="File to be used as the light projection",
    subtype='FILE_PATH',
    default="")

Lamp.yaf_samples = IntProperty(
    name="Samples",
    description="Number of samples to be taken for direct lighting",
    min=0, max=512,
    default=16)


class LampButtonsPanel():
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    @classmethod
    def poll(cls, context):
        engine = context.scene.render.engine
        return context.lamp and (engine in cls.COMPAT_ENGINES)


class YAF_PT_preview(LampButtonsPanel, Panel):
    bl_label = "Preview"
    COMPAT_ENGINES = {'YAFA_RENDER'}

    def draw(self, context):
        self.layout.template_preview(context.lamp)


class YAF_PT_lamp(LampButtonsPanel, Panel):
    bl_label = "Lamp settings"
    COMPAT_ENGINES = {'YAFA_RENDER'}

    def draw(self, context):
        layout = self.layout
        lamp = context.lamp

        layout.prop(lamp, "lamp_type", expand=True)
        layout.separator()

        layout.prop(lamp, "color")
        layout.prop(lamp, "yaf_energy", text="Power")

        if lamp.lamp_type == 'area':
            layout.prop(lamp, "yaf_samples")
            layout.prop(lamp, "create_geometry")

        elif lamp.lamp_type == 'spot':
            layout.prop(lamp, "spot_soft_shadows", toggle=True)

            if lamp.spot_soft_shadows:
                box = layout.box()
                box.prop(lamp, "yaf_samples")
                box.prop(lamp, "shadow_fuzzyness")

            layout.prop(lamp, "photon_only")

        elif lamp.lamp_type == 'sun':
            layout.prop(lamp, "angle")
            layout.prop(lamp, "yaf_samples")
            layout.prop(lamp, "directional", toggle=True)
            if lamp.directional:
                box = layout.box()
                box.prop(lamp, "shadow_soft_size")
                box.prop(lamp, "infinite")

        elif lamp.lamp_type == 'point':
            layout.prop(lamp, "use_sphere", toggle=True)
            if lamp.use_sphere:
                box = layout.box()
                box.prop(lamp, "shadow_soft_size")
                box.prop(lamp, "yaf_samples")
                box.prop(lamp, "create_geometry")

        elif lamp.lamp_type == 'ies':
            layout.prop(lamp, "ies_file")
            layout.prop(lamp, "ies_soft_shadows", toggle=True)
            if lamp.ies_soft_shadows:
                box = layout.box()
                box.prop(lamp, "yaf_samples")


class YAF_PT_spot(LampButtonsPanel, Panel):
    bl_label = "Spot Shape"
    COMPAT_ENGINES = {'YAFA_RENDER'}

    @classmethod
    def poll(cls, context):
        lamp = context.lamp
        engine = context.scene.render.engine
        return (lamp and lamp.lamp_type == 'spot') and (engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        layout = self.layout
        lamp = context.lamp

        split = layout.split()

        col = split.column()
        col.prop(lamp, "spot_size", text="Size")
        col.prop(lamp, "show_cone")

        col = split.column()

        col.prop(lamp, "spot_blend", text="Blend", slider=True)
