import bpy

from ..model.CacheGroups import MeshObjectCache, CollectionCache, NodeCache
from .formatting_util import format_num


class SA_UL_MeshComplexity(bpy.types.UIList):
    """UI list to display all meshes in a scene and their complexity."""
    is_visible: bpy.props.BoolProperty(
        name="Visible Only",
        description="Only show visible objects",
        default=True
    )
    """Toggle to only show visible objects."""
    is_selected: bpy.props.BoolProperty(
        name="Selected Only",
        description="Only show visible objects",
        default=False
    )
    """Toggle to only show selected object."""

    def draw_item(self, context, layout, data, mesh_obj_cache: MeshObjectCache, icon, active_data, active_propname,
                  index):
        layout.label(text=mesh_obj_cache.name)
        layout.label(text=format_num(mesh_obj_cache.tris), icon='MESH_DATA')
        layout.label(text=format_num(mesh_obj_cache.verts), icon='VERTEXSEL')

        layout.label(text=format_num(mesh_obj_cache.modifier_count), icon='MODIFIER')

        layout.label(text=format_num(mesh_obj_cache.material_count), icon='MATERIAL')
        layout.label(text=format_num(mesh_obj_cache.material_node_count), icon='NODETREE')

    def draw_filter(self, context, layout):
        row = layout.row()
        row.prop(self, 'filter_name', text='')
        row.prop(self, 'is_visible', text='', icon='HIDE_OFF')
        row.prop(self, 'is_selected', text='', icon='RESTRICT_SELECT_OFF')

    def filter_items(self, context, data, propname):
        all_mesh_objects = getattr(data, propname)
        obj_data = [bpy.data.objects[mesh_obj.name] for mesh_obj in all_mesh_objects]
        helper_funcs = bpy.types.UI_UL_list

        # Default return values.
        flt_flags = []
        flt_neworder = []

        # Filtering by name
        if self.filter_name:
            flt_flags = helper_funcs.filter_items_by_name(self.filter_name, self.bitflag_filter_item,
                                                          all_mesh_objects, 'name')

        if not flt_flags:
            if self.is_visible or self.is_selected:
                flt_flags = [0 if (self.is_visible and obj_data[idx].hide_get()) or (
                            self.is_selected and not obj_data[idx].select_get()) else self.bitflag_filter_item for
                             idx, coll in enumerate(all_mesh_objects)]
            else:
                flt_flags = [self.bitflag_filter_item] * len(all_mesh_objects)

        sort_value = context.window_manager.mesh_cache_sort_value
        _sort = [(idx, getattr(it, sort_value, '')) for idx, it in enumerate(all_mesh_objects)]
        if sort_value == 'name':
            flt_neworder = helper_funcs.sort_items_helper(_sort, lambda e: e[1].lower())
        else:
            flt_neworder = helper_funcs.sort_items_helper(_sort, lambda e: e[1], True)

        return flt_flags, flt_neworder


class SA_UL_CollectionComplexity(bpy.types.UIList):
    """UI list to display all collections in a scene and their complexity."""
    is_instanced: bpy.props.BoolProperty(
        name='Instanced Only',
        description='Only show collections instanced by other objects',
        default=False
    )
    """Toggle to only show instanced collections."""

    def draw_item(self, context, layout, data, coll_cache: CollectionCache, icon, active_data, active_propname,
                  index):
        layout.label(text=coll_cache.name)
        layout.label(text=format_num(coll_cache.total_tris), icon='MESH_DATA')
        layout.label(text=format_num(coll_cache.total_verts), icon='VERTEXSEL')

        layout.label(text=format_num(coll_cache.instance_count), icon='OUTLINER_OB_GROUP_INSTANCE')

    def draw_filter(self, context, layout):
        row = layout.row()
        row.prop(self, 'filter_name', text='')
        row.prop(self, 'is_instanced', text='', icon='OUTLINER_OB_GROUP_INSTANCE')

    def filter_items(self, context, data, propname):
        all_collections = getattr(data, propname)
        helper_funcs = bpy.types.UI_UL_list

        # Default return values.
        flt_flags = []
        flt_neworder = []

        # Filtering by name
        if self.filter_name:
            flt_flags = helper_funcs.filter_items_by_name(self.filter_name, self.bitflag_filter_item,
                                                          all_collections, 'name')
        if not flt_flags:
            if self.is_instanced:
                flt_flags = [0 if coll.instance_count == 0 else self.bitflag_filter_item for idx, coll in
                             enumerate(all_collections)]
            else:
                flt_flags = [self.bitflag_filter_item] * len(all_collections)

        sort_value = context.window_manager.collection_cache_sort_value
        _sort = [(idx, getattr(it, sort_value, '')) for idx, it in enumerate(all_collections)]
        if sort_value == 'name':
            flt_neworder = helper_funcs.sort_items_helper(_sort, lambda e: e[1].lower())
        else:
            flt_neworder = helper_funcs.sort_items_helper(_sort, lambda e: e[1], True)

        return flt_flags, flt_neworder


class SA_UL_MaterialNodeComplexity(bpy.types.UIList):
    """UI list to display all material nodes in a Blender file and their complexity."""

    def draw_item(self, context, layout, data, node_cache: NodeCache, icon, active_data, active_propname,
                  index):
        layout.label(text=node_cache.name)
        layout.label(text=format_num(node_cache.nodes_used), icon='NODETREE')

    def filter_items(self, context, data, propname):
        all_nodes = getattr(data, propname)
        helper_funcs = bpy.types.UI_UL_list

        # Default return values.
        flt_flags = []
        flt_neworder = []

        # Filtering by name
        if self.filter_name:
            flt_flags = helper_funcs.filter_items_by_name(self.filter_name, self.bitflag_filter_item,
                                                          all_nodes, 'name')
        if not flt_flags:
            flt_flags = [self.bitflag_filter_item] * len(all_nodes)

        if len(all_nodes) > 0:
            sort_value = context.window_manager.material_cache_sort_value
            _sort = [(idx, getattr(it, sort_value, '')) for idx, it in enumerate(all_nodes)]
            if sort_value == 'name':
                flt_neworder = helper_funcs.sort_items_helper(_sort, lambda e: e[1].lower())
            else:
                flt_neworder = helper_funcs.sort_items_helper(_sort, lambda e: e[1], True)

        return flt_flags, flt_neworder


class SA_UL_GeometryNodeComplexity(bpy.types.UIList):
    """UI list to display all geometry nodes in a Blender file and their complexity."""

    def draw_item(self, context, layout, data, node_cache: NodeCache, icon, active_data, active_propname,
                  index):
        layout.label(text=node_cache.name)
        layout.label(text=format_num(node_cache.nodes_used), icon='NODETREE')

    def filter_items(self, context, data, propname):
        all_nodes = getattr(data, propname)
        helper_funcs = bpy.types.UI_UL_list

        # Default return values.
        flt_flags = []
        flt_neworder = []

        # Filtering by name
        if self.filter_name:
            flt_flags = helper_funcs.filter_items_by_name(self.filter_name, self.bitflag_filter_item,
                                                          all_nodes, 'name')
        if not flt_flags:
            flt_flags = [self.bitflag_filter_item] * len(all_nodes)

        if len(all_nodes) > 0:
            sort_value = context.window_manager.geometry_cache_sort_value
            _sort = [(idx, getattr(it, sort_value, '')) for idx, it in enumerate(all_nodes)]
            if sort_value == 'name':
                flt_neworder = helper_funcs.sort_items_helper(_sort, lambda e: e[1].lower())
            else:
                flt_neworder = helper_funcs.sort_items_helper(_sort, lambda e: e[1], True)

        return flt_flags, flt_neworder
