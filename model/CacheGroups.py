# Copyright (C) 2023 Spencer Magnusson
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


class MeshObjectCache(bpy.types.PropertyGroup):
    """Cache of objects and their sizes by triangles, vertices, materials and their nodes, and modifiers."""
    name: bpy.props.StringProperty(name="Mesh Object Name", default="")

    tris: bpy.props.IntProperty(default=0)
    verts: bpy.props.IntProperty(default=0)

    material_count: bpy.props.IntProperty(default=0)
    material_node_count: bpy.props.IntProperty(default=0)

    modifier_count: bpy.props.IntProperty(default=0)


class CollectionCache(bpy.types.PropertyGroup):
    """Cache of collections and their sizes by total triangles, vertices, and the number of times it's instanced."""
    name: bpy.props.StringProperty(name="Collection Name", default="")

    total_tris: bpy.props.IntProperty(default=0)
    total_verts: bpy.props.IntProperty(default=0)

    instance_count: bpy.props.IntProperty(default=0)  # all collection instances (recursive)


class NodeCache(bpy.types.PropertyGroup):
    """Cache of node trees and their sizes. Used for both material and geometry nodes."""
    name: bpy.props.StringProperty(name="Node Name", default="")

    nodes_used: bpy.props.IntProperty(default=0)
