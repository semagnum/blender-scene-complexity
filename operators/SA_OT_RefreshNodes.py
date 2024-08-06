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


def get_nodes_used(curr_node: bpy.types.Node, node_group_cache: dict[str, set[bpy.types.Node]], image_cache: set[bpy.types.Image]) -> set[bpy.types.Node]:
    """Get all nodes currently used within a node tree.

    :param curr_node: node to start with.
    """
    node_set = set()
    if not curr_node.mute:
        if hasattr(curr_node, 'node_tree'):
            node_group_name = curr_node.node_tree.name
            if node_group_name not in node_group_cache:
                new_node_group_entry = set()
                for output in get_output_nodes(curr_node.node_tree):
                    new_node_group_entry.update(get_nodes_used(output, node_group_cache, image_cache))
                node_group_cache[node_group_name] = new_node_group_entry

            node_set.update(node_group_cache[curr_node.node_tree.name])
        elif not any(p in curr_node.bl_idname for p in NODE_PATTERNS_TO_SKIP):
            node_set.add(curr_node)

            if curr_node.type == 'TEX_IMAGE' and hasattr(curr_node.image, 'size'):
                image_cache.add(curr_node.image)

    nodes_from_inputs = [
        get_nodes_used(link.from_node, node_group_cache, image_cache)
        for node_input in curr_node.inputs
        for link in node_input.links
        if node_input.is_linked
    ]
    for n in nodes_from_inputs:
        node_set.update(n)
    return node_set


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

        materials = {
            material_slot.material
            for object in context.scene.objects
            for material_slot in object.material_slots
            if material_slot.material and material_slot.material.use_nodes
        }

        failed_node_trees = []
        node_group_cache = dict()
        for material in materials:
            node_tree = material.node_tree
            total_nodes = set()
            image_cache = set()
            for output in get_output_nodes(node_tree):
                total_nodes.update(get_nodes_used(output, node_group_cache, image_cache))

            texture_size = max(
                [
                    max(image.size)
                    for image in image_cache
                ],
                default=0
            )
            new_material_cache: NodeCache = window_manager.sa_material_cache.add()
            new_material_cache.name = material.name
            new_material_cache.nodes_used = len(total_nodes)
            new_material_cache.max_texture_size = texture_size

        window_manager.sa_geometry_cache.clear()
        geo_node_trees = (node_tree for node_tree in bpy.data.node_groups if node_tree.bl_idname == 'GeometryNodeTree')
        for geometry_node_tree in geo_node_trees:
            total_nodes = set()
            for output in get_output_nodes(geometry_node_tree):
                total_nodes.update(get_nodes_used(output, node_group_cache, set()))
            new_data: NodeCache = window_manager.sa_geometry_cache.add()
            new_data.name = geometry_node_tree.name
            new_data.nodes_used = len(total_nodes)

        if failed_node_trees:
            self.report({'WARNING'}, 'Some node trees failed to update (see console)')
            print(''.join([
                '\n\t{} ({})'.format(tree_name, e)
                for tree_name, e in failed_node_trees
            ]))
        return {'FINISHED'}
