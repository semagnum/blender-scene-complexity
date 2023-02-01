import bpy


class SA_OT_RefreshAll(bpy.types.Operator):
    """Refreshes all node, mesh, and collection caches."""
    bl_idname = 'scene_analyzer.refresh_all'
    bl_label = 'Refresh all'
    bl_description = 'Refresh all caches'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ops = bpy.ops
        ops.scene_analyzer.refresh_nodes()
        ops.scene_analyzer.refresh_meshes()
        ops.scene_analyzer.refresh_collections()
        return {'FINISHED'}
