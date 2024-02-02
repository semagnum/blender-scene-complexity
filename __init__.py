# Copyright (C) 2024 Spencer Magnusson
# semagnum@gmail.com
# Created by Spencer Magnusson
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.


import bpy

from .register_util import register_all, unregister_all
from . import model, operators, panels

bl_info = {
    "name": 'Scene Complexity',
    "author": 'Spencer Magnusson',
    "version": (0, 0, 4),
    "blender": (2, 93, 0),
    "description": 'Analyze various aspects of scene to determine complexity',
    "location": 'Properties -> Scene',
    "support": 'COMMUNITY',
    'category': '3D View',
    "category_icon": 'Scene',
    'tracker_url': 'https://github.com/semagnum/blender-scene-complexity/issues',
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
