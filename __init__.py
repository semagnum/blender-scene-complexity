import bpy

from .register_util import register_all, unregister_all
from . import model
from . import operators
from . import panels

bl_info = {
    "name": 'Scene Complexity',
    "author": 'Spencer Magnusson',
    "version": (0, 0, 2),
    "blender": (2, 93, 0),
    "description": 'Analyze various aspects of scene to determine complexity',
    "location": 'Scene',
    "support": 'COMMUNITY',
    "category_icon": 'Scene'
}

properties = [
    ('sa_apply_modifiers', bpy.props.BoolProperty(name='Apply modifiers',
                                                  description='Will apply modifiers for mesh statistics',
                                                  default=True)),
]


def register():
    window_manager = bpy.types.WindowManager

    model.register()
    operators.register()
    panels.register()

    for name, prop in properties:
        setattr(window_manager, name, prop)


def unregister():
    panels.unregister()
    operators.unregister()
    model.unregister()


if __name__ == '__main__':
    register()
