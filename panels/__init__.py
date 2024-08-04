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

from .. import register_all
from .. import unregister_all

from .SA_Complexity_Tables import SA_PT_ComplexityTable
from .SA_Complexity import SA_UL_MeshComplexity
from .SA_Complexity import SA_UL_MaterialNodeComplexity
from .SA_Complexity import SA_UL_GeometryNodeComplexity
from .SA_Complexity import SA_UL_CollectionComplexity

_register_order = (
    SA_UL_MeshComplexity, SA_UL_MaterialNodeComplexity, SA_UL_GeometryNodeComplexity, SA_UL_CollectionComplexity,
    SA_PT_ComplexityTable)
_register_props = (('sa_mesh_active', bpy.props.IntProperty(default=0, options={'SKIP_SAVE'})),
                   ('sa_collection_active', bpy.props.IntProperty(default=0, options={'SKIP_SAVE'})),
                   ('sa_material_active', bpy.props.IntProperty(default=0, options={'SKIP_SAVE'})),
                   ('sa_geometry_active', bpy.props.IntProperty(default=0, options={'SKIP_SAVE'})),

                   ('mesh_cache_sort_value', bpy.props.EnumProperty(items=[
                       ('name', 'Name', 'Mesh object name'),
                       ('tris', 'Triangles', 'Calculated triangle count'),
                       ('verts', 'Vertices', 'Vertex count'),
                       ('modifier_count', 'Modifiers', 'Total number of modifiers on object'),
                       ('material_count', 'Material', 'Total number of material slots used on object'),
                       ('material_node_count', 'Nodes', 'Total number of shader nodes used on object'),
                   ])),
                   ('collection_cache_sort_value', bpy.props.EnumProperty(items=[
                       ('name', 'Name', 'Collection name'),
                       ('total_tris', 'Triangles', 'Calculated triangle count'),
                       ('total_verts', 'Vertices', 'Vertex count'),
                       ('instance_count', 'Instances', 'Number of instances of this collection'),
                   ])),
                   ('material_cache_sort_value', bpy.props.EnumProperty(items=[
                       ('name', 'Name', 'Node tree name'),
                       ('nodes_used', 'Nodes', 'Total number of nodes used'),
                       ('max_texture_size', 'Texture Size', 'Maximum width or height of textures used within material'),
                   ])),
                   ('geometry_cache_sort_value', bpy.props.EnumProperty(items=[
                       ('name', 'Name', 'Node tree name'),
                       ('nodes_used', 'Nodes', 'Total number of nodes used'),
                   ])),
                   )


def register():
    register_all(_register_order, _register_props)


def unregister():
    unregister_all(_register_order[::-1])
