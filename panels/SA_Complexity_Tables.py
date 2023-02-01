import bpy

from ..operators.SA_OT_RefreshAll import SA_OT_RefreshAll
from ..operators.SA_OT_RefreshCollections import SA_OT_RefreshCollections
from ..operators.SA_OT_RefreshMeshes import SA_OT_RefreshMeshes
from ..operators.SA_OT_RefreshNodes import SA_OT_RefreshNodes


class SA_PT_ComplexityTable(bpy.types.Panel):
    "Scene properties panel to show scene and file complexity."
    bl_label = 'Scene Analyzer'
    bl_category = 'Scene Analyzer'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'scene'

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        col = layout.column(align=True)
        col.operator(SA_OT_RefreshAll.bl_idname, icon='FILE_REFRESH')
        row = col.row()
        row.operator(SA_OT_RefreshMeshes.bl_idname, icon='MESH_DATA')
        row.operator(SA_OT_RefreshCollections.bl_idname, icon='OUTLINER_COLLECTION')
        row.operator(SA_OT_RefreshNodes.bl_idname, icon='NODETREE')

        layout.prop(wm, 'sa_apply_modifiers', icon='MODIFIER')

        layout.label(text='Mesh objects')
        layout.prop(wm, 'mesh_cache_sort_value', expand=True)
        layout.template_list('SA_UL_MeshComplexity', '', wm, 'sa_mesh_cache', wm, 'sa_mesh_active', columns=6)

        layout.label(text='Collections')
        layout.prop(wm, 'collection_cache_sort_value', expand=True)
        layout.template_list('SA_UL_CollectionComplexity', '', wm, 'sa_collection_cache', wm,
                             'sa_collection_active', columns=4)

        layout.label(text='Shader nodes')
        layout.prop(wm, 'material_cache_sort_value', expand=True)
        layout.template_list('SA_UL_MaterialNodeComplexity', '', wm, 'sa_material_cache',
                             wm, 'sa_material_active', columns=2)

        layout.label(text='Geometry nodes')
        layout.prop(wm, 'geometry_cache_sort_value', expand=True)
        layout.template_list('SA_UL_GeometryNodeComplexity', '', wm, 'sa_geometry_cache',
                             wm, 'sa_geometry_active', columns=2)
