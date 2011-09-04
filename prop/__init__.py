from . import yaf_object
from . import yaf_material


def register():
    yaf_object.register()
    yaf_material.register()


def unregister():
    yaf_object.unregister()
    yaf_material.unregister()
