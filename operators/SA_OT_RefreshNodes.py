import bpy

from ..model.CacheGroups import NodeCache

NODE_PATTERNS_TO_SKIP = {'Reroute', 'GroupInput', 'GroupOutput', 'NodeOutput'}


def get_nodes_used(curr_node):
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


def get_output_nodes(node_tree):
    return (node for node in node_tree.nodes if 'Output' in node.bl_idname)


class SA_OT_RefreshNodes(bpy.types.Operator):
    bl_idname = 'scene_analyzer.refresh_nodes'
    bl_label = 'Refresh nodes'
    bl_description = 'Refresh cache of node stats'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        scene.sa_material_cache.clear()
        for material in bpy.data.materials:
            if material.use_nodes:
                node_tree = material.node_tree
                try:
                    total_nodes = {}
                    for output in get_output_nodes(node_tree):
                        total_nodes.update(get_nodes_used(output))
                    new_material_cache: NodeCache = scene.sa_material_cache.add()
                    new_material_cache.name = material.name
                    new_material_cache.nodes_used = len(total_nodes.keys())
                except Exception as e:
                    print('Adding material to cache failed', material.name, e)

        scene.sa_geometry_cache.clear()
        geo_node_trees = (node_tree for node_tree in bpy.data.node_groups if node_tree.bl_idname == 'GeometryNodeTree')
        for geometry_node_tree in geo_node_trees:
            try:
                total_nodes = {}
                for output in get_output_nodes(geometry_node_tree):
                    total_nodes.update(get_nodes_used(output))
                new_data: NodeCache = scene.sa_geometry_cache.add()
                new_data.name = geometry_node_tree.name
                new_data.nodes_used = len(total_nodes.keys())
            except Exception as e:
                print('Adding geometry nodes to cache failed', geometry_node_tree.name, e)
        return {'FINISHED'}
