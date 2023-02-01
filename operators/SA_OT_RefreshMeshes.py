from typing import Iterator

import bpy
import bmesh

from ..model.CacheGroups import MeshObjectCache


def find_vert_face_instancers(curr_coll: bpy.types.Collection) -> Iterator[bpy.types.Collection]:
    """Find all objects that face or vert instancers.

    :param curr_coll: current collection
    """
    return (obj for obj in curr_coll.all_objects if obj.is_instancer and obj.instance_type in {'VERTS', 'FACES'})


def get_parent_ancestors(obj: bpy.types.Object) -> list[bpy.types.Object]:
    """Returns all ancestors of the current object.

    :param obj: Blender object
    """
    curr_obj = obj
    parents = []
    while curr_obj.parent is not None:
        parents.append(curr_obj.parent)
        curr_obj = obj.parent
    return parents


def get_bmesh_data(obj: bpy.types.Object, depsgraph: bpy.types.Depsgraph, use_bmesh: bool = True) -> tuple[int]:
    """Gets bmesh stats for object.

    :param obj: mesh object
    :param depsgraph: current scene depsgraph.
    :param use_bmesh: whether to use evaluated bmesh or simplified stats.
    :return: Tuple containing the evaluated ``(face_count, triangle_count, vertex_count)`` of the mesh object.
    """
    if not use_bmesh:
        face_count = len(obj.data.polygons)
        verts_count = len(obj.data.vertices)
        tris_count = sum(len(face.vertices) - 2 for face in obj.data.polygons)
    else:
        blender_mesh = obj.evaluated_get(depsgraph).to_mesh(preserve_all_data_layers=True, depsgraph=depsgraph)

        bm = bmesh.new()
        bm.from_mesh(blender_mesh)
        bm.faces.ensure_lookup_table()

        face_count = len(bm.faces)
        tris_count = len(bm.calc_loop_triangles())
        verts_count = len(bm.verts)

        bm.free()

    return face_count, tris_count, verts_count


class SA_OT_RefreshMeshes(bpy.types.Operator):
    """Refreshes the mesh cache."""
    bl_idname = 'scene_analyzer.refresh_meshes'
    bl_label = 'Refresh mesh objects'
    bl_description = 'Refresh cache of mesh stats'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        window_manager = context.window_manager
        window_manager.sa_mesh_cache.clear()
        root_collection = context.view_layer.layer_collection.collection
        all_mesh_objects = {o for o in root_collection.all_objects if o.type == 'MESH'}
        material_cache_tree = {m.name: m.nodes_used for m in window_manager.sa_material_cache}

        depsgraph = context.evaluated_depsgraph_get()
        use_bmesh = window_manager.sa_apply_modifiers
        for o in all_mesh_objects:
            new_data: MeshObjectCache = window_manager.sa_mesh_cache.add()
            new_data.name = o.name_full
            new_data.material_count = len({m.material.name_full for m in o.material_slots if m.material is not None})
            try:
                new_data.faces, new_data.tris, new_data.verts = get_bmesh_data(o, depsgraph, use_bmesh)
            except Exception as e:
                print('Uninitialized data for ' + new_data.name, e)

            new_data.modifier_count = len(o.modifiers)

            uniq_material_names = {m.material.name for m in o.material_slots if m.material is not None}
            for m in uniq_material_names:
                if m in material_cache_tree:
                    new_data.material_node_count += material_cache_tree[m]

        return {'FINISHED'}
