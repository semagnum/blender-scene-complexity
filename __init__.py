import bpy

from .operators.SA_OT_RefreshAll import SA_OT_RefreshAll
from .operators.SA_OT_RefreshMeshes import SA_OT_RefreshMeshes
from .operators.SA_OT_RefreshCollections import SA_OT_RefreshCollections
from .operators.SA_OT_RefreshNodes import SA_OT_RefreshNodes

from .model.CacheGroups import MeshObjectCache, CollectionCache, NodeCache

from .panels.SA_Complexity_Tables import SA_PT_ComplexityTable
from .panels.SA_Complexity import SA_UL_MeshComplexity, SA_UL_MaterialNodeComplexity, SA_UL_GeometryNodeComplexity, \
    SA_UL_CollectionComplexity

bl_info = {
    "name": 'Scene Complexity',
    "author": 'Spencer Magnusson',
    "version": (0, 0, 1),
    "blender": (2, 93, 0),
    "description": 'Analyze various aspects of scene to determine complexity',
    "location": 'Scene',
    "support": 'COMMUNITY',
    "category_icon": 'Scene'
}
ui_lists = [SA_UL_MeshComplexity, SA_UL_MaterialNodeComplexity, SA_UL_GeometryNodeComplexity,
            SA_UL_CollectionComplexity]
prop_groups = [MeshObjectCache, CollectionCache, NodeCache]
operators_panels = [SA_OT_RefreshMeshes, SA_OT_RefreshCollections, SA_OT_RefreshNodes, SA_OT_RefreshAll,
                    SA_PT_ComplexityTable]

classes = ui_lists + prop_groups + operators_panels

properties = [
    ('sa_apply_modifiers', bpy.props.BoolProperty(name='Apply modifiers',
                                                  description='Will apply modifiers for mesh statistics',
                                                  default=True)),
    ('sa_mesh_cache', bpy.props.CollectionProperty(type=MeshObjectCache, options={'SKIP_SAVE'})),
    ('sa_collection_cache', bpy.props.CollectionProperty(type=CollectionCache, options={'SKIP_SAVE'})),
    ('sa_material_cache', bpy.props.CollectionProperty(type=NodeCache, options={'SKIP_SAVE'})),
    ('sa_geometry_cache', bpy.props.CollectionProperty(type=NodeCache, options={'SKIP_SAVE'})),

    ('sa_mesh_active', bpy.props.IntProperty(default=0, options={'SKIP_SAVE'})),
    ('sa_collection_active', bpy.props.IntProperty(default=0, options={'SKIP_SAVE'})),
    ('sa_material_active', bpy.props.IntProperty(default=0, options={'SKIP_SAVE'})),
    ('sa_geometry_active', bpy.props.IntProperty(default=0, options={'SKIP_SAVE'})),

    ('mesh_cache_sort_value', bpy.props.EnumProperty(items=[
        ('name', 'Name', 'Mesh object name'),
        ('tris', 'Triangles', 'Calculated triangle count'),
        ('verts', 'Vertices', 'Vertex count'),
        ('modifier_count', 'Modifier Count', 'number of modifiers on meshobject'),
        ('material_count', 'Materials', 'Number of materials on object'),
        ('material_node_count', 'nodes', 'total number of shader nodes used on object'),
    ])),
    ('collection_cache_sort_value', bpy.props.EnumProperty(items=[
        ('name', 'Name', 'Collection name'),
        ('total_tris', 'Triangles', 'Calculated triangle count'),
        ('total_verts', 'Vertices', 'Vertex count'),
        ('instance_count', 'Instances', 'Number of instances of this collection'),
    ])),
    ('material_cache_sort_value', bpy.props.EnumProperty(items=[
        ('name', 'Name', 'Material node tree name'),
        ('nodes_used', 'Nodes', 'Total number of used nodes'),
    ])),
    ('geometry_cache_sort_value', bpy.props.EnumProperty(items=[
        ('name', 'Name', 'Geometry node tree name'),
        ('nodes_used', 'Nodes', 'Total number of used nodes'),
    ])),
]


def register():
    window_manager = bpy.types.WindowManager

    for cls in classes:
        bpy.utils.register_class(cls)

    for name, prop in properties:
        setattr(window_manager, name, prop)


def unregister():
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)


if __name__ == '__main__':
    register()
