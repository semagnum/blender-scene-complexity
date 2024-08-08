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


class SA_OT_RefreshAll(bpy.types.Operator):
    """Refreshes all node, mesh, and collection caches."""
    bl_idname = 'scene_analyzer.refresh_all'
    bl_label = 'Refresh'
    bl_description = 'Refresh all scene analyzer caches'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ops = bpy.ops
        ops.scene_analyzer.refresh_nodes()
        ops.scene_analyzer.refresh_meshes()
        ops.scene_analyzer.refresh_collections()
        return {'FINISHED'}
