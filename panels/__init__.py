import bpy

from .. import register_all
from .. import unregister_all

from .SA_Complexity_Tables import SA_PT_ComplexityTable
from .SA_Complexity import SA_UL_MeshComplexity
from .SA_Complexity import SA_UL_MaterialNodeComplexity
from .SA_Complexity import SA_UL_GeometryNodeComplexity
from .SA_Complexity import SA_UL_CollectionComplexity

_register_order = (
    SA_UL_MeshComplexity, SA_UL_MaterialNodeComplexity, SA_UL_GeometryNodeComplexity, SA_UL_CollectionComplexity,
    SA_PT_ComplexityTable)
_register_props = (('sa_mesh_active', bpy.props.IntProperty(default=0, options={'SKIP_SAVE'})),
                   ('sa_collection_active', bpy.props.IntProperty(default=0, options={'SKIP_SAVE'})),
                   ('sa_material_active', bpy.props.IntProperty(default=0, options={'SKIP_SAVE'})),
                   ('sa_geometry_active', bpy.props.IntProperty(default=0, options={'SKIP_SAVE'})),

                   ('mesh_cache_sort_value', bpy.props.EnumProperty(items=[
                       ('name', 'Name', 'Mesh object name'),
                       ('tris', 'Triangles', 'Calculated triangle count'),
                       ('verts', 'Vertices', 'Vertex count'),
                       ('modifier_count', 'Modifier Count', 'number of modifiers on meshobject'),
                       ('material_count', 'Materials', 'Number of materials on object'),
                       ('material_node_count', 'Nodes', 'total number of shader nodes used on object'),
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
                   )


def register():
    register_all(_register_order, _register_props)


def unregister():
    unregister_all(_register_order[::-1])
