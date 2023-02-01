import bpy

from .. import register_all
from .. import unregister_all

from .CacheGroups import MeshObjectCache
from .CacheGroups import CollectionCache
from .CacheGroups import NodeCache

_register_order = (MeshObjectCache, CollectionCache, NodeCache)
_register_props = (('sa_mesh_cache', bpy.props.CollectionProperty(type=MeshObjectCache, options={'SKIP_SAVE'})),
                   ('sa_collection_cache', bpy.props.CollectionProperty(type=CollectionCache, options={'SKIP_SAVE'})),
                   ('sa_material_cache', bpy.props.CollectionProperty(type=NodeCache, options={'SKIP_SAVE'})),
                   ('sa_geometry_cache', bpy.props.CollectionProperty(type=NodeCache, options={'SKIP_SAVE'})))


def register():
    register_all(_register_order, _register_props)


def unregister():
    unregister_all(_register_order[::-1])
