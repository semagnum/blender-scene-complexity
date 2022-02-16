import bpy

from ..operators.SA_OT_RefreshAll import SA_OT_RefreshAll
from ..operators.SA_OT_RefreshCollections import SA_OT_RefreshCollections
from ..operators.SA_OT_RefreshMeshes import SA_OT_RefreshMeshes
from ..operators.SA_OT_RefreshNodes import SA_OT_RefreshNodes


class SA_PT_ComplexityTable(bpy.types.Panel):
    bl_label = 'Scene Analyzer'
    bl_category = 'Scene Analyzer'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'scene'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        col = layout.column(align=True)
        col.operator(SA_OT_RefreshAll.bl_idname, icon='FILE_REFRESH')
        row = col.row()
        row.operator(SA_OT_RefreshMeshes.bl_idname, icon='MESH_DATA')
        row.operator(SA_OT_RefreshCollections.bl_idname, icon='OUTLINER_COLLECTION')
        row.operator(SA_OT_RefreshNodes.bl_idname, icon='NODETREE')

        layout.label(text='Mesh objects')
        layout.prop(scene, 'mesh_cache_sort_value', expand=True)
        layout.template_list('SA_UL_MeshComplexity', '', scene, 'sa_mesh_cache', scene, 'sa_mesh_active', columns=6)

        layout.label(text='Collections')
        layout.prop(scene, 'collection_cache_sort_value', expand=True)
        layout.template_list('SA_UL_CollectionComplexity', '', scene, 'sa_collection_cache', scene,
                             'sa_collection_active', columns=4)

        layout.label(text='Shader nodes')
        layout.prop(scene, 'material_cache_sort_value', expand=True)
        layout.template_list('SA_UL_MaterialNodeComplexity', '', scene, 'sa_material_cache',
                             scene, 'sa_material_active', columns=2)

        layout.label(text='Geometry nodes')
        layout.prop(scene, 'geometry_cache_sort_value', expand=True)
        layout.template_list('SA_UL_GeometryNodeComplexity', '', scene, 'sa_geometry_cache',
                             scene, 'sa_geometry_active', columns=2)
