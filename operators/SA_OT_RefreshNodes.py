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


from typing import Iterator

import bpy

from ..model import NodeCache

NODE_PATTERNS_TO_SKIP = {'Reroute', 'GroupInput', 'GroupOutput', 'NodeOutput'}
"""Node types that can be skipped in calculations.
Should only be non-operational nodes or otherwise not actually affecting the complexity or performance of a node tree.
"""


def get_nodes_used(curr_node: bpy.types.Node) -> dict[str, bpy.types.Node]:
    """Get all nodes currently used within a node tree.

    :param curr_node: node to start with.
    """
    curr_dict = {}
    if not curr_node.mute:
        if hasattr(curr_node, 'node_tree'):
            for output in get_output_nodes(curr_node.node_tree):
                curr_dict.update(get_nodes_used(output))
        elif not any(p in curr_node.bl_idname for p in NODE_PATTERNS_TO_SKIP):
            curr_dict[curr_node.id_data.name + curr_node.bl_idname] = curr_node

    for node_input in curr_node.inputs:
        if node_input.is_linked:
            for link in node_input.links:
                curr_dict.update(get_nodes_used(link.from_node))
    return curr_dict


def get_max_texture(curr_node: bpy.types.Node) -> int:
    """Get texture node image's size with most pixels.

    :param curr_node: node to start with.
    """

    if not curr_node.mute:
        if hasattr(curr_node, 'node_tree'):
            return max([
                get_max_texture(output)
                for output in get_output_nodes(curr_node.node_tree)
            ])
        elif curr_node.type == 'TEX_IMAGE':
            return max(curr_node.image.size[0], curr_node.image.size[1])

    texture_size = 0
    for node_input in curr_node.inputs:
        if node_input.is_linked:
            for link in node_input.links:
                texture_size = max(texture_size, get_max_texture(link.from_node))

    return texture_size


def get_output_nodes(node_tree: bpy.types.NodeTree) -> Iterator[bpy.types.Node]:
    """Returns all output nodes in a node tree."""
    return (node for node in node_tree.nodes if 'Output' in node.bl_idname)


class SA_OT_RefreshNodes(bpy.types.Operator):
    """Refreshes all node caches."""
    bl_idname = 'scene_analyzer.refresh_nodes'
    bl_label = 'Refresh nodes'
    bl_description = 'Refresh cache of node stats'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        window_manager = context.window_manager
        window_manager.sa_material_cache.clear()
        for material in bpy.data.materials:
            if material.use_nodes:
                node_tree = material.node_tree
                try:
                    total_nodes = {}
                    texture_size = 0
                    for output in get_output_nodes(node_tree):
                        total_nodes.update(get_nodes_used(output))
                        texture_size = max(texture_size, get_max_texture(output))
                    new_material_cache: NodeCache = window_manager.sa_material_cache.add()
                    new_material_cache.name = material.name
                    new_material_cache.nodes_used = len(total_nodes.keys())
                    new_material_cache.max_texture_size = texture_size
                except Exception as e:
                    print('Adding material to cache failed', material.name, e)

        window_manager.sa_geometry_cache.clear()
        geo_node_trees = (node_tree for node_tree in bpy.data.node_groups if node_tree.bl_idname == 'GeometryNodeTree')
        for geometry_node_tree in geo_node_trees:
            try:
                total_nodes = {}
                for output in get_output_nodes(geometry_node_tree):
                    total_nodes.update(get_nodes_used(output))
                new_data: NodeCache = window_manager.sa_geometry_cache.add()
                new_data.name = geometry_node_tree.name
                new_data.nodes_used = len(total_nodes.keys())
            except Exception as e:
                print('Adding geometry nodes to cache failed', geometry_node_tree.name, e)
        return {'FINISHED'}
