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

from ..operators.SA_OT_RefreshAll import SA_OT_RefreshAll


class SA_PT_ComplexityTable(bpy.types.Panel):
    """Scene properties panel to show scene and file complexity."""
    bl_label = 'Scene Analyzer'
    bl_category = 'Scene Analyzer'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'scene'

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        layout.operator(SA_OT_RefreshAll.bl_idname, icon='FILE_REFRESH')

        layout.prop(wm, 'sa_apply_modifiers')

        layout.label(text='Mesh Objects')
        layout.prop(wm, 'mesh_cache_sort_value', expand=True)
        layout.template_list('SA_UL_MeshComplexity', '', wm, 'sa_mesh_cache', wm, 'sa_mesh_active', columns=6)

        layout.label(text='Collections')
        layout.prop(wm, 'collection_cache_sort_value', expand=True)
        layout.template_list('SA_UL_CollectionComplexity', '', wm, 'sa_collection_cache', wm,
                             'sa_collection_active', columns=4)

        layout.label(text='Material Nodes')
        layout.prop(wm, 'material_cache_sort_value', expand=True)
        layout.template_list('SA_UL_MaterialNodeComplexity', '', wm, 'sa_material_cache',
                             wm, 'sa_material_active', columns=2)

        layout.label(text='Geometry Nodes')
        layout.prop(wm, 'geometry_cache_sort_value', expand=True)
        layout.template_list('SA_UL_GeometryNodeComplexity', '', wm, 'sa_geometry_cache',
                             wm, 'sa_geometry_active', columns=2, rows=3)
