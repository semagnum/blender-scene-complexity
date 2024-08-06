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


def get_bmesh_data(obj: bpy.types.Object, depsgraph: bpy.types.Depsgraph, use_bmesh: bool = True) -> tuple[int, int]:
    """Gets bmesh stats for object.

    :param obj: mesh object
    :param depsgraph: current scene depsgraph.
    :param use_bmesh: whether to use evaluated bmesh or simplified stats.
    :return: Tuple containing the evaluated ``(triangle_count, vertex_count)`` of the mesh object.
    """
    if not use_bmesh:
        data = obj.data
    else:
        data = obj.evaluated_get(depsgraph).data

    return sum([len(face.vertices) - 2 for face in data.polygons]), len(data.vertices)


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
        all_mesh_objects = [o for o in root_collection.all_objects if o.type == 'MESH']
        material_cache_tree = {m.name: m.nodes_used for m in window_manager.sa_material_cache}

        depsgraph = context.evaluated_depsgraph_get()
        use_bmesh = window_manager.sa_apply_modifiers
        failed_meshes = []
        for o in all_mesh_objects:
            new_data: MeshObjectCache = window_manager.sa_mesh_cache.add()
            new_data.name = o.name_full
            new_data.material_count = len({m.material.name_full for m in o.material_slots if m.material is not None})
            try:
                new_data.tris, new_data.verts = get_bmesh_data(o, depsgraph, use_bmesh)
            except Exception as e:
                failed_meshes.append((o.name, str(e)))

            new_data.modifier_count = len(o.modifiers)

            new_data.material_count = sum([
                material_cache_tree[m.material.name]
                for m in o.material_slots
                if m.material is not None and
                m.material.name in material_cache_tree
            ])

        if failed_meshes:
            self.report({'WARNING'}, 'Some meshes failed to update (see console)')
            print(''.join([
                '\n\t{} ({})'.format(mesh_name, e)
                for mesh_name, e in failed_meshes
            ]))

        return {'FINISHED'}
